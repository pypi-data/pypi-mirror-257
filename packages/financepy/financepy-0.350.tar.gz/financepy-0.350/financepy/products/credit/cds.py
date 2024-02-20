##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

from copy import deepcopy
from math import exp, log

import numpy as np
from numba import njit, float64, int64

from ...utils.date import Date
from ...utils.error import FinError
from ...utils.calendar import Calendar, CalendarTypes
from ...utils.calendar import BusDayAdjustTypes, DateGenRuleTypes
from ...utils.day_count import DayCount, DayCountTypes
from ...utils.frequency import annual_frequency, FrequencyTypes
from ...utils.global_vars import gDaysInYear
from ...utils.math import ONE_MILLION
from ...utils.helpers import label_to_string, table_to_string
from ...market.curves.interpolator import InterpTypes, _uinterpolate

from ...utils.helpers import check_argument_types

use_flat_hazard_rate_integral = True
standard_recovery_rate = 0.40
glob_num_steps_per_year = 25

###############################################################################
# TODO: Perform protection leg pv analytically using fact that hazard rate and
#       interest rates are flat between their combined node points. Right now I
#       do not find the protection leg PV calculations to be a bottleneck,
#       especially given the speedup benefits of using NUMBA.
###############################################################################


@njit(float64[:](float64, float64, float64[:], float64[:], float64[:],
                 float64[:], float64[:], float64[:], int64),
      fastmath=True, cache=True)
def _risky_pv01_numba(teff,
                      accrual_factorPCDToNow,
                      payment_times,
                      year_fracs,
                      npIborTimes,
                      npIborValues,
                      npSurvTimes,
                      npSurvValues,
                      pv01_method):
    """ Fast calculation of the risky PV01 of a CDS using NUMBA.
    The output is a numpy array of the full and clean risky PV01."""

    method = InterpTypes.FLAT_FWD_RATES.value

    if 1 == 0:
        print("===================")
        print("Teff", teff)
        print("Acc", accrual_factorPCDToNow)
        print("Payments", payment_times)
        print("Alphas", year_fracs)
        print("QTimes", npSurvTimes)
        print("QValues", npSurvValues)

    cpnAccruedIndicator = 1

    # Method 0 : This is the market standard which assumes that the cpn
    # accrued is treated as though on average default occurs roughly midway
    # through a cpn period.

    tncd = payment_times[0]

    # The first cpn is a special case which needs to be handled carefully
    # taking into account what cpn has already accrued and what has not
    qeff = _uinterpolate(teff, npSurvTimes, npSurvValues, method)
    q1 = _uinterpolate(tncd, npSurvTimes, npSurvValues, method)
    z1 = _uinterpolate(tncd, npIborTimes, npIborValues, method)

    # this is the part of the cpn accrued from previous cpn date to now
    # accrual_factorPCDToNow = day_count.year_frac(pcd,teff)

    # reference credit survives to the premium payment date
    full_rpv01 = q1 * z1 * year_fracs[1]

    # cpn accrued from previous cpn to today paid in full at default
    # before cpn payment
    full_rpv01 = full_rpv01 + z1 * \
        (qeff - q1) * accrual_factorPCDToNow * cpnAccruedIndicator

    # future accrued from now to cpn payment date assuming default roughly
    # midway
    full_rpv01 += 0.5 * z1 * \
        (qeff - q1) * (year_fracs[1] - accrual_factorPCDToNow) \
        * cpnAccruedIndicator

    for it in range(1, len(payment_times)):

        t2 = payment_times[it]

        q2 = _uinterpolate(t2, npSurvTimes, npSurvValues, method)
        z2 = _uinterpolate(t2, npIborTimes, npIborValues, method)

        accrual_factor = year_fracs[it]

        # full cpn is paid at the end of the current period if survives to
        # payment date
        full_rpv01 += q2 * z2 * accrual_factor

        #######################################################################

        if cpnAccruedIndicator == 1:

            if use_flat_hazard_rate_integral:
                # This needs to be updated to handle small h+r
                tau = accrual_factor
                h12 = -log(q2 / q1) / tau
                r12 = -log(z2 / z1) / tau
                alpha = h12 + r12
                expTerm = 1.0 - exp(-alpha * tau) - alpha * \
                    tau * exp(-alpha * tau)
                d_full_rpv01 = q1 * z1 * h12 * \
                    expTerm / abs(alpha * alpha + 1e-20)
            else:
                d_full_rpv01 = 0.50 * (q1 - q2) * z2 * accrual_factor

            full_rpv01 = full_rpv01 + d_full_rpv01

        q1 = q2

    clean_rpv01 = full_rpv01 - accrual_factorPCDToNow

    return np.array([full_rpv01, clean_rpv01])

