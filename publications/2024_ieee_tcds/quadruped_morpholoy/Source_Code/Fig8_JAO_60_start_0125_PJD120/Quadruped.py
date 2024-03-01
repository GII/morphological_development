import os
import sys
import pickle
import datetime
import argparse
import copy as cp
import numpy as np
import random as rd
import MultiNEAT as NEAT
import supportFile as sf

import multiprocessing

from MultiNEAT import EvaluateGenomeList_Serial
from MultiNEAT import GetGenomeList, ZipFitness

from zmqRemoteApi import RemoteAPIClient

# Setting the port number to the CoppeliaSim connection for running several independet experiments in the CESGA supercomputer (https://www.cesga.es/en/home-2/)
# At the same time, the port number is used as seed for generating random values.
cluster = True
if cluster == True:
    port_conexion = int(sys.argv[1])
    print ('Base Port:', port_conexion)
# Whether the CESGA is not used, select the port '23000' by default.
else:
    port_conexion = 23000

# Setting the values of the experimental parameters.
ang_off = 0.125
simSteps = 90           # Number of simulaton steps performed by the robot 
numEntries = 1          # Number of inputs to the NeuralNetwork
generations = 300       # Number of generations
populationSize = 50     # Size of the population

# Parameters of the sinusoidal function that consitutes the inputs of the NeuralNetwork. It is the motor patern generator of the robot.
A = 2.0
omega = 1.0

# Class for saving relevant data of the neuroevolutionary process.
datah = sf.saveData(generations)

# Classs to store the different handlers the robot needs to operate in the simulator. 
class handlers ():
    def __init__(self):
        self.jd1a = 0
        self.jd1l = 0
        self.jd1e = 0
        self.jd2a = 0
        self.jd2l = 0
        self.jd2e = 0
        self.jd3a = 0
        self.jd3l = 0
        self.jd3e = 0
        self.ji1a = 0
        self.ji1l = 0
        self.ji1e = 0
        self.ji2a = 0
        self.ji2l = 0
        self.ji2e = 0
        self.ji3a = 0
        self.ji3l = 0
        self.ji3e = 0
        self.head = 0

handler = handlers()

# Parameter configuration of the NEAT algortihm
params = NEAT.Parameters()
# Basic parameters
params.MinSpecies = 1
params.MaxSpecies = 3
params.InnovationsForever = True
params.DynamicCompatibility = True
params.PopulationSize = populationSize

# GA Parameters
params.KillWorstAge = 150
params.SurvivalRate = 0.2
params.CrossoverRate = 0.5
params.OldAgeTreshold = 50
params.OldAgePenalty = 1.0
params.YoungAgeTreshold = 5
params.StagnationDelta = 0.0
params.SpeciesDropoffAge = 75
params.KillWorstSpeciesEach = 100
params.OverallMutationRate = 0.1
params.YoungAgeFitnessBoost = 1.0
params.MultipointCrossoverRate = 0.4
params.RouletteWheelSelection = False
params.InterspeciesCrossoverRate = 0.001
params.DetectCompetetiveCoevolutionStagnation = True

# Structural Mutation parameters
params.RecurrentProb = 0.05
params.SplitRecurrent = True
params.MutateAddLinkProb = 0.2
params.RecurrentLoopProb = 0.01
params.MutateRemLinkProb = 0.01
params.MutateAddNeuronProb = 0.1
params.SplitLoopedRecurrent = False
params.MutateAddLinkFromBiasProb = 0.0
params.MutateRemSimpleNeuronProb = 0.0

# Parameter Mutation parameters
params.MaxWeight = 10.0
params.MaxNeuronBias = 10.0
params.EliteFraction = 0.01
params.MinNeuronBias = -10.0
params.MutateWeightsProb = 0.1
params.WeightMutationRate = 0.1
params.BiasMutationMaxPower = 1.0
params.MutateActivationAProb = 0.0
params.MutateActivationBProb = 0.0
params.MutateNeuronBiasesProb = 0.1
params.WeightMutationMaxPower = 1.0
params.MutateWeightsSevereProb = 0.1
params.WeightReplacementMaxPower = 1.0
params.ActivationAMutationMaxPower = 0.0
params.ActivationBMutationMaxPower = 0.0
params.TimeConstantMutationMaxPower = 0.0
params.MutateNeuronTimeConstantsProb = 0.0

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

