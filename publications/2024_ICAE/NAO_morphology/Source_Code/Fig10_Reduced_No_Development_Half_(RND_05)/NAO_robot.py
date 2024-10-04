import os
import sys
import pickle
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

D = 0.5
max_distance = 2.75
fall_penalization = 15.0

tiempoSeg = 180
numEntradas = 3 
generations = 300
populationSize = 50

A = 2.0
omega = 0.1 * np.pi

datah = sf.saveData(generations)

class handlers ():
    def __init__(self):
        self.NAO_m_joint1 = 0   # HeadYaw4
        self.NAO_m_joint2 = 0   # HeadPitch
        self.NAO_m_joint3 = 0   # LHipYawPitch3
        self.NAO_m_joint4 = 0   # LHipRoll3
        self.NAO_m_joint5 = 0   # LHipPitch3
        self.NAO_m_joint6 = 0   # L_ext_1
        self.NAO_m_joint7 = 0   # LKneePitch3
        self.NAO_m_joint8 = 0   # L_ext_2
        self.NAO_m_joint9 = 0   # LAnklePitch3
        self.NAO_m_joint10 = 0  # LAnkleRoll3
        self.NAO_m_joint11 = 0  # RHipYawPitch3
        self.NAO_m_joint12 = 0  # RHipRoll3
        self.NAO_m_joint13 = 0  # RHipPitch3
        self.NAO_m_joint14 = 0  # R_ext_1
        self.NAO_m_joint15 = 0  # RKneePitch3
        self.NAO_m_joint16 = 0  # R_ext_2
        self.NAO_m_joint17 = 0  # RAnklePitch3
        self.NAO_m_joint18 = 0  # RAnkleRoll3
        self.NAO_m_joint19 = 0  # LShoulderPitch3
        self.NAO_m_joint20 = 0  # RShoulderPitch3
        self.head = 0

class specie():
    def __init__(self):
        self.tamano = 0
        self.ID = 0

handler = handlers()

# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
def EvaluateGenomeList_Parallel(genome_list, evaluator):
    port = [(port_conexion+2*n) for n in range(0, populationSize)]
    inputs = []
    for n in range(0, populationSize):
        inputs.append([genome_list[n], port[n]])
        
    if datah.contGen == 0:
        cwd = os.getcwd()
        sh_file = cwd + "/parallel_run_baseScript.sh"
        for num_gen in range(len(genome_list)):
            arg1 = str(port[num_gen])
            os.system("sh " + sh_file + " " + arg1 + " " + cwd)
    else:
        pass

    with multiprocessing.Pool(processes=populationSize) as pool:
        fitness_list = pool.map(evaluator, inputs)

    return fitness_list