###############################################################################


@njit(float64(float64, float64, float64[:], float64[:], float64[:], float64[:],
              float64, int64, int64), fastmath=True, cache=True)
def _protection_leg_pv_numba(teff,
                             t_mat,
                             npIborTimes,
                             npIborValues,
                             npSurvTimes,
                             npSurvValues,
                             contract_recovery_rate,
                             num_steps_per_year,
                             prot_method):
    """ Fast calculation of the CDS protection leg PV using NUMBA to speed up
    the numerical integration over time. """

    method = InterpTypes.FLAT_FWD_RATES.value
    dt = 1.0 / num_steps_per_year
    num_steps = int((t_mat-teff) * num_steps_per_year + 0.50)
    dt = (t_mat - teff) / num_steps

    t = teff
    z1 = _uinterpolate(t, npIborTimes, npIborValues, method)
    q1 = _uinterpolate(t, npSurvTimes, npSurvValues, method)

    prot_pv = 0.0
    small = 1e-8

    if use_flat_hazard_rate_integral:

        for _ in range(0, num_steps):
            t = t + dt
            z2 = _uinterpolate(t, npIborTimes, npIborValues, method)
            q2 = _uinterpolate(t, npSurvTimes, npSurvValues, method)
            # This needs to be updated to handle small h+r
            h12 = -log(q2 / q1) / dt
            r12 = -log(z2 / z1) / dt
            expTerm = exp(-(r12 + h12) * dt)
            dprot_pv = h12 * (1.0 - expTerm) * q1 * z1 / \
                (abs(h12 + r12) + small)
            prot_pv += dprot_pv
            q1 = q2
            z1 = z2

    else:

        for _ in range(0, num_steps):
            t += dt
            z2 = _uinterpolate(t, npIborTimes, npIborValues, method)
            q2 = _uinterpolate(t, npSurvTimes, npSurvValues, method)
            dq = q1 - q2
            dprot_pv = 0.5 * (z1 + z2) * dq
            prot_pv += dprot_pv
            q1 = q2
            z1 = z2

    prot_pv = prot_pv * (1.0 - contract_recovery_rate)
    return prot_pv

###############################################################################
###############################################################################
###############################################################################


