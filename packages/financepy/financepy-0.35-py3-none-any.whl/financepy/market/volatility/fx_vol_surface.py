##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane, Saeed Amen
##############################################################################

import numpy as np
from scipy.optimize import minimize

import matplotlib.pyplot as plt
from numba import njit, float64, int64

from ...utils.error import FinError
from ...utils.date import Date
from ...utils.global_vars import gDaysInYear
from ...utils.global_types import OptionTypes
from ...products.fx.fx_vanilla_option import FXVanillaOption
from ...models.option_implied_dbn import option_implied_dbn
from ...products.fx.fx_mkt_conventions import FinFXATMMethod
from ...products.fx.fx_mkt_conventions import FinFXDeltaMethod
from ...utils.helpers import check_argument_types, label_to_string
from ...market.curves.discount_curve import DiscountCurve

from ...models.black_scholes import BlackScholes

from ...models.volatility_fns import vol_function_clark
from ...models.volatility_fns import vol_function_bloomberg
from ...models.volatility_fns import VolFuncTypes
from ...models.sabr import vol_function_sabr
from ...models.sabr import vol_function_sabr_beta_one
from ...models.sabr import vol_function_sabr_beta_half

from ...utils.math import norminvcdf

from ...models.black_scholes_analytic import bs_value
from ...products.fx.fx_vanilla_option import fast_delta
from ...utils.distribution import FinDistribution

from ...utils.solver_1d import newton_secant

###############################################################################
# TODO: Speed up search for strike by providing derivative function to go with
#       delta fit.
###############################################################################


@njit(fastmath=True, cache=True)
def g(K, *args):
    """ This is the objective function used in the determination of the FX
    option implied strike which is computed in the class below. """

    s = args[0]
    t = args[1]
    r_d = args[2]
    r_f = args[3]
    volatility = args[4]
    delta_method_value = args[5]
    option_type_value = args[6]
    delta_target = args[7]

    delta_out = fast_delta(s, t, K, r_d, r_f,
                           volatility,
                           delta_method_value,
                           option_type_value)

    obj_fn = delta_target - delta_out
    return obj_fn

###############################################################################
# Do not cache this function


@njit(fastmath=True)  # , cache=True)
def obj_fast(params, *args):
    """ Return a function that is minimised when the ATM, MS and RR vols have
    been best fitted using the parametric volatility curve represented by cvec
    """

    s = args[0]
    t = args[1]
    r_d = args[2]
    r_f = args[3]
    K_ATM = args[4]
    atm_vol = args[5]
    k_25d_c_ms = args[6]
    k_25d_p_ms = args[7]
    v_25d_ms_target = args[8]
    delta_method_value = args[9]
    target_rr_vol = args[10]
    vol_type_value = args[11]

    f = s * np.exp((r_d-r_f)*t)
    # We first need to solve for the strikes at the 25 delta points using the
    # new volatility curve

    # Match the at-the-money option volatility
    atm_curve_vol = vol_function(vol_type_value, params, f, K_ATM, t)
    term1 = (atm_vol - atm_curve_vol)**2

    ###########################################################################
    # Match the market strangle value but this has to be at the MS strikes
    ###########################################################################

    sigma_k_25d_c_ms = vol_function(vol_type_value, params, f, k_25d_c_ms, t)

    V_25D_C_MS = bs_value(s, t, k_25d_c_ms, r_d, r_f, sigma_k_25d_c_ms,
                          OptionTypes.EUROPEAN_CALL.value)

    sigma_k_25d_p_ms = vol_function(vol_type_value, params, f, k_25d_p_ms, t)

    V_25D_P_MS = bs_value(s, t, k_25d_p_ms, r_d, r_f, sigma_k_25d_p_ms,
                          OptionTypes.EUROPEAN_PUT.value)

    v_25d_ms = V_25D_C_MS + V_25D_P_MS
    term2 = (v_25d_ms - v_25d_ms_target)**2

    ###########################################################################
    # Match the risk reversal volatility
    ###########################################################################

    K_25D_C = solver_for_smile_strike_fast(s, t, r_d, r_f,
                                           OptionTypes.EUROPEAN_CALL.value,
                                           vol_type_value, +0.2500,
                                           delta_method_value, k_25d_c_ms,
                                           params)

    sigma_k_25d_c = vol_function(vol_type_value, params, f, K_25D_C, t)

    K_25D_P = solver_for_smile_strike_fast(s, t, r_d, r_f,
                                           OptionTypes.EUROPEAN_PUT.value,
                                           vol_type_value, -0.2500,
                                           delta_method_value, k_25d_p_ms,
                                           params)

    sigma_k_25d_p = vol_function(vol_type_value, params, f, K_25D_P, t)

    sigma_25d_rr = (sigma_k_25d_c - sigma_k_25d_p)
    term3 = (sigma_25d_rr - target_rr_vol)**2

    # sum up the errors
    err = term1 + term2 + term3

    return err

###############################################################################
# This function cannot be jitted until the scipy minimisation has been replaced
# with a jittable function


