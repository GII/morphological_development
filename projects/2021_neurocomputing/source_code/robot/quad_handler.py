from robot.joint_handler import JointHandler


class QuadHandler(JointHandler):
    """
    This class represents the handlers to operate with a quad robot.

    It contains the properties and methods the quad robots have in common,
    regardless of the number of joints the robot has.
    """

    def __init__(self, sim):
        super().__init__(sim)
        self.final_pos_x = 0.0

    def grow_legs(self, finalLength):
        """Grow robot's legs to final length"""
        super().grow_legs(finalLength)
        self.sim.set_joint_target_position(self.jd1e[1], finalLength)
        self.sim.set_joint_target_position(self.jd3e[1], finalLength)
        self.sim.set_joint_target_position(self.ji1e[1], finalLength)
        self.sim.set_joint_target_position(self.ji3e[1], finalLength)

        self.sim.set_joint_position(self.jd1e[1], finalLength)
        self.sim.set_joint_position(self.jd3e[1], finalLength)
        self.sim.set_joint_position(self.ji1e[1], finalLength)
        self.sim.set_joint_position(self.ji3e[1], finalLength)