class CDS:
    """ A class which manages a Credit Default Swap. It performs schedule
    generation and the valuation and risk management of CDS. """

    def __init__(self,
                 step_in_dt: Date,  # Date protection starts
                 maturity_dt_or_tenor: (Date, str),  # Date or tenor
                 running_cpn: float,  # Annualised cpn on premium fee leg
                 notional: float = ONE_MILLION,
                 long_protection: bool = True,
                 freq_type: FrequencyTypes = FrequencyTypes.QUARTERLY,
                 dc_type: DayCountTypes = DayCountTypes.ACT_360,
                 cal_type: CalendarTypes = CalendarTypes.WEEKEND,
                 bd_type: BusDayAdjustTypes = BusDayAdjustTypes.FOLLOWING,
                 dg_type: DateGenRuleTypes = DateGenRuleTypes.BACKWARD):
        """ Create a CDS from the step-in date, maturity date and cpn """

        check_argument_types(self.__init__, locals())

        if type(maturity_dt_or_tenor) == Date:
            maturity_dt = maturity_dt_or_tenor
        else:
            # To get the next CDS date we move on by the tenor and then roll to
            # the next CDS date after that. We do not holiday adjust it. That
            # is handled in the schedule generation.
            maturity_dt = step_in_dt.add_tenor(maturity_dt_or_tenor)
            maturity_dt = maturity_dt.next_cds_date()

        if step_in_dt > maturity_dt:
            raise FinError("Step in date after maturity date")

        self._step_in_dt = step_in_dt
        self._maturity_dt = maturity_dt
        self._running_cpn = running_cpn
        self._notional = notional
        self._long_protection = long_protection
        self._dc_type = dc_type
        self._dg_type = dg_type
        self._cal_type = cal_type
        self._freq_type = freq_type
        self._bd_type = bd_type

        self._generate_adjusted_cds_payment_dts()
        self._calc_flows()

    ###########################################################################

    def _generate_adjusted_cds_payment_dts(self):
        """ Generate CDS payment dates which have been holiday adjusted."""

        frequency = annual_frequency(self._freq_type)
        calendar = Calendar(self._cal_type)
        start_dt = self._step_in_dt

        self._payment_dts = []
        self._accrual_start_dts = []
        self._accrual_end_dts = []
        num_months = int(12.0 / frequency)

        # We generate unadjusted dates - not adjusted for weekends or holidays
        unadjusted_schedule_dts = []

        if self._dg_type == DateGenRuleTypes.BACKWARD:

            # We start at end date and step backwards

            next_dt = self._maturity_dt

            unadjusted_schedule_dts.append(next_dt)

            # the unadjusted dates start at end date and end at previous
            # cpn date
            while next_dt > start_dt:
                next_dt = next_dt.add_months(-num_months)
                unadjusted_schedule_dts.append(next_dt)

            # now we adjust for holiday using business day adjustment
            # convention specified
            adjusted_dts = []

            for date in reversed(unadjusted_schedule_dts):
                adjusted = calendar.adjust(date, self._bd_type)
                adjusted_dts.append(adjusted)