def solve_to_horizon_fast(s, t,
                          rd, rf,
                          K_ATM, atm_vol,
                          ms_25d_vol, rr_25d_vol,
                          delta_method_value, vol_type_value,
                          xopt):

    c0 = xopt

    # Determine the price of a market strangle from market strangle
    # Need to price a call and put that agree with market strangle

    vol_25d_ms = atm_vol + ms_25d_vol

    k_25d_c_ms = solve_for_strike(s, t, rd, rf,
                                  OptionTypes.EUROPEAN_CALL.value,
                                  +0.2500,
                                  delta_method_value,
                                  vol_25d_ms)

    k_25d_p_ms = solve_for_strike(s, t, rd, rf,
                                  OptionTypes.EUROPEAN_PUT.value,
                                  -0.2500,
                                  delta_method_value,
                                  vol_25d_ms)

    # USE MARKET STRANGLE VOL TO DETERMINE PRICE OF A MARKET STRANGLE
    V_25D_C_MS = bs_value(s, t, k_25d_c_ms, rd, rf, vol_25d_ms,
                          OptionTypes.EUROPEAN_CALL.value)

    V_25D_P_MS = bs_value(s, t, k_25d_p_ms, rd, rf, vol_25d_ms,
                          OptionTypes.EUROPEAN_PUT.value)

    # Market price of strangle in the domestic currency
    v_25d_ms = V_25D_C_MS + V_25D_P_MS

    # Determine parameters of vol surface using minimisation
    tol = 1e-8

    fargs = (s, t, rd, rf,
             K_ATM, atm_vol,
             k_25d_c_ms, k_25d_p_ms,
             v_25d_ms,
             delta_method_value, rr_25d_vol, vol_type_value)

    opt = minimize(obj_fast, c0, fargs, method="CG", tol=tol)
    xopt = opt.x

    params = np.array(xopt)

    K_25D_C = solver_for_smile_strike_fast(s, t, rd, rf,
                                           OptionTypes.EUROPEAN_CALL.value,
                                           vol_type_value, +0.2500,
                                           delta_method_value, k_25d_c_ms,
                                           params)

    K_25D_P = solver_for_smile_strike_fast(s, t, rd, rf,
                                           OptionTypes.EUROPEAN_PUT.value,
                                           vol_type_value, -0.2500,
                                           delta_method_value, k_25d_p_ms,
                                           params)

    ret = (params, k_25d_c_ms, k_25d_p_ms, K_25D_C, K_25D_P)
    return ret

###############################################################################


@njit(float64(int64, float64[:], float64, float64, float64),
      cache=True, fastmath=True)
def vol_function(vol_function_type_value, params, f, k, t):
    """ Return the volatility for a strike using a given polynomial
    interpolation following Section 3.9 of Iain Clark book. """

    if vol_function_type_value == VolFuncTypes.CLARK.value:
        vol = vol_function_clark(params, f, k, t)
        return vol
    elif vol_function_type_value == VolFuncTypes.SABR.value:
        vol = vol_function_sabr(params, f, k, t)
        return vol
    elif vol_function_type_value == VolFuncTypes.SABR_BETA_ONE.value:
        vol = vol_function_sabr_beta_one(params, f, k, t)
        return vol
    elif vol_function_type_value == VolFuncTypes.SABR_BETA_HALF.value:
        vol = vol_function_sabr_beta_half(params, f, k, t)
        return vol
    elif vol_function_type_value == VolFuncTypes.BBG.value:
        vol = vol_function_bloomberg(params, f, k, t)
        return vol
    elif vol_function_type_value == VolFuncTypes.CLARK5.value:
        vol = vol_function_clark(params, f, k, t)
        return vol
    else:
        raise FinError("Unknown Model Type")

###############################################################################


@njit(cache=True, fastmath=True)
def delta_fit(K, *args):
    """ This is the objective function used in the determination of the FX
    Option implied strike which is computed in the class below. I map it into
    inverse normcdf space to avoid the flat slope of this function at low vol
    and high K. It speeds up the code as it allows initial values close to
    the solution to be used. """

    vol_type_value = args[0]
    s = args[1]
    t = args[2]
    r_d = args[3]
    r_f = args[4]
    option_type_value = args[5]
    delta_type_value = args[6]
    inverse_delta_target = args[7]
    params = args[8]

    f = s*np.exp((r_d-r_f)*t)
    v = vol_function(vol_type_value, params, f, K, t)
    delta_out = fast_delta(
        s, t, K, r_d, r_f, v, delta_type_value, option_type_value)
    inverse_delta_out = norminvcdf(np.abs(delta_out))
    inv_obj_fn = inverse_delta_target - inverse_delta_out

    return inv_obj_fn

###############################################################################
# Unable to cache this function due to dynamic globals warning. Revisit.


@njit(float64(float64, float64, float64, float64, int64, int64, float64,
              int64, float64, float64[:]), fastmath=True, cache=False)
def solver_for_smile_strike_fast(s, t, rd, rf,
                                 option_type_value,
                                 volatility_type_value,
                                 delta_target,
                                 delta_method_value,
                                 initial_guess,
                                 parameters):
    """ Solve for the strike that sets the delta of the option equal to the
    target value of delta allowing the volatility to be a function of the
    strike. """

    inverse_delta_target = norminvcdf(np.abs(delta_target))

    argtuple = (volatility_type_value, s, t, rd, rf, option_type_value,
                delta_method_value, inverse_delta_target, parameters)

    K = newton_secant(delta_fit, x0=initial_guess, args=argtuple,
                      tol=1e-8, maxiter=50)

    return K

