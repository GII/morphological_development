from robot.quad_handler import QuadHandler


class Quad16DOFJointHandler(QuadHandler):
    """
    Class to operate with the handlers of the different joints and shapes of the robot in V-REP.
    """

    def __init__(self, sim):
        super().__init__(sim)
        self.joint_number = 16
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
        # Right front
        self.jd1a = self.sim.get_object_handle("arm_joint0")
        self.jd2a = self.sim.get_object_handle("arm_joint2")
        self.jd1l = self.sim.get_object_handle("leg_joint0")
        self.jd2l = self.sim.get_object_handle("leg_joint2")
        self.jd1e = self.sim.get_object_handle("leg0_ext")

        # Right back
        self.jd3a = self.sim.get_object_handle("arm_joint1")
        self.jd4a = self.sim.get_object_handle("arm_joint5")
        self.jd3l = self.sim.get_object_handle("leg_joint1")
        self.jd4l = self.sim.get_object_handle("leg_joint7")
        self.jd3e = self.sim.get_object_handle("leg1_ext")

        # Left front
        self.ji1a = self.sim.get_object_handle("arm_joint3")
        self.ji2a = self.sim.get_object_handle("arm_joint7")
        self.ji1l = self.sim.get_object_handle("leg_joint3")
        self.ji2l = self.sim.get_object_handle("leg_joint5")
        self.ji1e = self.sim.get_object_handle("leg3_ext")

        # Left back
        self.ji3a = self.sim.get_object_handle("arm_joint4")
        self.ji4a = self.sim.get_object_handle("arm_joint6")
        self.ji3l = self.sim.get_object_handle("leg_joint4")
        self.ji4l = self.sim.get_object_handle("leg_joint6")
        self.ji3e = self.sim.get_object_handle("leg4_ext")

        # Head
        self.head = self.sim.get_object_handle("head")

    def move_joints_to_position(self, final_angle):
        """Move the joints of the robot to the target position."""
        self.sim.set_joint_target_position(self.jd1a[1], final_angle[0])
        self.sim.set_joint_target_position(self.jd1l[1], final_angle[1])
        self.sim.set_joint_target_position(self.jd2a[1], final_angle[2])
        self.sim.set_joint_target_position(self.jd2l[1], final_angle[3])
        self.sim.set_joint_target_position(self.jd3a[1], final_angle[4])
        self.sim.set_joint_target_position(self.jd3l[1], final_angle[5])
        self.sim.set_joint_target_position(self.jd4a[1], final_angle[6])
        self.sim.set_joint_target_position(self.jd4l[1], final_angle[7])
        self.sim.set_joint_target_position(self.ji1a[1], final_angle[8])
        self.sim.set_joint_target_position(self.ji1l[1], final_angle[9])
        self.sim.set_joint_target_position(self.ji2a[1], final_angle[10])
        self.sim.set_joint_target_position(self.ji2l[1], final_angle[11])
        self.sim.set_joint_target_position(self.ji3a[1], final_angle[12])
        self.sim.set_joint_target_position(self.ji3l[1], final_angle[13])
        self.sim.set_joint_target_position(self.ji4a[1], final_angle[14])
        self.sim.set_joint_target_position(self.ji4l[1], final_angle[15])

        for _ in range(2):
            self.sim.sync_trigger()