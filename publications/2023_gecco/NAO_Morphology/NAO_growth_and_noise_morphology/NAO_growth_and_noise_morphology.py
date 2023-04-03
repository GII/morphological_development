import os
import sys
import pickle
import argparse
import copy as cp
import numpy as np
import random as rd
import MultiNEAT as NEAT
import supportFile as sf

from MultiNEAT import EvaluateGenomeList_Serial
from MultiNEAT import GetGenomeList, ZipFitness

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

# Setting the port number to the CoppeliaSim connection for running several independet experiments in the CESGA supercomputer (https://www.cesga.es/en/home-2/)
# At the same time, the port number is used as seed for generating random values.
cluster = False
if cluster == True:
    port_conexion = int(sys.argv[1])
    relativePath = sys.argv[2]
else:
    relativePath = 'NAO_growth_and_noise_input_sigma'
    port_conexion = 19997

# Opening the connection with CoppeliaSim simulator
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1', port_conexion, True, True, 5000, 5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
    print ('Simulation Started')
else:
    print ('Failed connecting to remote API server')

# Parameters of the growing morphology
trigGrowth = 150.0  # Generation at which the robot stop growing
StartLenght = 0.0   # Initial leg joint extension, in meters
FinalLength = 0.04  # Final leg joint extension, in meters 
startPos = 0.33243  # Initial position of the centre of robot in the "z" axis. Used to updapte the initial position of the robot at each generation when the robot grows

# Setting the values of the experimental parameters.
simSteps = 100          # Number of simulaton steps performed by the robot 
numEntries = 3          # Number of inputs to the NeuralNetwork
generations = 300       # Number of generations
populationSize = 50     # Size of the population

# Parameters of the sinusoidal function that consitutes the inputs of the NeuralNetwork. It is the motor patern generator of the robot.
A = 2.0
omega = 2.42 * np.pi / 20.0

# Parameters of the gaussian function utilized for generation random noise.
mu = 0.0
sigma = 0.01 # Change the sigma value according to the experiment

# Class for saving relevant data of the neuroevolutionary process.
datah = sf.saveData(generations)