###############################################################################
# Unable to cache function


@njit(float64(float64, float64, float64, float64, int64, float64,
              int64, float64), fastmath=True)
def solve_for_strike(spot_fx_rate,
                     tdel, rd, rf,
                     option_type_value,
                     delta_target,
                     delta_method_value,
                     volatility):
    """ This function determines the implied strike of an FX option
    given a delta and the other option details. It uses a one-dimensional
    Newton root search algorithm to determine the strike that matches an
    input volatility. """

    # =========================================================================
    # IMPORTANT NOTE:
    # =========================================================================
    # For some delta quotation conventions I can solve for K explicitly.
    # Note that as I am using the function norm_inv_delta to calculate the
    # inverse value of delta, this may not, on a round trip using N(x), give
    # back the value x as it is calculated to a different number of decimal
    # places. It should however agree to 6-7 decimal places. Which is OK.
    # =========================================================================

    if delta_method_value == FinFXDeltaMethod.SPOT_DELTA.value:

        dom_df = np.exp(-rd*tdel)
        for_df = np.exp(-rf*tdel)

        if option_type_value == OptionTypes.EUROPEAN_CALL.value:
            phi = +1.0
        else:
            phi = -1.0

        F0T = spot_fx_rate * for_df / dom_df
        vsqrtt = volatility * np.sqrt(tdel)
        arg = delta_target*phi/for_df  # CHECK THIS !!!
        norm_inv_delta = norminvcdf(arg)
        K = F0T * np.exp(-vsqrtt * (phi*norm_inv_delta - vsqrtt/2.0))
        return K

    elif delta_method_value == FinFXDeltaMethod.FORWARD_DELTA.value:

        dom_df = np.exp(-rd*tdel)
        for_df = np.exp(-rf*tdel)

        if option_type_value == OptionTypes.EUROPEAN_CALL.value:
            phi = +1.0
        else:
            phi = -1.0

        F0T = spot_fx_rate * for_df / dom_df
        vsqrtt = volatility * np.sqrt(tdel)
        arg = delta_target*phi   # CHECK THIS!!!!!!!!
        norm_inv_delta = norminvcdf(arg)
        K = F0T * np.exp(-vsqrtt * (phi*norm_inv_delta - vsqrtt/2.0))
        return K

    elif delta_method_value == FinFXDeltaMethod.SPOT_DELTA_PREM_ADJ.value:

        argtuple = (spot_fx_rate, tdel, rd, rf, volatility,
                    delta_method_value, option_type_value, delta_target)

        K = newton_secant(g, x0=spot_fx_rate, args=argtuple,
                          tol=1e-7, maxiter=50)

        return K

    elif delta_method_value == FinFXDeltaMethod.FORWARD_DELTA_PREM_ADJ.value:

        argtuple = (spot_fx_rate, tdel, rd, rf, volatility,
                    delta_method_value, option_type_value, delta_target)

        K = newton_secant(g, x0=spot_fx_rate, args=argtuple,
                          tol=1e-7, maxiter=50)

        return K

    else:

        raise FinError("Unknown FinFXDeltaMethod")

###############################################################################


class FXVolSurface():
    """ Class to perform a calibration of a chosen parametrised surface to the
    prices of FX options at different strikes and expiry tenors. The
    calibration inputs are the ATM and 25 Delta volatilities given in terms of
    the market strangle amd risk reversals. There is a choice of volatility
    function ranging from polynomial in delta to a limited version of SABR. """

    def __init__(self,
                 value_dt: Date,
                 spot_fx_rate: float,
                 currency_pair: str,
                 notional_currency: str,
                 dom_discount_curve: DiscountCurve,
                 for_discount_curve: DiscountCurve,
                 tenors: (list),
                 atm_vols: (list, np.ndarray),
                 ms25DeltaVols: (list, np.ndarray),
                 rr25DeltaVols: (list, np.ndarray),
                 atmMethod: FinFXATMMethod = FinFXATMMethod.FWD_DELTA_NEUTRAL,
                 delta_method: FinFXDeltaMethod = FinFXDeltaMethod.SPOT_DELTA,
                 volatility_function_type: VolFuncTypes = VolFuncTypes.CLARK):
        """ Create the FinFXVolSurface object by passing in market vol data
        for ATM and 25 Delta Market Strangles and Risk Reversals. """

        check_argument_types(self.__init__, locals())

        self._value_dt = value_dt
        self._spot_fx_rate = spot_fx_rate
        self._currency_pair = currency_pair

        if len(currency_pair) != 6:
            raise FinError("Currency pair must be 6 characters.")

        self._forName = self._currency_pair[0:3]
        self._domName = self._currency_pair[3:6]

        self._notional_currency = notional_currency
        self._dom_discount_curve = dom_discount_curve
        self._for_discount_curve = for_discount_curve
        self._num_vol_curves = len(tenors)

        if len(atm_vols) != self._num_vol_curves:
            raise FinError("Number ATM vols must equal number of tenors")

        if len(atm_vols) != self._num_vol_curves:
            raise FinError("Number ATM vols must equal number of tenors")

        if len(ms25DeltaVols) != self._num_vol_curves:
            raise FinError("Number MS25D vols must equal number of tenors")

        if len(rr25DeltaVols) != self._num_vol_curves:
            raise FinError("Number RR25D vols must equal number of tenors")

        self._tenors = tenors
        self._atm_vols = np.array(atm_vols)/100.0
        self._ms25DeltaVols = np.array(ms25DeltaVols)/100.0
        self._rr25DeltaVols = np.array(rr25DeltaVols)/100.0

        self._atmMethod = atmMethod
        self._delta_method = delta_method

        if self._delta_method == FinFXDeltaMethod.SPOT_DELTA:
            self._delta_method_string = "pips_spot_delta"
        elif self._delta_method == FinFXDeltaMethod.FORWARD_DELTA:
            self._delta_method_string = "pips_fwd_delta"
        elif self._delta_method == FinFXDeltaMethod.SPOT_DELTA_PREM_ADJ:
            self._delta_method_string = "pct_spot_delta_prem_adj"
        elif self._delta_method == FinFXDeltaMethod.FORWARD_DELTA_PREM_ADJ:
            self._delta_method_string = "pct_fwd_delta_prem_adj"
        else:
            raise FinError("Unknown Delta Type")

        self._vol_func_type = volatility_function_type
        self._tenor_index = 0

        self._expiry_dts = []
        for i in range(0, self._num_vol_curves):
            expiry_dt = value_dt.add_tenor(tenors[i])
            self._expiry_dts.append(expiry_dt)

        self.build_vol_surface()

