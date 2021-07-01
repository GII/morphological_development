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

"""This module contains the class to instance for running morphogical development experiments."""


import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".", "lib"))

import sys
import pickle
import copy as cp
import numpy as np
import random as rd
import cv2

import MultiNEAT as NEAT
from MultiNEAT import EvaluateGenomeList_Serial

from config.experiment_type import ExperimentType


class MorphologicalDevExperiment(object):
    """This class represents a  morphological development experiment.

    :param port: The port number used to connect to the simulator. It's also used as seed generator for random values.
    :param sim: The simulatior facade object with the methods used in the experiments
    :param config: Parameter for the evolution configuration.
    :param handler: The joint handlers of the robot with which the experiment is carried out.
    :param data: Class to store relevant data during the evolution
    :param experiment_type: Indicates the type of the experiment

    :type port: string
    :type sim: VREPSimulatorFacade
    :type config: EvolutionConfig
    :type handler: JointHandler
    :type data: ExperimentData
    :type experiment_type: ExperimentType
    """

    def __init__(self, port, simulator, config, handler, data, experiment_type):
        """Initialize a no dev experiment class."""
        self.port_connection = port
        self.sim = simulator
        self.config = config
        self.handler = handler
        self.datah = data
        self.experiment_type = experiment_type

    def load_robot(self):
        """Get all the needed handlers of the robot and start the simulation.

        Although the model of the robot is not loaded, this function is utilized for getting all the needed
        handlers of the robot, as well as activating some data stream and starting the simulation. The simulation
        is launched in synchronous mode.
        """
        if self.experiment_type.value == ExperimentType.growth:
            # Calculate the length of the robot's legs for the generation contGen
            self.config.set_final_length(self.datah.contGen)
            # Calculate the position of the robot with its new legs length
            self.config.set_final_pos(self.handler.final_pos_x)
            # Raise the robot to the position previous calculated
            self.handler.get_and_set_model_to_position(self.config.finalPos)

        # Get all handlers
        self.handler.get_joint_handlers()

        if self.experiment_type.value == ExperimentType.growth:
            self.handler.grow_legs(self.config.finalLength)

        # Start simulation
        self.sim.start_simulation()

        # Get the positin of the head in stream mode
        self.sim.get_object_position_stream_mode(self.handler.head[1])

    def ev_single_genome(self, genome):
        """Return the fitness value for an individual.

        :param genome: The individal to evolve

        :return: the distance travelled by the robot in straight line for each individual (genotype)
        :rtype: Genome
        """
        # Getting the robot handlers and starting the simulation
        self.load_robot()

        # Configure the Neat NN
        net = NEAT.NeuralNetwork()
        genome.BuildPhenotype(net)

        # Loop to evaluate the performance of the individual during "secondsTime" in real time. In this loop, the NN is
        # evaluated each 2 time steps, to give enough time to the joints to reach the desired position
        for timeStep in range(0, self.config.secondsTime):
            inputs_already_norm = []
            inputs_already_norm.append(self.config.A * np.sin(self.config.omega * timeStep))
            inputs_already_norm.append(1.0)  # Add one extra input for the bias neuron input

            net.Flush()
            net.Input(inputs_already_norm)
            for _ in range(2):
                net.Activate()
            net_out_std = net.Output()

            final_angle = self.datah.denormalize_outputs(net_out_std)

            # Moving the joints of the robot to the target position given by the outputs of the
            self.handler.move_joints_to_position(final_angle)

        # Getting the final position of the head of the robot
        position = self.handler.get_head_position()

        self.sim.stop_simulation()

        return position[0]

    def run_population_evolution(self, genIndex):
        """Evolve the population.

        :param genIndex: Number
        :rtype: integer: Seed for the random generation when creating the population

        :return: Best generation number, best individual index, best individual and best fitness
        :rtype: integer, integer, Genome, float

        """
        # Definition of the features of each genome of the population and creation of the population.
        inputsNeuron = self.config.numEntries + 1
        outputsNeuron = self.handler.joint_number
        genome = NEAT.Genome(
            0,
            inputsNeuron,
            0,
            outputsNeuron,
            False,
            NEAT.ActivationFunction.UNSIGNED_SIGMOID,
            NEAT.ActivationFunction.UNSIGNED_SIGMOID,
            1,
            self.config.neat_params,
            0,
        )

        # Genone, NEAT config parameters, RandomizeWeights = True,  RandonRange = 1.0, RNG_seed = genIndex
        pop = NEAT.Population(genome, self.config.neat_params, True, 1.0, genIndex)
        pop.RNG.Seed(self.port_connection)
        print("NumLinks:", genome.NumLinks())

        evhist = []
        best_gs = []
        best_fit_ever = 0
        best_index_ever = 0
        best_generation_ever = 0
        # Evolution loop
        for generation in range(0, self.config.generations):
            self.datah.genome_counter = 0
            genome_list = NEAT.GetGenomeList(pop)
            fitness_list = EvaluateGenomeList_Serial(genome_list, self.ev_single_genome, display=False)
            NEAT.ZipFitness(genome_list, fitness_list)

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

            # Section for saving relevant data
            fit_index = fitness_list.index(max(fitness_list))
            self.datah.max_fitness_value[self.datah.contGen] = fitness_list[fit_index]
            self.datah.average_value[self.datah.contGen] = np.average(fitness_list)
            self.datah.median_value[self.datah.contGen] = np.median(fitness_list)
            self.datah.saveStatistics()
            self.datah.contGen = cp.deepcopy(self.datah.contGen) + 1

            # Update the population. Point where the NEAT do its stuff
            pop.Epoch()

            print(
                "Gen:",
                generation,
                "Fit:",
                best,
                "Mediana:",
                round(np.median(fitness_list), 3),
                "Media:",
                round(np.average(fitness_list), 3),
                "Std:",
                round(np.std(fitness_list), 3),
            )
        return (best_generation_ever, best_index_ever, best_gs[len(best_gs) - 1], best_fit_ever)

    def set_data_folder_name(self):
        """Set then name of the folder to save the experiments.

        :return: The forder path
        :rtype: string
        """
        directory00 = (
            self.config.result_folder
            + os.path.sep
            + "4legged_p"
            + str(self.config.populationSize)
            + "_gen"
            + str(self.config.generations)
            + "_"
            + str(self.port_connection)
        )
        return directory00

    def create_data_folder(self):
        """Create a folder to save the relevant data.

        If the data folder can't be created, an error message is shown

        :return: error (True: if the folder couldn't be created, otherwise False)
        :rtype: boolean
        """
        error = False
        self.datah.directory = self.set_data_folder_name()
        try:
            os.makedirs(self.datah.directory, exist_ok=True)
        except:
            print("The expermiment cannot be run. Error creating the data folder: " + str(self.datah.directory))
            error = True

        return error

    def serialize_best_individual(self, winner_genome):
        """Serialize to a file the winner genome.

        :param best_individual: The best individual to serialize
        :type best_individual: Genome

        :return: error (True: if the file couldn't be created, otherwise False)
        :rtype: boolean
        """
        error = False
        try:
            # saving the genome of the best individual obtained
            text01 = self.datah.directory + "/" + "winner_genome_" + str(0) + ".txt"
            file = open(text01, "wb")
            pickle.dump(winner_genome, file)
            file.close()
        except:
            error = True

        return error

    def load_winner_genome(self):
        """Load the winner genome data from file with pickle.

        :return: the winner genome and error (True: if the file couldn't be created, otherwise False)
        :rtype: Genome, boolean
        """
        text = (
            self.config.test_folder
            + os.path.sep
            + self.datah.directory
            + os.path.sep
            + "winner_genome_"
            + str(0)
            + ".txt"
        )
        error = False
        winner_genome = None
        try:
            with open(text, "rb") as newfile:
                winner_genome = pickle.load(newfile)
        except:
            error = True

        return error, winner_genome

    def experiment_configuration(self):
        """Set some configuration for the expermiment.

        This configuration is used both in the full experiment run and in test mode.
        """
        rd.seed(self.port_connection)
        self.datah.full_generations = self.config.generations
        arm_range = [
            cp.deepcopy(self.config.min_arm * np.pi) / 180.0,
            cp.deepcopy(self.config.max_arm * np.pi) / 180.0,
        ]
        leg_range = [
            cp.deepcopy(self.config.min_leg * np.pi) / 180.0,
            cp.deepcopy(self.config.max_leg * np.pi) / 180.0,
        ]
        if self.experiment_type == ExperimentType.rom:
            self.datah.set_output_range(arm_range, leg_range, self.config.angle_offset)
        else:
            self.datah.set_output_range(arm_range, leg_range)

    def draw_best_nn(self, winner_genome):
        """Draw the NN of the best individual.

        :param winner_genome: The best individual
        :type best_individual: Genome
        """
        net = NEAT.NeuralNetwork()
        winner_genome.BuildPhenotype(net)
        img = np.zeros((500, 500, 3), dtype=np.uint8)
        NEAT.DrawPhenotype(img, (0, 0, 500, 500), net)
        text = self.config.test_folder + os.path.sep + self.datah.directory + os.path.sep + "Best_Net.png"
        cv2.imwrite(text, img)

    def run_test(self, test_folder):
        """
        Run the experiment only with one individual, the best one saved in a previous expermiment.

        :param test_folder: The name of the folder that contains the data of the individual to evolve.
        :type test_folder: string
        """
        if self.experiment_type.value == ExperimentType.growth:
            self.datah.contGen = self.config.test_generations

        self.datah.directory = test_folder
        error, winner_genome = self.load_winner_genome()
        if not error:
            self.experiment_configuration()
            fitness = self.ev_single_genome(winner_genome)
            print("Fitness: ", fitness)
            self.draw_best_nn(winner_genome)
            self.sim.stop_simulation()

    def run_evolution(self):
        """Run the evolution and serializes the result.

        If the data folder to save the results can't be created the expermient is not executed.
        """
        error = self.create_data_folder()
        # If the data folder could not be created, the experiment is not run
        if not error:
            self.experiment_configuration()
            # Run the evolution loop and get the best individual
            best_individual = self.run_population_evolution(self.port_connection)
            winner_genome = best_individual[2]
            error = self.serialize_best_individual(winner_genome)
            if error:
                print("Error saving the best individual in a file.")
            self.sim.stop_simulation()
