##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

# TODO: Add __repr__ method

from math import sqrt
import numpy as np

from ...models.gauss_copula_onefactor import tranch_surv_prob_gaussian
from ...models.gauss_copula_onefactor import tranche_surv_prob_adj_binomial
from ...models.gauss_copula_onefactor import tranche_surv_prob_recursion
from ...models.gauss_copula_lhp import tr_surv_prob_lhp

from ...utils.day_count import DayCountTypes
from ...utils.frequency import FrequencyTypes
from ...utils.calendar import CalendarTypes
from ...utils.calendar import BusDayAdjustTypes, DateGenRuleTypes

from ...products.credit.cds import CDS
from ...products.credit.cds_curve import CDSCurve

from ...utils.global_vars import gDaysInYear
from ...utils.math import ONE_MILLION
from ...market.curves.interpolator import InterpTypes, interpolate
from ...utils.error import FinError

from ...utils.helpers import check_argument_types
from ...utils.date import Date

###############################################################################

from enum import Enum


class FinLossDistributionBuilder(Enum):
    ''' Method for constructing loss distributions numerically '''
    RECURSION = 1
    ADJUSTED_BINOMIAL = 2
    GAUSSIAN = 3
    LHP = 4


###############################################################################


class CDSTranche:

    def __init__(self,
                 step_in_dt: Date,
                 maturity_dt: Date,
                 k1: float,
                 k2: float,
                 notional: float = ONE_MILLION,
                 running_cpn: float = 0.0,
                 long_protection: bool = True,
                 freq_type: FrequencyTypes = FrequencyTypes.QUARTERLY,
                 dc_type: DayCountTypes = DayCountTypes.ACT_360,
                 cal_type: CalendarTypes = CalendarTypes.WEEKEND,
                 bd_type: BusDayAdjustTypes = BusDayAdjustTypes.FOLLOWING,
                 dg_type: DateGenRuleTypes = DateGenRuleTypes.BACKWARD):

        check_argument_types(self.__init__, locals())

        if k1 >= k2:
            raise FinError("K1 must be less than K2")

        self._k1 = k1
        self._k2 = k2

        self._step_in_dt = step_in_dt
        self._maturity_dt = maturity_dt
        self._notional = notional
        self._running_cpn = running_cpn
        self._long_protection = long_protection
        self._dc_type = dc_type
        self._dg_type = dg_type
        self._cal_type = cal_type
        self._freq_type = freq_type
        self._bd_type = bd_type

        notional = 1.0

        self._cds_contract = CDS(self._step_in_dt,
                                 self._maturity_dt,
                                 self._running_cpn,
                                 notional,
                                 self._long_protection,
                                 self._freq_type,
                                 self._dc_type,
                                 self._cal_type,
                                 self._bd_type,
                                 self._dg_type)

    ###########################################################################

    def value_bc(self,
                 value_dt,
                 issuer_curves,
                 upfront,
                 running_cpn,
                 corr1,
                 corr2,
                 num_points=50,
                 model=FinLossDistributionBuilder.RECURSION):

        num_credits = len(issuer_curves)
        k1 = self._k1
        k2 = self._k2
        t_mat = (self._maturity_dt - value_dt) / gDaysInYear

        if t_mat < 0.0:
            raise FinError("Value date is after maturity date")

        if abs(k1 - k2) < 0.00000001:
            output = np.zeros(4)
            output[0] = 0.0
            output[1] = 0.0
            output[2] = 0.0
            output[3] = 0.0
            return output

        if k1 > k2:
            raise FinError("K1 > K2")

        kappa = k2 / (k2 - k1)

        recovery_rates = np.zeros(num_credits)

        payment_dts = self._cds_contract._payment_dts
        num_payments = len(payment_dts)
        num_times = num_payments + 1

        beta_1 = sqrt(corr1)
        beta_2 = sqrt(corr2)
        beta_vector1 = np.zeros(num_credits)
        for bb in range(0, num_credits):
            beta_vector1[bb] = beta_1

        beta_vector2 = np.zeros(num_credits)
        for bb in range(0, num_credits):
            beta_vector2[bb] = beta_2

        q_vector = np.zeros(num_credits)
        qt1 = np.zeros(num_times)  # include 1.0
        qt2 = np.zeros(num_times)  # include 1.0

        tranche_times = np.zeros(num_times)
        tranche_surv_curve = np.zeros(num_times)

        tranche_times[0] = 0
        tranche_surv_curve[0] = 1.0
        qt1[0] = 1.0
        qt2[0] = 1.0

        for i in range(1, num_times):

            t = (payment_dts[i-1] - value_dt) / gDaysInYear

            for j in range(0, num_credits):

                issuer_curve = issuer_curves[j]
                vTimes = issuer_curve._times
                qRow = issuer_curve._values
                recovery_rates[j] = issuer_curve._recovery_rate
                q_vector[j] = interpolate(
                    t, vTimes, qRow, InterpTypes.FLAT_FWD_RATES.value)

            if model == FinLossDistributionBuilder.RECURSION:

                qt1[i] = tranche_surv_prob_recursion(
                    0.0, k1, num_credits, q_vector, recovery_rates,
                    beta_vector1, num_points)

                qt2[i] = tranche_surv_prob_recursion(
                    0.0, k2, num_credits, q_vector, recovery_rates,
                    beta_vector2, num_points)

            elif model == FinLossDistributionBuilder.ADJUSTED_BINOMIAL:

                qt1[i] = tranche_surv_prob_adj_binomial(
                    0.0, k1, num_credits, q_vector, recovery_rates,
                    beta_vector1, num_points)

                qt2[i] = tranche_surv_prob_adj_binomial(
                    0.0, k2, num_credits, q_vector, recovery_rates,
                    beta_vector2, num_points)

            elif model == FinLossDistributionBuilder.GAUSSIAN:

                qt1[i] = tranch_surv_prob_gaussian(0.0, k1, num_credits,
                                                   q_vector, recovery_rates,
                                                   beta_vector1, num_points)

                qt2[i] = tranch_surv_prob_gaussian(0.0, k2, num_credits,
                                                   q_vector, recovery_rates,
                                                   beta_vector2, num_points)

            elif model == FinLossDistributionBuilder.LHP:

                qt1[i] = tr_surv_prob_lhp(0.0, k1, num_credits, 
                                          q_vector, recovery_rates, beta_1)

                qt2[i] = tr_surv_prob_lhp(0.0, k2, num_credits, 
                                          q_vector, recovery_rates, beta_2)

            else:
                raise FinError(
                    "Unknown model type only full and AdjBinomial allowed")

            if qt1[i] > qt1[i - 1]:
                raise FinError(
                    "Tranche K1 survival probabilities not decreasing.")

            if qt2[i] > qt2[i - 1]:
                raise FinError(
                    "Tranche K2 survival probabilities not decreasing.")

            tranche_surv_curve[i] = kappa * qt2[i] + (1.0 - kappa) * qt1[i]
            tranche_times[i] = t

        curve_recovery = 0.0  # For tranches only
        libor_curve = issuer_curves[0]._libor_curve
        tranche_curve = CDSCurve(
            value_dt, [], libor_curve, curve_recovery)
        tranche_curve._times = tranche_times
        tranche_curve._values = tranche_surv_curve

        protLegPV = self._cds_contract.protection_leg_pv(
            value_dt, tranche_curve, curve_recovery)
        risky_pv01 = self._cds_contract.risky_pv01(
            value_dt, tranche_curve)['clean_rpv01']

        mtm = self._notional * (protLegPV - upfront - risky_pv01 * running_cpn)

        if not self._long_protection:
            mtm *= -1.0

        tranche_output = np.zeros(4)
        tranche_output[0] = mtm
        tranche_output[1] = risky_pv01 * self._notional * running_cpn
        tranche_output[2] = protLegPV * self._notional
        tranche_output[3] = protLegPV / risky_pv01

        return tranche_output

###############################################################################