###############################################################################

    def volatility(self, K, expiry_dt):
        """ Interpolate the Black-Scholes volatility from the volatility
        surface given the option strike and expiry date. Linear interpolation
        is done in variance x time. """

        vol_type_value = self._vol_func_type.value

        index0 = 0
        index1 = 0

        t = (expiry_dt - self._value_dt) / gDaysInYear

        num_curves = self._num_vol_curves

        if num_curves == 1:

            # The volatility term structure is flat if there is only one expiry
            fwd = self._F0T[0]
            t_exp = self._t_exp[0]
            vol = vol_function(vol_type_value, self._parameters[0],
                               fwd, K, t_exp)
            return vol

        # If the time is below first time then assume a flat vol
        if t <= self._t_exp[0]:

            fwd = self._F0T[0]
            t_exp = self._t_exp[0]
            vol = vol_function(vol_type_value, self._parameters[0],
                               fwd, K, t_exp)
            return vol

        # If the time is beyond the last time then extrapolate with a flat vol
        if t > self._t_exp[-1]:

            fwd = self._F0T[-1]
            t_exp = self._t_exp[-1]
            vol = vol_function(vol_type_value, self._parameters[-1],
                               fwd, K, t_exp)
            return vol

        for i in range(1, num_curves):

            if t <= self._t_exp[i] and t > self._t_exp[i-1]:
                index0 = i-1
                index1 = i
                break

        fwd0 = self._F0T[index0]
        t0 = self._t_exp[index0]
        vol0 = vol_function(vol_type_value, self._parameters[index0],
                            fwd0, K, t0)

        fwd1 = self._F0T[index1]
        t1 = self._t_exp[index1]
        vol1 = vol_function(vol_type_value, self._parameters[index1],
                            fwd1, K, t1)

        vart0 = vol0*vol0*t0
        vart1 = vol1*vol1*t1
        vart = ((t-t0) * vart1 + (t1-t) * vart0) / (t1 - t0)

        if vart < 0.0:
            raise FinError("Negative variance.")

        volt = np.sqrt(vart/t)
        return volt

