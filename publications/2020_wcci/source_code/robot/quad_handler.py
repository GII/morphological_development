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
