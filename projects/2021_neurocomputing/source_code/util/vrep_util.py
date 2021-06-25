import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))

try:
    import vrep
except:
    print("--------------------------------------------------------------")
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print("Make sure both are in the same folder as this file,")
    print('or appropriately adjust the file "vrep.py"')
    print("--------------------------------------------------------------")
    print("")


class VREPSimulatorFacade(object):
    """VREP Simulator Facade"""

    def __init__(self, port):
        self.port_connection = port
        self.clientID = -1

    def connect(self):
        """Open the connection to V-REP.

        All the previous connections are closed before establish the connection.

        :param port_connection: The port number to establish the connection
        :type port_connection: integer

        :return: the V-REP Client ID
        :rtype: integer
        """

        print("Program started")
        vrep.simxFinish(-1)  # just in case, close all opened connections
        clientID = vrep.simxStart("127.0.0.1", self.port_connection, True, True, 5000, 5)  # Connect to V-REP
        if clientID != -1:
            print("Connected to remote API server")
            print("Simulation Started")
            self.clientID = clientID
        else:
            print("Failed connecting to remote API server")

    def disconnect(self):
        """Close the connection."""
        vrep.simxFinish(self.clientID)

    def start_simulation(self):
        """Start the simulation."""
        vrep.simxSynchronous(self.clientID, True)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)

    def stop_simulation(self):
        """Stop the simulation."""
        retCode = vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
        while retCode != 0:
            retCode = vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)

    def get_object_position_buffer_mode(self, objectHandle):
        """Get the absolute position on an object.

        :param objectHandle: the handle of the object
        :type object: integer

        :return: the position on the object
        :rtype: list
        """
        # relativeToObjectHandle = -1: indicates the
        retCode, position = vrep.simxGetObjectPosition(self.clientID, objectHandle, -1, vrep.simx_opmode_buffer)
        vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxGetPingTime(self.clientID)
        return position

    def get_object_position_stream_mode(self, object):
        """Get the absolute position on an object with API operation mode =  streaming.

        API operation mode streaming is the recomended mode for the firts call. The following calls should be use  operation mode buffer.

        :param objectHandle: the handle of the object
        :type object: integer

        :return: the position on the object
        :rtype: list
        """
        retCode, position = vrep.simxGetObjectPosition(self.clientID, object, -1, vrep.simx_opmode_streaming)
        vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxGetPingTime(self.clientID)
        return position

    def set_object_position(self, object, position):
        vrep.simxSetObjectPosition(self.clientID, object, -1, position, vrep.simx_opmode_oneshot)

    def get_object_handle(self, object_name):
        """Get the handle of an object.

        :param object_name: the name of the object
        :type object: string

        :return: the handle of the object
        :rtype: integer
        """
        object = vrep.simxGetObjectHandle(self.clientID, object_name, vrep.simx_opmode_blocking)
        return object

    def set_joint_target_position(self, joint, target_position):
        vrep.simxSetJointTargetPosition(self.clientID, joint, target_position, vrep.simx_opmode_oneshot)

    def set_joint_position(self, joint, position):
        vrep.simxSetJointPosition(self.clientID, joint, position, vrep.simx_opmode_oneshot)

    def sync_trigger(self):
        vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxGetPingTime(self.clientID)