###############################################################################

    def build_vol_surface(self):

        s = self._spot_fx_rate
        num_vol_curves = self._num_vol_curves

        if self._vol_func_type == VolFuncTypes.CLARK:
            num_parameters = 3
        elif self._vol_func_type == VolFuncTypes.SABR:
            num_parameters = 4
        elif self._vol_func_type == VolFuncTypes.SABR_BETA_ONE:
            num_parameters = 3
        elif self._vol_func_type == VolFuncTypes.SABR_BETA_HALF:
            num_parameters = 3
        elif self._vol_func_type == VolFuncTypes.BBG:
            num_parameters = 3
        elif self._vol_func_type == VolFuncTypes.CLARK5:
            num_parameters = 5
        else:
            print(self._vol_func_type)
            raise FinError("Unknown Model Type")

        self._parameters = np.zeros([num_vol_curves, num_parameters])

        self._F0T = np.zeros(num_vol_curves)
        self._rd = np.zeros(num_vol_curves)
        self._rf = np.zeros(num_vol_curves)
        self._K_ATM = np.zeros(num_vol_curves)
        self._deltaATM = np.zeros(num_vol_curves)

        self._k_25d_c = np.zeros(num_vol_curves)
        self._k_25d_p = np.zeros(num_vol_curves)
        self._k_25d_c_ms = np.zeros(num_vol_curves)
        self._k_25d_p_ms = np.zeros(num_vol_curves)
        self._v_25d_ms = np.zeros(num_vol_curves)
        self._t_exp = np.zeros(num_vol_curves)

        #######################################################################
        # TODO: ADD SPOT DAYS
        #######################################################################
        spot_dt = self._value_dt

        for i in range(0, num_vol_curves):

            expiry_dt = self._expiry_dts[i]
            t_exp = (expiry_dt - spot_dt) / gDaysInYear

            dom_df = self._dom_discount_curve._df(t_exp)
            for_df = self._for_discount_curve._df(t_exp)
            f = s * for_df/dom_df

            self._t_exp[i] = t_exp
            self._rd[i] = -np.log(dom_df) / t_exp
            self._rf[i] = -np.log(for_df) / t_exp
            self._F0T[i] = f

            atm_vol = self._atm_vols[i]

            # This follows exposition in Clarke Page 52
            if self._atmMethod == FinFXATMMethod.SPOT:
                self._K_ATM[i] = s
            elif self._atmMethod == FinFXATMMethod.FWD:
                self._K_ATM[i] = f
            elif self._atmMethod == FinFXATMMethod.FWD_DELTA_NEUTRAL:
                self._K_ATM[i] = f * np.exp(atm_vol*atm_vol*t_exp/2.0)
            elif self._atmMethod == FinFXATMMethod.FWD_DELTA_NEUTRAL_PREM_ADJ:
                self._K_ATM[i] = f * np.exp(-atm_vol*atm_vol*t_exp/2.0)
            else:
                raise FinError("Unknown Delta Type")

        #######################################################################
        # THE ACTUAL COMPUTATION LOOP STARTS HERE
        #######################################################################

        x_inits = []
        for i in range(0, num_vol_curves):

            atm_vol = self._atm_vols[i]
            ms25 = self._ms25DeltaVols[i]
            rr25 = self._rr25DeltaVols[i]
            s25 = atm_vol + ms25 + rr25/2.0
            s50 = atm_vol
            s75 = atm_vol + ms25 - rr25/2.0

            if self._vol_func_type == VolFuncTypes.CLARK:

                # Fit to 25D
                c0 = np.log(atm_vol)
                c1 = 2.0 * np.log(s75/s25)
                c2 = 8.0 * np.log(s25*s75/atm_vol/atm_vol)
                x_init = [c0, c1, c2]

            elif self._vol_func_type == VolFuncTypes.SABR:
                # SABR parameters are alpha, nu, rho
                # SABR parameters are alpha, nu, rho
                alpha = 0.174
                beta = 1.0
                rho = -0.112
                nu = 0.817

                x_init = [alpha, beta, rho, nu]

            elif self._vol_func_type == VolFuncTypes.SABR_BETA_ONE:
                # SABR parameters are alpha, nu, rho
                alpha = 0.174
                rho = -0.112
                nu = 0.817
                x_init = [alpha, nu, rho]

            elif self._vol_func_type == VolFuncTypes.SABR_BETA_HALF:
                # SABR parameters are alpha, nu, rho
                alpha = 0.174
                rho = -0.112
                nu = 0.817
                x_init = [alpha, rho, nu]

            elif self._vol_func_type == VolFuncTypes.BBG:

                # BBG Params if we fit to 25D
                a = 8.0*s75-16.0*s50+8.0*s25
                b = -6.0*s75+16.0*s50-10.0*s25
                c = s75-3.0*s50+3.0*s25

                x_init = [a, b, c]

            elif self._vol_func_type == VolFuncTypes.CLARK5:

                # Fit to 25D
                c0 = np.log(atm_vol)
                c1 = 2.0 * np.log(s75/s25)
                c2 = 8.0 * np.log(s25*s75/atm_vol/atm_vol)
                x_init = [c0, c1, c2, 0.0, 0.0]

            else:
                raise FinError("Unknown Model Type")

            x_inits.append(x_init)

        delta_method_value = self._delta_method.value
        vol_type_value = self._vol_func_type.value

        for i in range(0, num_vol_curves):

            t = self._t_exp[i]
            r_d = self._rd[i]
            r_f = self._rf[i]
            K_ATM = self._K_ATM[i]
            atm_vol = self._atm_vols[i]
            ms_25d_vol = self._ms25DeltaVols[i]
            rr_25d_vol = self._rr25DeltaVols[i]

#            print(t, rd, rf, K_ATM, atm_vol, ms_25d_vol, rr_25d_vol)

            res = solve_to_horizon_fast(s, t, r_d, r_f, K_ATM,
                                        atm_vol, ms_25d_vol, rr_25d_vol,
                                        delta_method_value, vol_type_value,
                                        x_inits[i])

            (self._parameters[i, :],
             self._k_25d_c_ms[i], self._k_25d_p_ms[i],
             self._k_25d_c[i], self._k_25d_p[i]) = res