# ------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def loadRobot (port_con):

    # Opening the connection with CoppeliaSim simulator
    # print('Program started')
    datah.client = RemoteAPIClient('localhost', port_con)
    datah.sim = datah.client.getObject('sim')

    # Setting the simulation mode for working in sinchronous mode. The simulation timming is controlled by the Python program and not by the simulation itselfs.
    datah.client.setStepping(True)

    # Section where all the handlers of the robot are obtained and stored in the class with their corresponding name.
    # Left
    handler.NAO_m_joint3 = datah.sim.getObject("/NAO_m_joint3")
    handler.NAO_m_joint4 = datah.sim.getObject("/NAO_m_joint4")
    handler.NAO_m_joint5 = datah.sim.getObject("/NAO_m_joint5")
    handler.NAO_m_joint7 = datah.sim.getObject("/NAO_m_joint7")
    handler.NAO_m_joint9 = datah.sim.getObject("/NAO_m_joint9")
    handler.NAO_m_joint10 = datah.sim.getObject("/NAO_m_joint10")
    # Right
    handler.NAO_m_joint11 = datah.sim.getObject("/NAO_m_joint11")
    handler.NAO_m_joint12 = datah.sim.getObject("/NAO_m_joint12")
    handler.NAO_m_joint13 = datah.sim.getObject("/NAO_m_joint13")
    handler.NAO_m_joint15 = datah.sim.getObject("/NAO_m_joint15")
    handler.NAO_m_joint17 = datah.sim.getObject("/NAO_m_joint17")
    handler.NAO_m_joint18 = datah.sim.getObject("/NAO_m_joint18")
    # Shoulders
    handler.NAO_m_joint19 = datah.sim.getObject("/NAO_m_joint19")
    handler.NAO_m_joint20 = datah.sim.getObject("/NAO_m_joint20")

    # Extension
    handler.NAO_m_joint6 = datah.sim.getObject("/NAO_m_joint6")
    handler.NAO_m_joint8 = datah.sim.getObject("/NAO_m_joint8")
    handler.NAO_m_joint14 = datah.sim.getObject("/NAO_m_joint14")
    handler.NAO_m_joint16 = datah.sim.getObject("/NAO_m_joint16")

    handler.head = datah.sim.getObject("/imported_part_16_sub0")

    # Starting the simulation in Synchronous mode. 
    datah.sim.startSimulation()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def ev_single_genome(various_inputs):
    
    # Load of the robot.
    loadRobot(various_inputs[1])

    # Bulding the NeuralNetwork configuration based on the information provided in the genome.
    net = NEAT.NeuralNetwork()
    various_inputs[0].BuildPhenotype(net)  

    aux_fitness = []
    early_trigger = False
    for timeStep in range(0, tiempoSeg):
        inputs_already_norm = []
        inputs_already_norm.append(A*np.sin(omega * timeStep))
        inputs_already_norm.append(A*np.sin(omega * timeStep + np.pi/2.0))
        inputs_already_norm.append(A*np.sin(omega * timeStep + np.pi/3.0))
        inputs_already_norm.append(1.0)     

        net.Flush()
        net.Input(inputs_already_norm)
        for _ in range(2):
            net.Activate()
        net_out_std = net.Output()
        angulo_final = sf.normalizeOuputs(net_out_std, datah)            

        datah.sim.setJointTargetPosition(handler.NAO_m_joint3,  angulo_final[0])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint4,  angulo_final[1])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint5,  angulo_final[2])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint7,  angulo_final[3])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint9,  angulo_final[4])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint10, angulo_final[5])

        datah.sim.setJointTargetPosition(handler.NAO_m_joint11, angulo_final[6])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint12, angulo_final[7])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint13, angulo_final[8])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint15, angulo_final[9])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint17, angulo_final[10])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint18, angulo_final[11])

        datah.sim.setJointTargetPosition(handler.NAO_m_joint19, angulo_final[12])
        datah.sim.setJointTargetPosition(handler.NAO_m_joint20, angulo_final[13])

        # Giving two time steps for the simulation
        datah.client.step()

        position = datah.sim.getObjectPosition(handler.head, datah.sim.handle_world)

        if position[2] < 0.4:
            early_trigger = True
            break

    if early_trigger == True:
        falls = 1.0
        fitnessA = ((timeStep - fall_penalization)/tiempoSeg) * D
    else:
        falls = 0.0
        fitnessA = (timeStep/tiempoSeg) * D

    # Stoppping the simulation.
    datah.sim.stopSimulation()
    while datah.sim.getSimulationState()!=datah.sim.simulation_stopped:
        pass

    distanceA = (position[0]/max_distance)*(1.0-D)
    true_fitness = round(fitnessA + distanceA, 5)
    return [true_fitness, falls, timeStep]
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
def run_population_evolution (genIndex):

    inputsNeuron = numEntradas + 1
    outputsNeuron = 14
    genome = NEAT.Genome(0, inputsNeuron, 0, outputsNeuron, False, NEAT.ActivationFunction.UNSIGNED_SIGMOID,NEAT.ActivationFunction.UNSIGNED_SIGMOID, 1, params, 0)
    pop = NEAT.Population(genome, params, True, 1.0, genIndex)
    pop.RNG.Seed(port_conexion)
    print('NumLinks:', genome.NumLinks())

    evhist = []
    best_gs = []
    best_fit_ever = 0
    best_index_ever = 0
    datah.dev_stage = 3
    best_generation_ever = 0
    for generation in range(0, generations):
        datah.genome_counter = 0
        genome_list = NEAT.GetGenomeList(pop)
        fit_fall_list = EvaluateGenomeList_Parallel(genome_list, ev_single_genome)
        falls = []
        fitness_list = []
        timeStep_array = []        
        for m in range(0, len(fit_fall_list)):
            fitness_list.append(fit_fall_list[m][0])
            falls.append(fit_fall_list[m][1])
            timeStep_array.append(fit_fall_list[m][2])
        NEAT.ZipFitness(genome_list, fitness_list)

        best = max(fitness_list)
        best_index = fitness_list.index(max(fitness_list))
        evhist.append(best)
        best_genome_aux = pop.GetBestGenome()
        if datah.contGen == int(generations / 2.0):
            best_fit_ever = max(fitness_list)
        else:
            pass
        if best > best_fit_ever:
            sys.stdout.flush()
            best_gs.append(best_genome_aux)
            best_fit_ever = best
            best_index_ever = best_index
            best_generation_ever = generation
        else:
            pass

        # Section for saving relevant data
        fit_index = fitness_list.index(max(fitness_list))
        datah.max_fitness_value[datah.contGen] = fitness_list[fit_index]
        caida_mejor = falls[fit_index]
        datah.fall_of_the_best[datah.contGen] = caida_mejor
        datah.timeStep_of_the_best[datah.contGen] = timeStep_array[fit_index]
        
        datah.average_value[datah.contGen] = np.average(fitness_list)
        datah.median_value[datah.contGen] = np.median(fitness_list)
        
        datah.falls_value[datah.contGen] = sum(falls)
        sf.saveStatistics(datah)
        datah.contGen = cp.deepcopy(datah.contGen) + 1

        pop.Epoch()
        print('Gen:', generation, 'Fit:', best, '. Time Best:', timeStep_array[fit_index], '. Fall Best:', caida_mejor)

    return (best_generation_ever, best_index_ever, best_gs[len(best_gs)-1], best_fit_ever)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def main():

    directory00 = 'NAO_p' + str(populationSize) + '_gen' + str(generations) + '_' + str(port_conexion)
    datah.directory = directory00
    try:
        os.makedirs(directory00)
    except:
        pass

    rd.seed(port_conexion)
        
    coef = np.pi / 180.0

    datah.output_range = [-10.0*coef, 10.0*coef,  -10.0*coef, 10.0*coef, -50.0*coef,     10.0*coef,  25.0*coef,   85.0*coef,  -65.0*coef, -5.0*coef, -30.0*coef,   30.0*coef,  -10.0*coef,  10.0*coef, -10.0*coef,  10.0*coef, -50.0*coef,    10.0*coef, 25.0*coef,   85.0*coef,  -65.0*coef,-5.0*coef,  -30.0*coef, 30.0*coef,  -40.0*coef,  40.0*coef,  -40.0*coef, 40.0*coef]
    
    datah.locked = [-0.029*coef, -0.029*coef, -1.0*coef, -1.0*coef, -18.59*coef, -18.59*coef,  48.52*coef, 48.52*coef,  -30.0*coef, -30.0*coef, 1.0*coef, 1.0*coef,  -0.029*coef,   -0.029*coef, -1.0*coef,   -1.0*coef, -18.59*coef,  -18.59*coef, 48.52*coef, 48.52*coef, -30.0*coef, -30.0*coef, 1.0*coef, 1.0*coef,  0.0*coef,  0.0*coef,  0.0*coef, 0.0*coef]
    
    datah.ang_reduced = [(datah.output_range[n]+datah.locked[n])/2.0 for n in range(0, len(datah.output_range))]

    best_individual = run_population_evolution(port_conexion)
    winner_genome = best_individual[2]

    text01 = datah.directory + '/' + 'winner_genome_' + str(301) + '.txt'
    file = open(text01, 'wb')
    pickle.dump(winner_genome, file)
    file.close()
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
