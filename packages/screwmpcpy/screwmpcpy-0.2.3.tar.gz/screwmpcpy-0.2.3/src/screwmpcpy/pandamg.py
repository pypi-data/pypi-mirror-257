from __future__ import annotations

import numpy as np
import qpsolvers as qp
import roboticstoolbox as rtb
from dqrobotics import C8, DQ, haminus8, vec8
from dqrobotics.robots import FrankaEmikaPandaRobot
from dqrobotics.utils.DQ_LinearAlgebra import pinv

from .basemg import BaseMotionGenerator
from .screwmpc import BOUND


class PandaScrewMotionGenerator(BaseMotionGenerator):
    r"""Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.

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
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
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
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._kin = FrankaEmikaPandaRobot.kinematics()
        self._dqerror: DQ = None

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """

        x_current = self._kin.fkm(q_robot)
        error, smooth_traj = super().step(x_current, goal)
        dot_x = vec8(error)
        j_pose = np.linalg.multi_dot(
            [haminus8(smooth_traj), C8(), self._kin.pose_jacobian(q_robot)]
        )
        self._dqerror = error
        return pinv(j_pose) @ dot_x

    @property
    def dqerror(self) -> DQ:
        """Get the DQ error of the last optimization step.

        :return: The dual quaternion error of the last optimization step
        :rtype: DQ
        """
        return self._dqerror


class PandaScrewMpMotionGenerator(PandaScrewMotionGenerator):
    r"""Motion generator for Panda robot using Dual Quaternions, while considering jerk-, acceleration- and velocity constraints.
        Further, the manipulability of the robot is considered.

    :param n_p: Prediction horizon :math:`n_p`.
    :type n_p: int
    :param n_c: Control horizon :math:`n_c`.
    :type n_c: int
    :param q_mpc: :math:`\boldsymbol{Q}=q_{mpc}\boldsymbol{I}`.
    :type q_mpc: float
    :param r_mpc: :math:`\boldsymbol{R}=r_{mpc}\boldsymbol{I}.
    :type r_mpc: float
    :param lu_bound_vel: lower- and upper bound for velocity.
    :type lu_bound_vel: BOUND
    :param lu_bound_acc: lower- and upper bound for accerlation.
    :type lu_bound_acc: BOUND
    :param lu_bound_jerk: lower- and upper bound for jerk.
    :type lu_bound_jerk: BOUND
    :param sclerp: ScLERP interpolation for EE pose generatation,
        must lie in :math:`\left(0, 1\right]`, defaults to 0.1
    :type sclerp: float, optional
    :param slack: slack variable for manipulability maximization, defaults to 10.0
    :type slack: float, optional.
    :param gain: gain for manipulabiliy quadratic program, defaults to 0.01.
    :type gain: float, optional.
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
        slack: float = 10.0,
        gain: float = 0.01,
    ) -> None:
        super().__init__(
            n_p, n_c, q_mpc, r_mpc, lu_bound_vel, lu_bound_acc, lu_bound_jerk, sclerp
        )

        self._panda_rtb = rtb.models.Panda()
        self._gain = gain
        self._m_upper = np.zeros((13,))
        self._m_upper[:7] = self._panda_rtb.qdlim[:7]
        self._m_upper[7:] = slack
        self._m_lower = -self._m_upper.copy()

    def step(self, q_robot: np.ndarray, goal: DQ) -> np.ndarray:
        r"""Perform one step for motion generation.

        :param q_robot: robot joint angles :math:`q \in \mathbb{R}^7`.
        :type q_robot: np.ndarray
        :param goal: Goal pose represented as Dual Quaternion.
        :type goal: DQ
        :raises ValueError: If the the number of arguments mismatch.
        :return: commanded joint velocity :math:`\dot{\boldsymbol{q}} \in \mathbb{R}^7`.
        :rtype: np.ndarray
        """

        dq_desired = super().step(q_robot, goal)
        twist = self._panda_rtb.jacob0(q_robot) @ dq_desired
        a_eq = np.concatenate([self._panda_rtb.jacob0(q_robot), np.eye(6)], axis=-1)

        q_mat = np.eye(q_robot.shape[0] + 6)
        q_mat[: q_robot.shape[0], : q_robot.shape[0]] *= self._gain
        error_norm = np.linalg.norm(vec8(self.dqerror))
        q_mat[q_robot.shape[0] :, q_robot.shape[0] :] *= np.reciprocal(error_norm)

        c_vec = np.zeros((q_robot.shape[0] + 6,))
        j_m = np.squeeze(self._panda_rtb.jacobm(q_robot), axis=-1)
        # print(j_m)
        c_vec[: j_m.shape[0]] = -j_m

        dqout = qp.solve_qp(
            q_mat,
            c_vec,
            None,
            None,
            a_eq,
            twist,
            lb=self._m_lower,
            ub=self._m_upper,
            solver="daqp",
        )
        # print(dqout)
        return dqout[: q_robot.shape[0]]
