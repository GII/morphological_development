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

from config.experiment_data import ExperimentData


class OctopodExperimentData(ExperimentData):
    def set_output_range(self, arm_range, leg_range):
        self.output_range = [
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
            arm_range[0],
            arm_range[1],
            leg_range[0],
            leg_range[1],
        ]

    def denormalize_outputs(self, out_data):
        """Denormalize the output given by the NN."""
        sig_sup = 1.0
        sig_inf = 0.0
        #          0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
        ang_inf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ang_sup = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        ang_inf[0] = self.output_range[0]
        ang_sup[0] = self.output_range[1]
        ang_inf[1] = self.output_range[2]
        ang_sup[1] = self.output_range[3]
        ang_inf[2] = self.output_range[4]
        ang_sup[2] = self.output_range[5]
        ang_inf[3] = self.output_range[6]
        ang_sup[3] = self.output_range[7]
        ang_inf[4] = self.output_range[8]
        ang_sup[4] = self.output_range[9]
        ang_inf[5] = self.output_range[10]
        ang_sup[5] = self.output_range[11]
        ang_inf[6] = self.output_range[12]
        ang_sup[6] = self.output_range[13]
        ang_inf[7] = self.output_range[14]
        ang_sup[7] = self.output_range[15]
        ang_inf[8] = self.output_range[16]
        ang_sup[8] = self.output_range[17]
        ang_inf[9] = self.output_range[18]
        ang_sup[9] = self.output_range[19]
        ang_inf[10] = self.output_range[20]
        ang_sup[10] = self.output_range[21]
        ang_inf[11] = self.output_range[22]
        ang_sup[11] = self.output_range[23]
        ang_inf[12] = self.output_range[24]
        ang_sup[12] = self.output_range[25]
        ang_inf[13] = self.output_range[26]
        ang_sup[13] = self.output_range[27]
        ang_inf[14] = self.output_range[28]
        ang_sup[14] = self.output_range[29]
        ang_inf[15] = self.output_range[30]
        ang_sup[15] = self.output_range[31]

        aux = [
            ((((out_data[n] - sig_inf) * (ang_sup[n] - ang_inf[n])) / (sig_sup - sig_inf)) + ang_inf[n])
            for n in range(0, len(out_data))
        ]
        return aux
