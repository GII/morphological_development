from robot.joint_handler import JointHandler


class HexapodJointHandler(JointHandler):
    """
    Class to operate with the handlers to operate with an hexapod robot
    """

    def __init__(self, sim):
        super().__init__(sim)
        self.joint_number = 12
        self.final_pos_x = -0.15
        self.jd1a = 0
        self.jd1l = 0
        self.jd1e = 0
        self.jd2a = 0
        self.jd2l = 0
        self.jd2e = 0
        self.jd3a = 0
        self.jd3l = 0
        self.jd3e = 0
        self.ji1a = 0
        self.ji1l = 0
        self.ji1e = 0
        self.ji2a = 0
        self.ji2l = 0
        self.ji2e = 0
        self.ji3a = 0
        self.ji3l = 0
        self.ji3e = 0
        self.head = 0

    def get_joint_handlers(self):
        """Get the needed handlers of the robot joints."""
        self.jd1a = self.sim.get_object_handle("arm_joint0")
        self.jd1l = self.sim.get_object_handle("leg_joint0")
        self.jd1e = self.sim.get_object_handle("leg0_ext")
        self.jd2a = self.sim.get_object_handle("arm_joint1")
        self.jd2l = self.sim.get_object_handle("leg_joint1")
        self.jd2e = self.sim.get_object_handle("leg1_ext")
        self.jd3a = self.sim.get_object_handle("arm_joint2")
        self.jd3l = self.sim.get_object_handle("leg_joint2")
        self.jd3e = self.sim.get_object_handle("leg1_ext0")

        self.ji1a = self.sim.get_object_handle("arm_joint3")
        self.ji1l = self.sim.get_object_handle("leg_joint3")
        self.ji1e = self.sim.get_object_handle("leg3_ext")
        self.ji2a = self.sim.get_object_handle("arm_joint4")
        self.ji2l = self.sim.get_object_handle("leg_joint4")
        self.ji2e = self.sim.get_object_handle("leg4_ext")
        self.ji3a = self.sim.get_object_handle("arm_joint5")
        self.ji3l = self.sim.get_object_handle("leg_joint5")
        self.ji3e = self.sim.get_object_handle("leg4_ext0")
        self.head = self.sim.get_object_handle("head")

    def grow_legs(self, finalLength):
        self.sim.set_joint_target_position(self.jd1e[1], finalLength)
        self.sim.set_joint_target_position(self.jd2e[1], finalLength)
        self.sim.set_joint_target_position(self.jd3e[1], finalLength)
        self.sim.set_joint_target_position(self.ji1e[1], finalLength)
        self.sim.set_joint_target_position(self.ji2e[1], finalLength)
        self.sim.set_joint_target_position(self.ji3e[1], finalLength)
        self.sim.set_joint_position(self.jd1e[1], finalLength)
        self.sim.set_joint_position(self.jd2e[1], finalLength)
        self.sim.set_joint_position(self.jd3e[1], finalLength)
        self.sim.set_joint_position(self.ji1e[1], finalLength)
        self.sim.set_joint_position(self.ji2e[1], finalLength)
        self.sim.set_joint_position(self.ji3e[1], finalLength)

    def move_joints_to_position(self, final_angle):
        """Move the joints of the robot to the target position."""
        self.sim.set_joint_target_position(self.jd1a[1], final_angle[0])
        self.sim.set_joint_target_position(self.jd1l[1], final_angle[1])
        self.sim.set_joint_target_position(self.jd2a[1], final_angle[2])
        self.sim.set_joint_target_position(self.jd2l[1], final_angle[3])
        self.sim.set_joint_target_position(self.jd3a[1], final_angle[4])
        self.sim.set_joint_target_position(self.jd3l[1], final_angle[5])
        self.sim.set_joint_target_position(self.ji1a[1], final_angle[6])
        self.sim.set_joint_target_position(self.ji1l[1], final_angle[7])
        self.sim.set_joint_target_position(self.ji2a[1], final_angle[8])
        self.sim.set_joint_target_position(self.ji2l[1], final_angle[9])
        self.sim.set_joint_target_position(self.ji3a[1], final_angle[10])
        self.sim.set_joint_target_position(self.ji3l[1], final_angle[11])

        for _ in range(2):
            self.sim.sync_trigger()
