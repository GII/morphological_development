#############################################################################
#
#    Copyright (C) 2020 Martín Naya
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU  General Public License
#    along with this program.  If not, see < http:#www.gnu.org/licenses/ >.
#
#    Contact info:
#
#    Martín Naya < martin.naya@udc.es >
#############################################################################

from robot.joint_handler import JointHandler


class OctopodJointHandler(JointHandler):
    """Class to operate with the handlers to operate with an octopod robot."""

    def __init__(self, sim):
        super().__init__(sim)
        self.joint_number = 16
        self.final_pos_x = -0.3
        self.jd1a = 0
        self.jd1l = 0
        self.jd1e = 0
        self.jd2a = 0
        self.jd2l = 0
        self.jd2e = 0
        self.jd3a = 0
        self.jd3l = 0
        self.jd3e = 0
        self.jd4a = 0
        self.jd4l = 0
        self.jd4e = 0
        self.ji1a = 0
        self.ji1l = 0
        self.ji1e = 0
        self.ji2a = 0
        self.ji2l = 0
        self.ji2e = 0
        self.ji3a = 0
        self.ji3l = 0
        self.ji3e = 0
        self.ji4a = 0
        self.ji4l = 0
        self.ji4e = 0
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
        self.jd4a = self.sim.get_object_handle("arm_joint6")
        self.jd4l = self.sim.get_object_handle("leg_joint6")
        self.jd4e = self.sim.get_object_handle("leg1_ext1")

        self.ji1a = self.sim.get_object_handle("arm_joint3")
        self.ji1l = self.sim.get_object_handle("leg_joint3")
        self.ji1e = self.sim.get_object_handle("leg3_ext")
        self.ji2a = self.sim.get_object_handle("arm_joint4")
        self.ji2l = self.sim.get_object_handle("leg_joint4")
        self.ji2e = self.sim.get_object_handle("leg4_ext")
        self.ji3a = self.sim.get_object_handle("arm_joint5")
        self.ji3l = self.sim.get_object_handle("leg_joint5")
        self.ji3e = self.sim.get_object_handle("leg4_ext0")
        self.ji4a = self.sim.get_object_handle("arm_joint7")
        self.ji4l = self.sim.get_object_handle("leg_joint7")
        self.ji4e = self.sim.get_object_handle("leg4_ext1")
        # Head
        self.head = self.sim.get_object_handle("head")

    def grow_legs(self, finalLength):
        self.sim.set_joint_target_position(self.jd1e[1], finalLength)
        self.sim.set_joint_target_position(self.jd2e[1], finalLength)
        self.sim.set_joint_target_position(self.jd3e[1], finalLength)
        self.sim.set_joint_target_position(self.jd4e[1], finalLength)
        self.sim.set_joint_target_position(self.ji1e[1], finalLength)
        self.sim.set_joint_target_position(self.ji2e[1], finalLength)
        self.sim.set_joint_target_position(self.ji3e[1], finalLength)
        self.sim.set_joint_target_position(self.ji4e[1], finalLength)

        self.sim.set_joint_position(self.jd1e[1], finalLength)
        self.sim.set_joint_position(self.jd2e[1], finalLength)
        self.sim.set_joint_position(self.jd3e[1], finalLength)
        self.sim.set_joint_position(self.jd4e[1], finalLength)
        self.sim.set_joint_position(self.ji1e[1], finalLength)
        self.sim.set_joint_position(self.ji2e[1], finalLength)
        self.sim.set_joint_position(self.ji3e[1], finalLength)
        self.sim.set_joint_position(self.ji4e[1], finalLength)

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
