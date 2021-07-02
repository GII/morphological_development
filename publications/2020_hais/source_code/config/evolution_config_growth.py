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


from config.evolution_config import EvolutionConfig
import MultiNEAT as NEAT
import copy as cp


class EvolutionConfigGrowth(EvolutionConfig):
    """This class contains the evolution parameter settings for growth expermiments."""

    def __init__(self):
        super().__init__()
        self.startPos = 0.089
        self.maxLength = 0.075
        self.finalLength = 0
        self.finalPos = []

    def set_final_pos(self, finalpos_x):
        self.finalPos = [finalpos_x, 0.0, cp.deepcopy(self.startPos + self.finalLength)]

    def set_final_length(self, contGen):
        """Set the legs length for the 'contGen' generation.

        This method calculates how long the robot's legs should be in 'contGen' generation
        (how much the robot has grown).

        :param contGen: the generation number
        :type contGen: integer
        """
        triglength = 60.0
        if contGen < triglength:
            self.finalLength = self.maxLength * (float(contGen) / triglength)
        else:
            self.finalLength = self.maxLength