# eg: https://www.cdsmodel.com/assets/cds-model/docs/Standard%20CDS%20Examples.pdf
# Payment       = [20-MAR-2009, 22-JUN-2009, 21-SEP-2009, 21-DEC-2009, 22-MAR-2010]
# Accrual Start = [22-DEC-2008, 20-MAR-2009, 22-JUN-2009, 21-SEP-2009, 21-DEC-2009]
# Accrual End   = [19-MAR-2009, 21-JUN-2009, 20-SEP-2009, 20-DEC-2009, 20-MAR-2010]

        elif self._dg_type == DateGenRuleTypes.FORWARD:

            # We start at start date and step forwards

            next_dt = start_dt

            # the unadjusted dates start at start date and end at last date
            # before maturity date
            while next_dt < self._maturity_dt:
                unadjusted_schedule_dts.append(next_dt)
                next_dt = next_dt.add_months(num_months)

            # We then append the maturity date
            unadjusted_schedule_dts.append(self._maturity_dt)

            adjusted_dts = []
            for date in unadjusted_schedule_dts:
                adjusted = calendar.adjust(date, self._bd_type)
                adjusted_dts.append(adjusted)

    # eg. Date(20, 2, 2009) to Date(20, 3, 2010) with DateGenRuleTypes.FORWARD
    # Payment       = [20-MAY-2009, 20-AUG-2009, 20-NOV-2009, 22-FEB-2010]
    # Accrual Start = [20-FEB-2009, 20-MAY-2009, 20-AUG-2009, 20-NOV-2009]
    # Accrual End   = [19-MAY-2009, 19-AUG-2009, 19-NOV-2009, 20-MAR-2010]

        else:

            raise FinError("Unknown DateGenRuleType:"
                           + str(self._dg_type))

        # We only include dates which fall after the CDS start date
        self._payment_dts = adjusted_dts[1:]

        # Accrual start dates run from previous cpn date to penultimate
        # cpn date
        self._accrual_start_dts = adjusted_dts[:-1]

        # Accrual end dates are one day before the start of the next
        # accrual period
        self._accrual_end_dts = [
            date.add_days(-1) for date in self._accrual_start_dts[1:]]

        # Final accrual end date is the maturity date
        self._accrual_end_dts.append(self._maturity_dt)

    ###########################################################################

    def _calc_flows(self):
        """ Calculate cash flow amounts on premium leg. """
        day_count = DayCount(self._dc_type)

        self._accrual_factors = []
        self._flows = []

        # self._accrual_factors.append(0.0)
        # self._flows.append(0.0)

        for t0, t1 in zip(self._accrual_start_dts, self._accrual_end_dts):
            # Adding a day because `year_frac` is non-inclusive
            # eg. 20th to 22nd should be 3 days
            accrual_factor = day_count.year_frac(t0, t1.add_days(1))[0]
            flow = accrual_factor * self._running_cpn * self._notional

            self._accrual_factors.append(accrual_factor)
            self._flows.append(flow)

    ###########################################################################

    def value(self,
              value_dt,
              issuer_curve,
              contract_recovery_rate,
              pv01_method=0,
              prot_method=0,
              num_steps_per_year=glob_num_steps_per_year):
        """ Valuation of a CDS contract on a specific valuation date given
        an issuer curve and a contract recovery rate."""

        rpv01 = self.risky_pv01(value_dt,
                                issuer_curve,
                                pv01_method)

        dirtyRPV01 = rpv01['dirty_rpv01']
        clean_rpv01 = rpv01['clean_rpv01']

        prot_pv = self.protection_leg_pv(value_dt,
                                         issuer_curve,
                                         contract_recovery_rate,
                                         num_steps_per_year,
                                         prot_method)

        fwdDf = 1.0

        if self._long_protection:
            longProt = +1
        else:
            longProt = -1

        dirtyPV = fwdDf * longProt * \
            (prot_pv - self._running_cpn * dirtyRPV01 * self._notional)
        clean_pv = fwdDf * longProt * \
            (prot_pv - self._running_cpn * clean_rpv01 * self._notional)

        return {'dirty_pv': dirtyPV, 'clean_pv': clean_pv}

    ###########################################################################

    def credit_dv01(self,
                    value_dt,
                    issuer_curve,
                    contract_recovery_rate,
                    pv01_method=0,
                    prot_method=0,
                    num_steps_per_year=glob_num_steps_per_year):
        """ Calculation of the change in the value of the CDS contract for a
        one basis point change in the level of the CDS curve."""

        v0 = self.value(value_dt,
                        issuer_curve,
                        contract_recovery_rate,
                        pv01_method,
                        prot_method,
                        num_steps_per_year)

        bump = 0.0001  # 1 basis point

        # we create a deep copy to avoid state issues
        bumpedIssuerCurve = deepcopy(issuer_curve)
        for cds in bumpedIssuerCurve._cds_contracts:
            cds._running_cpn += bump

        bumpedIssuerCurve._build_curve()

        v1 = self.value(value_dt,
                        bumpedIssuerCurve,
                        contract_recovery_rate,
                        pv01_method,
                        prot_method,
                        num_steps_per_year)

        credit_dv01 = v1['dirty_pv'] - v0['dirty_pv']
        return credit_dv01

    ###########################################################################

    def interest_dv01(self,
                      value_dt: Date,
                      issuer_curve,
                      contract_recovery_rate,
                      pv01_method: int = 0,
                      prot_method: int = 0,
                      num_steps_per_year=glob_num_steps_per_year):
        """ Calculation of the interest DV01 based on a simple bump of
        the discount factors and reconstruction of the CDS curve. """

        v0 = self.value(value_dt,
                        issuer_curve,
                        contract_recovery_rate,
                        pv01_method,
                        prot_method,
                        num_steps_per_year)

        # we create a deep copy to avoid state issues
        new_issuer_curve = deepcopy(issuer_curve)

        bump = 0.0001  # 1 basis point

        for depo in new_issuer_curve._libor_curve._usedDeposits:

            depo._deposit_rate += bump

        for fra in new_issuer_curve._libor_curve._usedFRAs:

            fra._fraRate += bump

        for swap in new_issuer_curve._libor_curve._usedSwaps:

            cpn = swap._fixed_leg._cpn
            swap._fixed_leg._cpn = cpn + bump

            # Need to regenerate fixed leg payments with bumped cpn
            # I could call swap._fixed_leg.generate_payments() but it is
            # overkill as it has to do all the schedule generation which is
            # not needed as the dates are unchanged
            num_payments = len(swap._fixed_leg._payments)
            for i in range(0, num_payments):
                old_pmt = swap._fixed_leg._payments[i]
                swap._fixed_leg._payments[i] = old_pmt * (cpn + bump) / cpn

        new_issuer_curve._libor_curve._build_curve()
        new_issuer_curve._build_curve()

        v1 = self.value(value_dt,
                        new_issuer_curve,
                        contract_recovery_rate,
                        pv01_method,
                        prot_method,
                        num_steps_per_year)

        interest_dv01 = v1['dirty_pv'] - v0['dirty_pv']
        return interest_dv01

    ###########################################################################

    def cash_settlement_amount(self,
                               value_dt,
                               settle_dt,
                               issuer_curve,
                               contract_recovery_rate,
                               pv01_method=0,
                               prot_method=0,
                               num_steps_per_year=glob_num_steps_per_year):
        """ Value of the contract on the settlement date including accrued
        interest. """

        v = self.value(value_dt,
                       issuer_curve,
                       contract_recovery_rate,
                       pv01_method,
                       prot_method,
                       num_steps_per_year)

        libor_curve = issuer_curve._libor_curve
        df = libor_curve.df(settle_dt)
        v = v / df
        return v

    ###########################################################################

    def clean_price(self,
                    value_dt,
                    issuer_curve,
                    contract_recovery_rate,
                    pv01_method=0,
                    prot_method=0,
                    num_steps_per_year=glob_num_steps_per_year):
        """ Value of the CDS contract excluding accrued interest. """

        risky_pv01 = self.risky_pv01(value_dt, issuer_curve, pv01_method)

        clean_rpv01 = risky_pv01['clean_rpv01']

        prot_pv = self.protection_leg_pv(value_dt,
                                         issuer_curve,
                                         contract_recovery_rate,
                                         num_steps_per_year,
                                         prot_method)

        fwdDf = 1.0

        clean_pv = fwdDf * (prot_pv - self._running_cpn * clean_rpv01
                           * self._notional)

        clean_price = (self._notional - clean_pv) / self._notional * 100.0

        return clean_price

    ###########################################################################

    def accrued_days(self):
        """ Number of days between the previous coupon and the currrent step
        in date. """

        # I assume accrued runs to the effective date
        pcd = self._accrual_start_dts[0]
        accrued_days = self._step_in_dt - pcd
        return accrued_days

    ###########################################################################

    def accrued_interest(self):
        """ Calculate the amount of accrued interest that has accrued from the
        previous cpn date (PCD) to the step_in_dt of the CDS contract. """

        day_count = DayCount(self._dc_type)
        pcd = self._accrual_start_dts[0]
        accrual_factor = day_count.year_frac(pcd, self._step_in_dt)[0]
        accrued_interest = accrual_factor * self._notional \
            * self._running_cpn

        if self._long_protection:
            accrued_interest *= -1.0

        return accrued_interest

    ###########################################################################

    def protection_leg_pv(self,
                          value_dt,
                          issuer_curve,
                          contract_recovery_rate=standard_recovery_rate,
                          num_steps_per_year=glob_num_steps_per_year,
                          prot_method=0):
        """ Calculates the protection leg PV of the CDS by calling into the
        fast NUMBA code that has been defined above. """

        teff = (self._step_in_dt - value_dt) / gDaysInYear
        t_mat = (self._maturity_dt - value_dt) / gDaysInYear

        libor_curve = issuer_curve._libor_curve

        v = _protection_leg_pv_numba(teff,
                                     t_mat,
                                     libor_curve._times,
                                     libor_curve._dfs,
                                     issuer_curve._times,
                                     issuer_curve._values,
                                     contract_recovery_rate,
                                     num_steps_per_year,
                                     prot_method)

        return v * self._notional

    ###########################################################################

    def risky_pv01(self,
                   value_dt,
                   issuer_curve,
                   pv01_method=0):
        """ The risky_pv01 is the present value of a risky one dollar paid on
        the premium leg of a CDS contract. """

        libor_curve = issuer_curve._libor_curve

        payment_times = []
        for date in self._payment_dts:
            t = (date - value_dt) / gDaysInYear

            if t > 0.0:
                payment_times.append(t)

        # this is the part of the cpn accrued from the previous cpn date
        # to now
        pcd = self._accrual_start_dts[0]
        eff = self._step_in_dt
        day_count = DayCount(self._dc_type)

        accrual_factorPCDToNow = day_count.year_frac(pcd, eff)[0]

        year_fracs = self._accrual_factors
        teff = (eff - value_dt) / gDaysInYear

        valueRPV01 = _risky_pv01_numba(teff,
                                       accrual_factorPCDToNow,
                                       np.array(payment_times),
                                       np.array(year_fracs),
                                       libor_curve._times,
                                       libor_curve._dfs,
                                       issuer_curve._times,
                                       issuer_curve._values,
                                       pv01_method)

        full_rpv01 = valueRPV01[0]
        clean_rpv01 = valueRPV01[1]

        return {'dirty_rpv01': full_rpv01, 'clean_rpv01': clean_rpv01}

    ###########################################################################

    def premium_leg_pv(self,
                       value_dt,
                       issuer_curve,
                       pv01_method=0):
        """ Value of the premium leg of a CDS. """

        full_rpv01 = self.risky_pv01(value_dt,
                                    issuer_curve,
                                    pv01_method)['dirty_rpv01']

        v = full_rpv01 * self._notional * self._running_cpn
        return v

    ###########################################################################

    def par_spread(self,
                   value_dt,
                   issuer_curve,
                   contract_recovery_rate=standard_recovery_rate,
                   num_steps_per_year=glob_num_steps_per_year,
                   pv01_method=0,
                   prot_method=0):
        """ Breakeven CDS cpn that would make the value of the CDS contract
        equal to zero. """

        clean_rpv01 = self.risky_pv01(value_dt,
                                     issuer_curve,
                                     pv01_method)['clean_rpv01']

        prot = self.protection_leg_pv(value_dt,
                                      issuer_curve,
                                      contract_recovery_rate,
                                      num_steps_per_year,
                                      prot_method)

        # By convention this is calculated using the clean RPV01
        spd = prot / clean_rpv01 / self._notional
        return spd

    ###########################################################################

    def value_fast_approx(self,
                          value_dt,
                          flat_cont_interest_rate,
                          flat_cds_curve_spread,
                          curve_recovery=standard_recovery_rate,
                          contract_recovery_rate=standard_recovery_rate):
        """ Implementation of fast valuation of the CDS contract using an
        accurate approximation that avoids curve building. """

        if isinstance(value_dt, Date) is False:
            raise FinError("Valuation date must be a Date and not " +
                           str(value_dt))

        t_mat = (self._maturity_dt - value_dt) / gDaysInYear
        t_eff = (self._step_in_dt - value_dt) / gDaysInYear

        h = flat_cds_curve_spread / (1.0 - curve_recovery)
        r = flat_cont_interest_rate
        fwdDf = 1.0
        bump_size = 0.0001

        if self._long_protection:
            long_protection = +1
        else:
            long_protection = -1

        # The sign of he accrued has already been sign adjusted for direction
        accrued = self.accrued_interest()

        # This is the clean RPV01 as it treats the PV01 stream as though it
        # pays just the accrued for the time between 0 and the maturity
        # It therefore omits the part that has accrued

        w = r + h
        z = np.exp(-w * t_eff) - np.exp(-w * t_mat)
        clean_rpv01 = (z / w) * 365.0 / 360.0
        prot_pv = h * (1.0 - contract_recovery_rate) * (z / w) * self._notional
        clean_pv = fwdDf * long_protection * \
            (prot_pv - self._running_cpn * clean_rpv01 * self._notional)
        full_pv = clean_pv + fwdDf * accrued

        #######################################################################
        # bump CDS spread and calculate
        #######################################################################

        h = (flat_cds_curve_spread + bump_size) / (1.0 - contract_recovery_rate)
        r = flat_cont_interest_rate
        w = r + h
        z = np.exp(-w * t_eff) - np.exp(-w * t_mat)
        clean_rpv01 = (z / w) * 365.0 / 360.0
        prot_pv = h * (1.0 - contract_recovery_rate) * (z / w) * self._notional
        clean_pv_credit_bumped = fwdDf * long_protection * \
            (prot_pv - self._running_cpn * clean_rpv01 * self._notional)
        full_pv_credit_bumped = clean_pv_credit_bumped \
            + fwdDf * long_protection * accrued
        credit01 = full_pv_credit_bumped - full_pv

        #######################################################################
        # bump Rate and calculate
        #######################################################################

        h = flat_cds_curve_spread / (1.0 - contract_recovery_rate)
        r = flat_cont_interest_rate + bump_size

        w = r + h
        z = np.exp(-w * t_eff) - np.exp(-w * t_mat)

        clean_rpv01 = (z / w) * 365.0 / 360.0

        prot_pv = h * (1.0 - contract_recovery_rate) * (z / w) * self._notional

        clean_pv_ir_bumped = fwdDf * long_protection * \
            (prot_pv - self._running_cpn * clean_rpv01 * self._notional)

        full_pv_ir_bumped = clean_pv_ir_bumped + fwdDf * long_protection * accrued

        ir01 = full_pv_ir_bumped - full_pv

        return (full_pv, clean_pv, credit01, ir01)

    ###########################################################################

    def print_payments(self, value_dt, issuer_curve):
        ''' We only print payments after the current valuation date '''
        num_flows = len(self._payment_dts)

        print("PAYMENT_dt      YEAR_FRAC      FLOW           DF       SURV_PROB      NPV")

        for it in range(0, num_flows):
            dt = self._payment_dts[it]

            if dt > value_dt:
                acc_factor = self._accrual_factors[it]
                flow = self._flows[it]
                z = issuer_curve.df(dt)
                q = issuer_curve.survival_prob(dt)
                print("%15s %10.6f %12.2f %12.6f %12.6f %12.2f" %
                      (dt, acc_factor, flow, z, q, flow * z * q))

    ###########################################################################

    def __repr__(self):
        """ print out details of the CDS contract and all the calculated
        cash flows """
        s = label_to_string("OBJECT TYPE", type(self).__name__)
        s += label_to_string("STEP-IN DATE", self._step_in_dt)
        s += label_to_string("MATURITY", self._maturity_dt)
        s += label_to_string("NOTIONAL", self._notional)
        s += label_to_string("RUN COUPON", self._running_cpn * 10000, "bp\n")
        s += label_to_string("DAYCOUNT", self._dc_type)
        s += label_to_string("FREQUENCY", self._freq_type)
        s += label_to_string("CALENDAR", self._cal_type)
        s += label_to_string("BUSDAYRULE", self._bd_type)
        s += label_to_string("DATEGENRULE", self._dg_type)
        s += label_to_string("ACCRUED DAYS", self.accrued_days())

        header = "PAYMENT_dt, YEAR_FRAC, ACCRUAL_START, ACCRUAL_END, FLOW"
        value_table = [
            self._payment_dts,
            self._accrual_factors,
            self._accrual_start_dts,
            self._accrual_end_dts,
            self._flows
        ]
        precision = "12.6f"

        s += table_to_string(header, value_table, precision)

        return s

    ###########################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

###############################################################################