###############################################################################

    def solver_for_smile_strike(self,
                                option_type_value,
                                delta_target,
                                tenor_index,
                                initialValue):
        """ Solve for the strike that sets the delta of the option equal to the
        target value of delta allowing the volatility to be a function of the
        strike. """

        s0 = self._spot_fx_rate
        tdel = self._t_exp[tenor_index]
        r_d = self._rd[tenor_index]
        r_f = self._rf[tenor_index]

        inverse_delta_target = norminvcdf(np.abs(delta_target))
        argtuple = (self, s0, tdel, r_d, r_f, option_type_value,
                    inverse_delta_target, tenor_index)

        vol_type_value = self._vol_func_type.value

        argtuple = (vol_type_value, s0, tdel, r_d, r_f, option_type_value,
                    self._delta_method.value,
                    inverse_delta_target, self._parameters[tenor_index])

        K = newton_secant(delta_fit, x0=initialValue, args=argtuple,
                          tol=1e-5, maxiter=50)

        return K

###############################################################################

    def check_calibration(self, verbose: bool, tol: float = 1e-6):

        if verbose:

            print("==========================================================")
            print("VALUE DATE:", self._value_dt)
            print("SPOT FX RATE:", self._spot_fx_rate)
            print("ATM METHOD:", self._atmMethod)
            print("DELTA METHOD:", self._delta_method)
            print("==========================================================")

        K_dummy = 999

        for i in range(0, self._num_vol_curves):

            expiry_dt = self._expiry_dts[i]

            if verbose:
                print("TENOR:", self._tenors[i])
                print("EXPIRY DATE:", expiry_dt)
                print("IN ATM VOL: %9.6f %%" % (100.0*self._atm_vols[i]))
                print("IN MKT STRANGLE 25D VOL: %9.6f %%" %
                      (100.0*self._ms25DeltaVols[i]))
                print("IN RSK REVERSAL 25D VOL: %9.6f %%" %
                      (100.0*self._rr25DeltaVols[i]))

            call = FXVanillaOption(expiry_dt,
                                   K_dummy,
                                   self._currency_pair,
                                   OptionTypes.EUROPEAN_CALL,
                                   1.0,
                                   self._notional_currency, )

            put = FXVanillaOption(expiry_dt,
                                  K_dummy,
                                  self._currency_pair,
                                  OptionTypes.EUROPEAN_PUT,
                                  1.0,
                                  self._notional_currency)

            ###################################################################
            # AT THE MONEY
            ###################################################################

            if verbose:
                print("======================================================")
                print("T_(YEARS): ", self._t_exp[i])
                print("CNT_CPD_RD:%9.6f %%" % (self._rd[i]*100))
                print("CNT_CPD_RF:%9.6f %%" % (self._rf[i]*100))
                print("FWD_RATE:  %9.6f" % (self._F0T[i]))

            sigma_ATM_out = vol_function(self._vol_func_type.value,
                                         self._parameters[i],
                                         self._F0T[i],
                                         self._K_ATM[i],
                                         self._t_exp[i])

            if verbose:
                print("======================================================")
                print("VOL FUNCTION", self._vol_func_type)
                print("VOL_PARAMETERS:", self._parameters[i])
                print("======================================================")
                print("OUT_K_ATM:  %9.6f" % (self._K_ATM[i]))
                print("OUT_ATM_VOL: %9.6f %%"
                      % (100.0*sigma_ATM_out))

            diff = sigma_ATM_out - self._atm_vols[i]

            if np.abs(diff) > tol:
                print("FAILED FIT TO ATM VOL IN: %9.6f  OUT: %9.6f  DIFF: %9.6f" %
                      (self._atm_vols[i]*100.0, sigma_ATM_out*100.0,
                       diff * 100.0))

            call._strike_fx_rate = self._K_ATM[i]
            put._strike_fx_rate = self._K_ATM[i]

            model = BlackScholes(sigma_ATM_out)

            delta_call = call.delta(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)[self._delta_method_string]

            delta_put = put.delta(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)[self._delta_method_string]

            if verbose:
                print("CALL_DELTA: % 9.6f  PUT_DELTA: % 9.6f  NET_DELTA: % 9.6f"
                      % (delta_call, delta_put, delta_call + delta_put))

            ###################################################################
            # NOW WE ASSIGN THE SAME VOLATILITY TO THE MS STRIKES
            # THESE STRIKES ARE DETERMINED BY SETTING DELTA TO 0.25/-0.25
            ###################################################################

            msVol = self._atm_vols[i] + self._ms25DeltaVols[i]

            if verbose:

                print("======================================================")
                print("MKT STRANGLE VOL IN: %9.6f %%"
                      % (100.0*self._ms25DeltaVols[i]))

            call._strike_fx_rate = self._k_25d_c_ms[i]
            put._strike_fx_rate = self._k_25d_p_ms[i]

            model = BlackScholes(msVol)

            delta_call = call.delta(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)[self._delta_method_string]

            delta_put = put.delta(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)[self._delta_method_string]

            if verbose:
                print("k_25d_c_ms: %9.6f  ATM + MSVOL: %9.6f %%   DELTA: %9.6f"
                      % (self._k_25d_c_ms[i], 100.0*msVol, delta_call))

                print("k_25d_p_ms: %9.6f  ATM + MSVOL: %9.6f %%   DELTA: %9.6f"
                      % (self._k_25d_p_ms[i], 100.0*msVol, delta_put))

            call_value = call.value(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)['v']

            put_value = put.value(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)['v']

            mktStrangleValue = call_value + put_value

            if verbose:
                print("CALL_VALUE: %9.6f  PUT_VALUE: %9.6f  MS_VALUE: % 9.6f"
                      % (call_value, put_value, mktStrangleValue))

            ###################################################################
            # NOW WE ASSIGN A DIFFERENT VOLATILITY TO THE MS STRIKES
            # THE DELTAS WILL NO LONGER EQUAL 0.25, -0.25
            ###################################################################

            # CALL
            sigma_k_25d_c_ms = vol_function(self._vol_func_type.value,
                                            self._parameters[i],
                                            self._F0T[i],
                                            self._k_25d_c_ms[i],
                                            self._t_exp[i])

            model = BlackScholes(sigma_k_25d_c_ms)
            call_value = call.value(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)['v']

            # THIS IS NOT GOING TO BE 0.25 AS WE HAVE USED A DIFFERENT SKEW VOL
            delta_call = call.delta(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)[self._delta_method_string]

            # PUT
            sigma_k_25d_p_ms = vol_function(self._vol_func_type.value,
                                            self._parameters[i],
                                            self._F0T[i],
                                            self._k_25d_p_ms[i],
                                            self._t_exp[i])

            model = BlackScholes(sigma_k_25d_p_ms)
            put_value = put.value(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)['v']

            # THIS IS NOT GOING TO BE -0.25 AS WE HAVE USED A DIFFERENT SKEW VOL
            delta_put = put.delta(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)[self._delta_method_string]

            mktStrangleValueSkew = call_value + put_value

            if verbose:
                print("k_25d_c_ms: %9.6f  SURFACE_VOL: %9.6f %%   DELTA: %9.6f"
                      % (self._k_25d_c_ms[i], 100.0*sigma_k_25d_c_ms, delta_call))

                print("k_25d_p_ms: %9.6f  SURFACE_VOL: %9.6f %%   DELTA: %9.6f"
                      % (self._k_25d_p_ms[i], 100.0*sigma_k_25d_p_ms, delta_put))

                print("CALL_VALUE: %9.6f  PUT_VALUE: %9.6f  MS_SKEW_VALUE: % 9.6f"
                      % (call_value, put_value, mktStrangleValueSkew))

            diff = mktStrangleValue - mktStrangleValueSkew
            if np.abs(diff) > tol:
                print("FAILED FIT TO 25D MS VAL: %9.6f  OUT: %9.6f  DIFF: % 9.6f" %
                      (mktStrangleValue, mktStrangleValueSkew, diff))

            ###################################################################
            # NOW WE SHIFT STRIKES SO THAT DELTAS NOW EQUAL 0.25, -0.25
            ###################################################################

            call._strike_fx_rate = self._k_25d_c[i]
            put._strike_fx_rate = self._k_25d_p[i]

            sigma_k_25d_c = vol_function(self._vol_func_type.value,
                                         self._parameters[i],
                                         self._F0T[i],
                                         self._k_25d_c[i],
                                         self._t_exp[i])

            model = BlackScholes(sigma_k_25d_c)

            # THIS DELTA SHOULD BE +0.25
            delta_call = call.delta(self._value_dt,
                                    self._spot_fx_rate,
                                    self._dom_discount_curve,
                                    self._for_discount_curve,
                                    model)[self._delta_method_string]

            sigma_k_25d_p = vol_function(self._vol_func_type.value,
                                         self._parameters[i],
                                         self._F0T[i],
                                         self._k_25d_p[i],
                                         self._t_exp[i])

            model = BlackScholes(sigma_k_25d_p)

            # THIS DELTA SHOULD BE -0.25
            delta_put = put.delta(self._value_dt,
                                  self._spot_fx_rate,
                                  self._dom_discount_curve,
                                  self._for_discount_curve,
                                  model)[self._delta_method_string]

            if verbose:
                print("K_25D_C: %9.7f  VOL: %9.6f  DELTA: % 9.6f"
                      % (self._k_25d_c[i], 100.0*sigma_k_25d_c, delta_call))

                print("K_25D_P: %9.7f  VOL: %9.6f  DELTA: % 9.6f"
                      % (self._k_25d_p[i], 100.0*sigma_k_25d_p, delta_put))

            sigma_RR = sigma_k_25d_c - sigma_k_25d_p

            if verbose:
                print("==========================================================")
                print("RR = VOL_K_25_C - VOL_K_25_P => RR_IN: %9.6f %% RR_OUT: %9.6f %%"
                      % (100.0 * self._rr25DeltaVols[i], 100.0*sigma_RR))
                print("==========================================================")

            diff = sigma_RR - self._rr25DeltaVols[i]

            if np.abs(diff) > tol:
                print("FAILED FIT TO 25D RRV IN: % 9.6f  OUT: % 9.6f  DIFF: % 9.6f" %
                      (self._rr25DeltaVols[i]*100.0,
                       sigma_RR*100.0,
                       diff*100.0))

