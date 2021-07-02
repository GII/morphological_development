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

import MultiNEAT as NEAT


class EvolutionConfig(object):
    """This class contains the evolution parameter settings"""

    def __init__(self):
        self.result_folder = "output"
        self.test_folder = "testdata"
        self.secondsTime = 30
        self.numEntries = 1
        self.generations = 2  # 300
        self.test_generations = 300
        self.populationSize = 2  # 50
        self.startExpe = 0
        self.experiments = 1

        self.A = 2.0
        self.omega = 1.0

        self.max_arm = 90.0
        self.min_arm = -90.0
        self.max_leg = 90.0
        self.min_leg = -90.0

        self.neat_params = self.set_NEAT_parameters(self.populationSize)

    def set_NEAT_parameters(self, populationSize):
        """Set configuration parameters of the NEAT algorithm.

        :param populationSize: the size of the population for the evolution
        :type populationSize: integer

        :return: The parameters for the NEAT algorithm.
        :rtype: NEAT.Parameters
        """

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
