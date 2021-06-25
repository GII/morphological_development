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
