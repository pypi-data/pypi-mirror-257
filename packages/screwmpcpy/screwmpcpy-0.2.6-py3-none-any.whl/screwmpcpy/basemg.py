"""Base motion generation module."""
from __future__ import annotations

import numpy as np
from dqrobotics import DQ, exp, log, pow, vec6

from .screwmpc import BOUND, ScrewMPC


def _get_twist(current_dq: np.ndarray, goal_dq: np.ndarray, alpha: float) -> np.ndarray:
    delta_dq = current_dq.inv() * goal_dq
    next_point = current_dq * pow(delta_dq, alpha)
    return vec6(log(next_point * current_dq.conj()))


class BaseMotionGenerator(ScrewMPC):
    r"""Base Motion generator for Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.

    :param n_p: Prediction horizon :math:`n_p`.
    :type n_p: int
    :param n_c: Control horizon :math:`n_c`.
    :type n_c: int
    :param q_mpc: :math:`\boldsymbol{Q}=q_{mpc}\boldsymbol{I}`.
    :type q_mpc: float
    :param r_mpc: :math:`\boldsymbol{R}=r_{mpc}\boldsymbol{I}`.
    :type r_mpc: float
    :param lu_bound_vel: lower- and upper bound for velocity.
    :type lu_bound_vel: BOUND
    :param lu_bound_acc: lower- and upper bound for accerlation.
    :type lu_bound_acc: BOUND
    :param lu_bound_jerk: lower- and upper bound for jerk.
    :type lu_bound_jerk: BOUND
    :param sclerp: ScLERP interpolation for EE pose generatation,
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1.
    :raises ValueError: If sclerp :math:`\not\in\left(0, 1\right]`.
    """

    def __init__(
        self,
        n_p: int,
        n_c: int,
        q_mpc: float,
        r_mpc: float,
        lu_bound_vel: BOUND,
        lu_bound_acc: BOUND,
        lu_bound_jerk: BOUND,
        sclerp: float = 0.1,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk
        )

        # setup internal states and kinematics
        self._mpc_state = np.zeros((18,))
        self._u_state = np.zeros((6,))

        if not 0 < sclerp <= 1:
            msg = "Select sclerp between 0 and 1!"
            raise ValueError(msg)

        self._sclerp = sclerp

    def step(self, current_dq: DQ, goal_dq: DQ) -> tuple[DQ, DQ]:
        """Perform one step for motion generation.

        :param current_dq: Current pose represented as Dual Quaternion.
        :type current_dq: DQ
        :param goal_dq: Goal pose represented as Dual Quaternion.
        :type goal_dq: DQ
        :return: Cartesian pose error represented and smooth trajectory.
        :rtype: tuple[DQ, DQ]
        """

        # perform optimization
        desired_twist = _get_twist(current_dq, goal_dq, self._sclerp)
        du = super().solve(desired_twist, self._u_state, self._mpc_state)[:6]

        # calculate the errors and compute commanded dq
        twist_out = DQ(self.c_matrix @ self._mpc_state)
        smooth_traj = exp(twist_out) * current_dq
        error = DQ(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) - (
            current_dq.conj() * smooth_traj
        )

        # update necessary states
        self._mpc_state = self.a_matrix @ self._mpc_state + self.b_matrix @ du
        self._u_state += du

        return error, smooth_traj
