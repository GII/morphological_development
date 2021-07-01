from config.evolution_config import EvolutionConfig
import MultiNEAT as NEAT
import copy as cp


class EvolutionConfigRom(EvolutionConfig):
    """This class contains the evolution parameter settings for rom expermiments."""

    def __init__(self):
        super().__init__()
        self.maxLength = 0.075
        self.angle_offset = 0.5