# Classs to store the different handlers the robot needs to operate in the simulator. This clase has the "old naming", due to previous work with the PyRep extension of the CoppeliaSim.
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
        self.head = 0           # Head of the robot

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

    # Section to load the adult morphology of the robot and avoid the constant growth of its morphology
    if datah.contGen <= trigGrowth:
        pass
    elif datah.contGen > trigGrowth and datah.trigGrowth == False:
        if cluster == True:
            datah.trigGrowth = True
            nameBase = '/naoScene5.ttt'
            pathToScene = '/mnt/netapp2/Home_FT2/home/ulc/ii/mnv/pythonExperiment/' + relativePath + nameBase
            retCode = sim.simxLoadScene(clientID, pathToScene, 1, sim.simx_opmode_blocking)
        else:
            datah.trigGrowth = True
            nameBase = '/naoScene5.ttt'
            # Change this path for the absolute path of your local directory
            pathToScene = '/home/martin/Python_Projects/2023_GECCO/zzSourceCode/' + relativePath + nameBase
            retCode = sim.simxLoadScene(clientID, pathToScene, 1, sim.simx_opmode_blocking)
    elif datah.contGen > trigGrowth and datah.trigGrowth == True:
        pass

    # Section where all the handlers of the robot are obtained and stored in the class with their corresponding name.
    # Left side of the NAO
    handler.NAO_m_joint3 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint3', sim.simx_opmode_blocking)
    handler.NAO_m_joint4 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint4', sim.simx_opmode_blocking)
    handler.NAO_m_joint5 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint5', sim.simx_opmode_blocking)
    handler.NAO_m_joint7 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint7', sim.simx_opmode_blocking)
    handler.NAO_m_joint9 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint9', sim.simx_opmode_blocking)
    handler.NAO_m_joint10 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint10', sim.simx_opmode_blocking)
    
    # Right side of the NAO
    handler.NAO_m_joint11 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint11', sim.simx_opmode_blocking)
    handler.NAO_m_joint12 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint12', sim.simx_opmode_blocking)
    handler.NAO_m_joint13 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint13', sim.simx_opmode_blocking)
    handler.NAO_m_joint15 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint15', sim.simx_opmode_blocking)
    handler.NAO_m_joint17 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint17', sim.simx_opmode_blocking)
    handler.NAO_m_joint18 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint18', sim.simx_opmode_blocking)
    
    # Shoulders of the NAO
    handler.NAO_m_joint19 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint19', sim.simx_opmode_blocking)
    handler.NAO_m_joint20 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint20', sim.simx_opmode_blocking)

    # Extension joints of the robot, those that growth
    handler.NAO_m_joint6 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint6', sim.simx_opmode_blocking)
    handler.NAO_m_joint8 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint8', sim.simx_opmode_blocking)
    handler.NAO_m_joint14 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint14', sim.simx_opmode_blocking)
    handler.NAO_m_joint16 = sim.simxGetObjectHandle(clientID, 'NAO_m_joint16', sim.simx_opmode_blocking)

    # Head of the robot
    handler.head = sim.simxGetObjectHandle(clientID, 'imported_part_16_sub0', sim.simx_opmode_blocking)
    handler.NAO = sim.simxGetObjectHandle(clientID, 'NAO', sim.simx_opmode_blocking)

    # Section for making the robot to growth and update the initial position of the joints that growth, those which are extendable joints, and the position of the NAO in the "z" axis.
    if datah.contGen <= trigGrowth:        
        extension_leg = ((FinalLength - StartLenght) * (float(datah.contGen) / trigGrowth)) + rd.gauss(mu, sigma)
        datah.finalLenght = StartLenght + extension_leg
            
        movement_in_z = abs(extension_leg * (np.sin(75.1*np.pi / 180) + np.sin(59.0*np.pi / 180)))
        finalPos = [0.0, 0.0, cp.deepcopy(startPos + movement_in_z)]
                
        retCode = sim.simxSetObjectPosition(clientID, handler.NAO[1], -1, finalPos, sim.simx_opmode_oneshot)
        
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint6[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint8[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint14[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint16[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointPosition(clientID, handler.NAO_m_joint6[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointPosition(clientID, handler.NAO_m_joint8[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointPosition(clientID, handler.NAO_m_joint14[1],  -datah.finalLenght, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointPosition(clientID, handler.NAO_m_joint16[1],  -datah.finalLenght, sim.simx_opmode_oneshot)    

    # Starting the simulation in Synchronous mode. The simulation timming is controlled by the Python program and not by the simulation itselfs.  
    sim.simxSynchronous(clientID, True)
    sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)

    # The firts time that the position of the head of the robot is obtained. The first time that the function "simxGetObjectPosition" is called, it has different parameters than the rest of the times is called. For that, it is called insided this function.
    retCode = sim.simxGetObjectPosition(clientID, handler.head[1], -1, sim.simx_opmode_streaming)
    retCode = sim.simxSynchronousTrigger(clientID)


# Function where each genome of the population is evaluated, returning its fitness value.
def ev_single_genome(genome):

    # Load of the robot.
    loadRobot()

    # Bulding the NeuralNetwork configuration based on the information provided in the genome.
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)

    aux_fitness = []
    early_trigger = False
    # Loop for moving the robot "simSteps" times.
    for timeStep in range(0, simSteps):
        inputs_already_norm = []
        #  Building the array of the input values to the NeuralNetwork.
        inputs_already_norm.append(A*np.sin(omega * timeStep))
        inputs_already_norm.append(A*np.sin(omega * timeStep + np.pi/2.0))
        inputs_already_norm.append(A*np.sin(omega * timeStep + np.pi/3.0))
        inputs_already_norm.append(1.0)   

        # Activation of the NeuralNetwork.
        net.Flush()
        net.Input(inputs_already_norm)
        for _ in range(2):
            net.Activate()
        net_out_std = net.Output()
        
        # Denormalization of the outputs of the NeuralNetwork.
        final_angle = sf.normalizeOuputs(net_out_std, datah)    

        # Updating of the postion of the NAO's joints at each simulation time step.
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint3[1],  final_angle[0], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint4[1],  final_angle[1], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint5[1],  final_angle[2], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint7[1],  final_angle[3], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint9[1],  final_angle[4], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint10[1], final_angle[5], sim.simx_opmode_oneshot)

        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint11[1], final_angle[6], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint12[1], final_angle[7], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint13[1], final_angle[8], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint15[1], final_angle[9], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint17[1], final_angle[10], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint18[1], final_angle[11], sim.simx_opmode_oneshot)

        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint19[1], final_angle[12], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, handler.NAO_m_joint20[1], final_angle[13], sim.simx_opmode_oneshot)

        for _ in range(1):
            retCode = sim.simxSynchronousTrigger(clientID)

        retCode, position = sim.simxGetObjectPosition(clientID, handler.head[1], -1, sim.simx_opmode_buffer)
        retCode = sim.simxSynchronousTrigger(clientID)

        # Evaluation of the height of the NAOs hed. If it falls below 0.3, we consider that the NAO has fallen and the simulation stops. Returning a fitness falue of 0.
        if position[2] < 0.3:
            true_timeStep = cp.deepcopy(timeStep)
            early_trigger = True
            break
        else:
            aux_fitness.append(position[0])

    # Stoppping the simulation.
    retCode = sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)
    while retCode != 0:
        retCode = sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)

    # Section for setting the fitness of the robot in case of falling. Otherwise, retrieve the distance traveled by the head of the NAO in the "x" direction.
    if early_trigger == True:
        if len(aux_fitness) > 16:
            true_aux_fitness = aux_fitness[true_timeStep - 15]
        else:
            true_aux_fitness = 0.0
    else:
        true_aux_fitness = aux_fitness[simSteps-1]

    return round(true_aux_fitness, 5)

# Function where the neuroevoluton process takes place.
def run_population_evolution (genIndex):

    # Configuration of the genome and population.
    inputsNeuron = numEntries + 1
    outputsNeuron = 14
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
        genome_list = NEAT.GetGenomeList(pop)
        fitness_list = EvaluateGenomeList_Serial(genome_list, ev_single_genome, display=False)
        NEAT.ZipFitness(genome_list, fitness_list)

        # Code for storing the best genome of each generation and its fitness value.
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

        # Section for saving relevant data into a file for further analysis.
        fit_index = fitness_list.index(max(fitness_list))
        datah.max_fitness_value[datah.contGen] = fitness_list[fit_index]
        datah.average_value[datah.contGen] = np.average(fitness_list)
        datah.median_value[datah.contGen] = np.median(fitness_list)
        sf.saveStatistics(datah)
        datah.contGen = cp.deepcopy(datah.contGen) + 1

        # Update of the neuroevolutionary process
        pop.Epoch()
        print('Gen:', generation, 'Fit:', best, 'Mediana:', round(np.median(fitness_list),3), 'Media:', round(np.average(fitness_list),3), 'Std:', round(np.std(fitness_list),3))

    return (best_generation_ever, best_index_ever, best_gs[len(best_gs)-1], best_fit_ever)

def main():

    # Creating a directory where all the information of the learning process is stored.
    directory00 = 'NAO_p' + str(populationSize) + '_gen' + str(generations) + '_' + str(port_conexion)
    datah.directory = directory00
    try:
        os.makedirs(directory00)
    except:
        pass

    rd.seed(port_conexion)
    
    # Range of Motion of the different NAO joints in radians.
    coef = np.pi / 180.0
    datah.output_range = [0.0*coef,  0.0*coef,  -20.0*coef,  20.0*coef, -50.0*coef,     10.0*coef,  25.0*coef,   85.0*coef,  -65.0*coef, -5.0*coef, -30.0*coef,   30.0*coef,  0.0*coef,    0.0*coef, -20.0*coef,   20.0*coef, -50.0*coef,    10.0*coef, 25.0*coef,   85.0*coef,  -65.0*coef,-5.0*coef,  -30.0*coef, 30.0*coef,  -20.0*coef,  50.0*coef,  -20.0*coef, 50.0*coef]

    # Neuroevolution.
    best_individual = run_population_evolution(port_conexion)
    
    # Saving the bet genome.
    winner_genome = best_individual[2]
    text01 = datah.directory + '/' + 'winner_genome_' + str(301) + '.txt'
    file = open(text01, 'wb')
    pickle.dump(winner_genome, file)
    file.close()

    # stop the simulation:
    sim.simxStopSimulation(clientID,sim.simx_opmode_blocking)
    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)


if __name__ == '__main__':
    main()