# Function that load the robot in the scene at the beggining of each evaluation.
def loadRobot ():
    
    # Opening the connection with CoppeliaSim simulator
    # print('Program started')
    datah.client = RemoteAPIClient('localhost', port_conexion)
    datah.sim = datah.client.getObject('sim')
    
    # Setting the simulation mode for working in sinchronous mode. The simulation timming is controlled by the Python program and not by the simulation itselfs.
    datah.client.setStepping(True)

    # Set the length of the robot for each generation.
    
    # Section where all the handlers of the robot are obtained and stored in the class with their corresponding name.
    # Right side of the Quadruped
    # Get all handlers
    handler.jd1a = datah.sim.getObject("/arm_joint0")
    handler.jd1l = datah.sim.getObject("/leg_joint0")
    handler.jd1e = datah.sim.getObject("/leg0_ext")
    handler.jd3a = datah.sim.getObject("/arm_joint1")
    handler.jd3l = datah.sim.getObject("/leg_joint1")
    handler.jd3e = datah.sim.getObject("/leg1_ext")

    # Left side of the Quadruped
    handler.ji1a = datah.sim.getObject("/arm_joint3")
    handler.ji1l = datah.sim.getObject("/leg_joint3")
    handler.ji1e = datah.sim.getObject("/leg3_ext")
    handler.ji3a = datah.sim.getObject("/arm_joint4")
    handler.ji3l = datah.sim.getObject("/leg_joint4")
    handler.ji3e = datah.sim.getObject("/leg4_ext")
    handler.head = datah.sim.getObject("/head")
        
    # Starting the simulation in Synchronous mode. 
    datah.sim.startSimulation()


# Function where each genome of the population is evaluated, returning its fitness value.
def ev_single_genome(genome):
    
    # Load of the robot.
    loadRobot()

    # Bulding the NeuralNetwork configuration based on the information provided in the genome.
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)  
    
    # Loop for moving the robot "simSteps" times.
    for timeStep in range(0, simSteps):
        
        # Building the array of the input values to the NeuralNetwork.
        inputs_already_norm = []
        inputs_already_norm.append(A*np.sin(omega * timeStep))
        inputs_already_norm.append(1.0) 

        # Activation of the NeuralNetwork.
        net.Flush()
        net.Input(inputs_already_norm)
        for _ in range(2):
            net.Activate()
        net_out_std = net.Output()
        
        # Denormalization of the outputs of the NeuralNetwork.
        final_angle = sf.deNormalizeOuputs(net_out_std, datah)                

        # Updating of the postion of the quadruped's joints at each simulation time step.
        datah.sim.setJointTargetPosition(handler.jd1a, final_angle[0])
        datah.sim.setJointTargetPosition(handler.jd1l, final_angle[1])
        datah.sim.setJointTargetPosition(handler.jd3a, final_angle[2])
        datah.sim.setJointTargetPosition(handler.jd3l, final_angle[3])
        datah.sim.setJointTargetPosition(handler.ji1a, final_angle[4])
        datah.sim.setJointTargetPosition(handler.ji1l, final_angle[5])
        datah.sim.setJointTargetPosition(handler.ji3a, final_angle[6])
        datah.sim.setJointTargetPosition(handler.ji3l, final_angle[7])

        # Giving two time steps for the simulation
        for _ in range(2):
            datah.client.step()

    # Section for retrieving the distance traveled by the head of the NAO in the "x" direction.
    position = datah.sim.getObjectPosition(handler.head, datah.sim.handle_world)

    # Stoppping the simulation.
    datah.sim.stopSimulation()
    while datah.sim.getSimulationState()!=datah.sim.simulation_stopped:
        pass
    # print(position[0])
    
    return position[0]

