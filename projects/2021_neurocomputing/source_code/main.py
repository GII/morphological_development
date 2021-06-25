"""
Main script to launch the experiments.

usage: python main.py [-h] [--port PORT] [--test TEST] [--type TYPE] robot

positional arguments:
  robot        Robot model. Accepted values: quad8DOF, quad16DOF, quad24DOF, hexapod, octopod

optional arguments:
  -h, --help   show this help message and exit
  --port PORT  Port number to connect to Simulator
  --test TEST  Folder name containing the test data
  --type TYPE  Experiment type. Accepted values:nodev, growth

"""

import argparse

from morph_dev_experiment import MorphologicalDevExperiment

from config.evolution_config import EvolutionConfig
from config.evolution_config_growth import EvolutionConfigGrowth
from config.quad_8DOF_experiment_data import Quad8DOFExperimentData
from config.quad_16DOF_experiment_data import Quad16DOFExperimentData
from config.quad_16DOF_experiment_data import Quad16DOFExperimentData
from config.quad_24DOF_experiment_data import Quad24DOFExperimentData
from config.hexapod_experiment_data import HexapodExperimentData
from config.octopod_experiment_data import OctopodExperimentData


from robot.quad_8DOF_handler import Quad8DOFJointHandler
from robot.quad_16DOF_handler import Quad16DOFJointHandler
from robot.quad_24DOF_handler import Quad24DOFJointHandler
from robot.hexapod_handler import HexapodJointHandler
from robot.octopod_handler import OctopodJointHandler

import config
import robot

from util.vrep_util import VREPSimulatorFacade


def check_arguments(available_robots, available_types, default_port=19997):
    """Parse the script arguments.

    If a port number is received as an argument, then this number is used to establish the connection
    to V-REP, otherwise, a default port value is set.

    Setting the port number to the V-REP connection allows different V-REP experiments to be run
    on the same computer. The port number is also used as a seed generator for random values.

    If a test folder is received as an argument, then this folder is used to load the experiment in test mode,
    i.e. the simulation is launched with the best individual saved from a previous experiment.

    :param available_robots: List of available robots
    :param available_types: List of available types of expermiments
    :param default_port: The default port for the connection if no other one if received as an argument

    :type available_robots: list
    :type available_types: list
    :type default_port: integer

    :return: port_connection: the port number
    :return: test: indicates if the mode is test (test = True) or learning (test = False)
    :return: robot: the robot model
    :return: type: the experiment type (growth or no devel)
    :rtype: (integer, bool, string, string)
    """
    robot_help_message = "Robot model. Accepted values: " + ", ".join(available_robots)
    type_help_message = "Experiment type. Accepted values:" + ", ".join(available_types)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port number to connect to Simulator")
    parser.add_argument("--test", help="Folder name containing the test data")
    parser.add_argument("--type", help=type_help_message)
    parser.add_argument("robot", help=robot_help_message)

    arg = parser.parse_args()
    if arg.port:
        port_connection = int(arg.port)
        print("Port:", port_connection)
    else:
        port_connection = default_port

    test = False
    if arg.test:
        test = str(arg.test) == "True"

    type = "nodev"
    if arg.type:
        type = arg.type

    robot = arg.robot

    return port_connection, test, robot, type


if __name__ == "__main__":
    # Check script arguments
    available_robots = ["quad8DOF", "quad16DOF", "quad24DOF", "hexapod", "octopod"]
    available_types = ["nodev", "growth"]
    port_connection, test, robot, exp_type = check_arguments(available_robots, available_types)

    if not robot in available_robots:
        print("Experiment not available: ", robot)
    else:
        # Connect to the VREP simulator
        sim = VREPSimulatorFacade(port_connection)
        sim.connect()

        # Get configuration classes
        if not exp_type in available_types:
            print("Experiment type not available: ", exp_type)
        else:
            growth = False
            if exp_type == "growth":
                config = EvolutionConfigGrowth()
                growth = True
            else:
                config = EvolutionConfig()

            if robot == "quad8DOF":
                handler = Quad8DOFJointHandler(sim)
                data = Quad8DOFExperimentData(config.generations)
            elif robot == "quad16DOF":
                handler = Quad16DOFJointHandler(sim)
                data = Quad16DOFExperimentData(config.generations)
            elif robot == "quad24DOF":
                handler = Quad24DOFJointHandler(sim)
                data = Quad24DOFExperimentData(config.generations)
            elif robot == "hexapod":
                handler = HexapodJointHandler(sim)
                data = HexapodExperimentData(config.generations)
            elif robot == "octopod":
                handler = OctopodJointHandler(sim)
                data = OctopodExperimentData(config.generations)

            # Run evolution
            experiment = MorphologicalDevExperiment(port_connection, sim, config, handler, data, growth)
            if test:
                test_folder = robot + "_" + exp_type
                experiment.run_test(test_folder)
            else:
                experiment.run_evolution()

            # Connect from the VREP simulator
            sim.disconnect()