###############################################################################

    def implied_dbns(self, low_fx, high_fx, num_intervals):
        """ Calculate the pdf for each tenor horizon. Returns a list of
        FinDistribution objects, one for each tenor horizon. """

        dbns = []

        for i_tenor in range(0, len(self._tenors)):

            f = self._F0T[i_tenor]
            t_exp = self._t_exp[i_tenor]

            dFX = (high_fx - low_fx) / num_intervals

            dom_df = self._dom_discount_curve.df(t_exp)
            for_df = self._for_discount_curve.df(t_exp)

            r_d = -np.log(dom_df) / t_exp
            r_f = -np.log(for_df) / t_exp

            Ks = []
            vols = []

            for iK in range(0, num_intervals):

                k = low_fx + iK*dFX

                vol = vol_function(self._vol_func_type.value,
                                   self._parameters[i_tenor],
                                   f, k, t_exp)

                Ks.append(k)
                vols.append(vol)

            Ks = np.array(Ks)
            vols = np.array(vols)

            density = option_implied_dbn(self._spot_fx_rate, t_exp,
                                         r_d, r_f, Ks, vols)

            dbn = FinDistribution(Ks, density)
            dbns.append(dbn)

        return dbns

###############################################################################

    def plot_vol_curves(self):

        plt.figure()

        vol_type_val = self._vol_func_type.value

        for tenor_index in range(0, self._num_vol_curves):

            atm_vol = self._atm_vols[tenor_index]*100
            msVol = self._ms25DeltaVols[tenor_index]*100
            rrVol = self._rr25DeltaVols[tenor_index]*100

            lowK = self._k_25d_p[tenor_index] * 0.75
            highK = self._k_25d_c[tenor_index] * 1.25

            strikes = []
            vols = []
            num_intervals = 30
            K = lowK
            dK = (highK - lowK)/num_intervals
            params = self._parameters[tenor_index]
            t = self._t_exp[tenor_index]
            f = self._F0T[tenor_index]

            for _ in range(0, num_intervals):
                sigma = vol_function(vol_type_val, params, f, K, t) * 100.0
                strikes.append(K)
                vols.append(sigma)
                K = K + dK

            label_str = self._tenors[tenor_index]
            label_str += " ATM: " + str(atm_vol)[0:6]
            label_str += " MS: " + str(msVol)[0:6]
            label_str += " RR: " + str(rrVol)[0:6]

            plt.plot(strikes, vols, label=label_str)
            plt.xlabel("Strike")
            plt.ylabel("Volatility")

            title = "25D FIT:" + self._currency_pair + \
                " " + str(self._vol_func_type)

            key_strikes = []
            key_strikes.append(self._K_ATM[tenor_index])

            key_vols = []
            for K in key_strikes:
                sigma = vol_function(vol_type_val, params, f, K, t) * 100.0
                key_vols.append(sigma)

            plt.plot(key_strikes, key_vols, 'ko', markersize=4)

            key_strikes = []
            key_strikes.append(self._k_25d_p[tenor_index])
            key_strikes.append(self._k_25d_p_ms[tenor_index])
            key_strikes.append(self._k_25d_c[tenor_index])
            key_strikes.append(self._k_25d_c_ms[tenor_index])

            key_vols = []

            for K in key_strikes:
                sigma = vol_function(vol_type_val, params, f, K, t) * 100.0
                key_vols.append(sigma)

            plt.plot(key_strikes, key_vols, 'bo', markersize=4)

        plt.title(title)
