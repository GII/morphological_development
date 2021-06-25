from config.evolution_config import EvolutionConfig
import MultiNEAT as NEAT
import copy as cp


class EvolutionConfigGrowth(EvolutionConfig):
    """This class contains the evolution parameter settings"""

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

    def set_NEAT_parameters(self, populationSize):
        # Configuration parameters of the NEAT algorithm
        params = NEAT.Parameters()

        # Basic parameters
        params.PopulationSize = populationSize
        params.DynamicCompatibility = True
        params.MinSpecies = 2
        params.MaxSpecies = 7
        params.InnovationsForever = True

        # GA Parameters
        params.YoungAgeTreshold = 5
        params.YoungAgeFitnessBoost = 1.0
        params.SpeciesDropoffAge = 50
        params.StagnationDelta = 0.0
        params.OldAgeTreshold = 30
        params.OldAgePenalty = 1.0
        params.KillWorstAge = 40
        params.SurvivalRate = 0.3
        params.CrossoverRate = 0.6
        params.KillWorstSpeciesEach = 20
        params.OverallMutationRate = 0.1
        params.MultipointCrossoverRate = 0.5
        params.RouletteWheelSelection = False
        params.InterspeciesCrossoverRate = 0.001
        params.DetectCompetetiveCoevolutionStagnation = True

        # Structural Mutation parameters
        params.RecurrentProb = 0.1
        params.SplitRecurrent = True
        params.MutateAddLinkProb = 0.5
        params.RecurrentLoopProb = 0.01
        params.MutateRemLinkProb = 0.01
        params.MutateAddNeuronProb = 0.5
        params.SplitLoopedRecurrent = False
        params.MutateAddLinkFromBiasProb = 0.0
        params.MutateRemSimpleNeuronProb = 0.0

        # Parameter Mutation parameters
        params.MutateWeightsProb = 0.5
        params.MutateWeightsSevereProb = 0.1
        params.WeightMutationRate = 0.9
        params.WeightMutationMaxPower = 1.0
        params.WeightReplacementMaxPower = 1.0
        params.MutateActivationAProb = 0.0
        params.MutateActivationBProb = 0.0
        params.ActivationAMutationMaxPower = 0.0
        params.ActivationBMutationMaxPower = 0.0
        params.TimeConstantMutationMaxPower = 0.0
        params.BiasMutationMaxPower = 1.0
        params.MutateNeuronTimeConstantsProb = 0.0
        params.MutateNeuronBiasesProb = 0.1

        params.MaxWeight = 10.0
        params.MinNeuronBias = -10.0
        params.MaxNeuronBias = 10.0
        params.EliteFraction = 0.02

        params.ExcessCoeff = 1.0
        params.DisjointCoeff = 1.0
        params.BiasDiffCoeff = 2.0
        params.CompatTreshold = 2.0
        params.WeightDiffCoeff = 2.0
        params.ActivationADiffCoeff = 0.0
        params.ActivationBDiffCoeff = 0.0
        params.TimeConstantDiffCoeff = 0.0
        params.CompatTresholdModifier = 0.1
        params.ActivationFunctionDiffCoeff = 0.0
        params.CompatTreshChangeInterval_Generations = 1

        params.MinActivationA = 1.0
        params.MaxActivationA = 1.0

        params.MinActivationB = 0.0
        params.MaxActivationB = 0.0

        params.ActivationFunction_Tanh_Prob = 0.0
        params.ActivationFunction_SignedStep_Prob = 0.0
        params.ActivationFunction_SignedSigmoid_Prob = 0.0
        params.ActivationFunction_UnsignedSigmoid_Prob = 1.0

        return params