# Function where the neuroevoluton process takes place.
def run_population_evolution (genIndex):
    # Configuration of the genome and population.
    inputsNeuron = numEntries + 1
    outputsNeuron = 8
    genome = NEAT.Genome(0, inputsNeuron, 0, outputsNeuron, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID,NEAT.ActivationFunction.UNSIGNED_SIGMOID, 1, params, 0)
    pop = NEAT.Population(genome, params, True, 1.0, genIndex)
    pop.RNG.Seed(port_conexion)

    # Variables to store the  best genomes of the population and its fitness value.
    evhist = []
    best_gs = []
    best_fit_ever = 0
    best_index_ever = 0
    datah.dev_stage = 3
    best_generation_ever = 0
    
    # Loop for evaluation the population during 300 generations.
    for generation in range(0, generations):
        datah.genome_counter = 0
        genome_list = NEAT.GetGenomeList(pop)
        fitness_list = EvaluateGenomeList_Serial(genome_list, ev_single_genome)
        NEAT.ZipFitness(genome_list, fitness_list)

        # Code for storing the best genome of each generation and its fitness value.
        best = max(fitness_list)
        best_index = fitness_list.index(max(fitness_list))
        evhist.append(best)
        best_genome_aux = pop.GetBestGenome()
        if best > best_fit_ever:
            sys.stdout.flush()
            best_gs.append(best_genome_aux)
            best_fit_ever = best
            best_index_ever = best_index
            best_generation_ever = generation
        else:
            pass

        
        # Section for saving relevant data into a file for further analysis.
        fit_index = fitness_list.index(max(fitness_list))
        datah.max_fitness_value[datah.contGen] = fitness_list[fit_index]
        datah.average_value[datah.contGen] = np.average(fitness_list)
        datah.median_value[datah.contGen] = np.median(fitness_list)
        sf.saveStatistics(datah)
        datah.contGen = cp.deepcopy(datah.contGen) + 1

        # Update of the neuroevolutionary process.
        pop.Epoch()
        print('Gen:', generation, 'Fit:', best, 'Mediana:', round(np.median(fitness_list),3), 'Media:', round(np.average(fitness_list),3), 'Std:', round(np.std(fitness_list),3))

    return (best_generation_ever, best_index_ever, best_gs[len(best_gs)-1], best_fit_ever)

# main function
def main():
    # Creating a directory where all the information of the learning process is stored.
    directory00 = '4legged_p' + str(populationSize) + '_gen' + str(generations) + '_' + str(port_conexion)
    datah.directory = directory00
    try:
        os.makedirs(directory00)
    except:
        pass

    rd.seed(port_conexion)

    # Range of Morion of the different quadruped joints in radians.
    coef = np.pi/180.0
    datah.output_range = [-90.0*coef, 90.0*coef, -150.0*coef, 30.0*coef, -90.0*coef, 90.0*coef, -150.0*coef, 30.0*coef, -90.0*coef, 90.0*coef, -150.0*coef, 30.0*coef, -90.0*coef, 90.0*coef, -150.0*coef, 30.0*coef]
    
    datah.ang_reduced = [datah.output_range[0] * ang_off, datah.output_range[1] * ang_off, datah.output_range[2] * ang_off, datah.output_range[3] * ang_off, datah.output_range[4] * ang_off, datah.output_range[5] * ang_off, datah.output_range[6] * ang_off, datah.output_range[7] * ang_off, datah.output_range[8] * ang_off, datah.output_range[9] * ang_off, datah.output_range[10] * ang_off, datah.output_range[11] * ang_off, datah.output_range[12] * ang_off, datah.output_range[13] * ang_off, datah.output_range[14] * ang_off, datah.output_range[15] * ang_off]

    best_individual = run_population_evolution(port_conexion)
    winner_genome = best_individual[2]

    text01 = datah.directory + '/' + 'winner_genome_' + str(301) + '.txt'
    file = open(text01, 'wb')
    pickle.dump(winner_genome, file)
    file.close()


if __name__ == '__main__':
    main()
