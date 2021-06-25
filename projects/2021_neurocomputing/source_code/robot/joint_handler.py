class JointHandler(object):
    """
    Class to operate with the handlers of the different joints and shapes of the robot.
    """

    def __init__(self, sim):
        self.sim = sim
        self.model = 0

    def get_and_set_model_to_position(self, position):
        """Move the robot to the position received as parameter.

        :param contGen: the generation number
        :type contGen: integer
        """

        self.model = self.sim.get_object_handle("Body")
        self.sim.set_object_position(self.model[1], position)

    def get_head_position(self):
        """Get the robot's head position."""
        return self.sim.get_object_position_buffer_mode(self.head[1])

    def grow_legs(self, finalLength):
        """Grow robot's legs to final length

        :param finalLength: the length the robot's legs will have after this method
        :type finalLength: float
        """
        pass
