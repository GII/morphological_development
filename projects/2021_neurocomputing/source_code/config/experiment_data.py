import pickle


class ExperimentData(object):
    """This class represents the relevant information obtained during the learning process."""

    def __init__(self, generations):
        self.contGen = 0
        self.directory = ""
        self.experiment = 0
        self.inputs_range = 0
        self.output_range = 0
        self.angle_offset = 0
        self.full_generations = 0

        self.median_value = [0 for n in range(0, generations)]
        self.average_value = [0 for n in range(0, generations)]
        self.cuartil_25 = [0 for n in range(0, generations)]
        self.cuartil_75 = [0 for n in range(0, generations)]
        self.max_fitness_value = [0 for n in range(0, generations)]

    def saveStatistics(self):
        """Serialize saved data to a file."""
        saveData = [self.average_value, self.median_value, self.max_fitness_value]

        text01 = self.directory + "/" + "MeanMedian_Data_array_" + str(0) + ".txt"
        file = open(text01, "wb")
        pickle.dump(saveData, file)
        file.close()
