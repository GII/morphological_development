from config.experiment_data import ExperimentData


class HexapodExperimentData(ExperimentData):
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
        ]

    def denormalize_outputs(self, out_data):
        """Denormalize the output given by the NN."""

        sig_sup = 1.0
        sig_inf = 0.0

        #          0  1  2  3  4  5  6  7  8  9 10 11
        ang_inf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ang_sup = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

        aux = [
            ((((out_data[n] - sig_inf) * (ang_sup[n] - ang_inf[n])) / (sig_sup - sig_inf)) + ang_inf[n])
            for n in range(0, len(out_data))
        ]

        return aux