#        plt.legend(loc="lower left", bbox_to_anchor=(1,0))

###############################################################################

    def __repr__(self):
        s = label_to_string("OBJECT TYPE", type(self).__name__)
        s += label_to_string("VALUE DATE", self._value_dt)
        s += label_to_string("FX RATE", self._spot_fx_rate)
        s += label_to_string("CCY PAIR", self._currency_pair)
        s += label_to_string("NOTIONAL CCY", self._notional_currency)
        s += label_to_string("NUM TENORS", self._num_vol_curves)
        s += label_to_string("ATM METHOD", self._atmMethod)
        s += label_to_string("DELTA METHOD", self._delta_method)
        s += label_to_string("VOL FUNCTION", self._vol_func_type)

        for i in range(0, self._num_vol_curves):

            s += "\n"

            s += label_to_string("TENOR", self._tenors[i])
            s += label_to_string("EXPIRY DATE", self._expiry_dts[i])
            s += label_to_string("TIME (YRS)", self._t_exp[i])
            s += label_to_string("FWD FX", self._F0T[i])

            s += label_to_string("ATM VOLS", self._atm_vols[i]*100.0)
            s += label_to_string("MS VOLS", self._ms25DeltaVols[i]*100.0)
            s += label_to_string("RR VOLS", self._rr25DeltaVols[i]*100.0)

            s += label_to_string("ATM Strike", self._K_ATM[i])
            s += label_to_string("ATM Delta", self._deltaATM[i])

            s += label_to_string("K_ATM", self._K_ATM[i])
            s += label_to_string("MS 25D Call Strike", self._k_25d_c_ms[i])
            s += label_to_string("MS 25D Put Strike", self._k_25d_p_ms[i])
            s += label_to_string("SKEW 25D CALL STRIKE", self._k_25d_c[i])
            s += label_to_string("SKEW 25D PUT STRIKE", self._k_25d_p[i])
            s += label_to_string("PARAMS", self._parameters[i])

        return s

###############################################################################

    def _print(self):
        """ Print a list of the unadjusted coupon payment dates used in
        analytic calculations for the bond. """
        print(self)

###############################################################################
