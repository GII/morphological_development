from config.experiment_data import ExperimentData
import copy as cp


class Quad8DOFRomExperimentData(ExperimentData):
    def set_output_range(self, arm_range, leg_range, angle_offset):
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
        ]
        self.angle_offset = [
            cp.deepcopy(arm_range[0] * angle_offset),
            cp.deepcopy(arm_range[1] * angle_offset),
            cp.deepcopy(leg_range[0] * angle_offset),
            cp.deepcopy(leg_range[1] * angle_offset),
            cp.deepcopy(arm_range[0] * angle_offset),
            cp.deepcopy(arm_range[1] * angle_offset),
            cp.deepcopy(leg_range[0] * angle_offset),
            cp.deepcopy(leg_range[1] * angle_offset),
            cp.deepcopy(arm_range[0] * angle_offset),
            cp.deepcopy(arm_range[1] * angle_offset),
            cp.deepcopy(leg_range[0] * angle_offset),
            cp.deepcopy(leg_range[1] * angle_offset),
            cp.deepcopy(arm_range[0] * angle_offset),
            cp.deepcopy(arm_range[1] * angle_offset),
            cp.deepcopy(leg_range[0] * angle_offset),
            cp.deepcopy(leg_range[1] * angle_offset),
        ]

    def denormalize_outputs(self, out_data):
        """Denormalize the output given by the NN."""
        sig_sup = 1.0
        sig_inf = 0.0

        #          0  1  2  3  4  5  6  7
        ang_inf = [0, 0, 0, 0, 0, 0, 0, 0]
        ang_sup = [0, 0, 0, 0, 0, 0, 0, 0]

        triggen = 60
        if self.contGen < triggen:
            orange = [
                (self.angle_offset[n] + ((self.output_range[n] - self.angle_offset[n]) / triggen) * self.contGen)
                for n in range(0, len(self.output_range))
            ]
        else:
            orange = self.output_range

        ang_inf[0] = orange[0]
        ang_sup[0] = orange[1]
        ang_inf[1] = orange[2]
        ang_sup[1] = orange[3]
        ang_inf[2] = orange[4]
        ang_sup[2] = orange[5]
        ang_inf[3] = orange[6]
        ang_sup[3] = orange[7]
        ang_inf[4] = orange[8]
        ang_sup[4] = orange[9]
        ang_inf[5] = orange[10]
        ang_sup[5] = orange[11]
        ang_inf[6] = orange[12]
        ang_sup[6] = orange[13]
        ang_inf[7] = orange[14]
        ang_sup[7] = orange[15]

        aux = [
            ((((out_data[n] - sig_inf) * (ang_sup[n] - ang_inf[n])) / (sig_sup - sig_inf)) + ang_inf[n])
            for n in range(0, len(out_data))
        ]

        return aux
