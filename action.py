# TODO change loc parameter to agent since passing the ssObj already
class Action:
    """
    Class to facilitate actions taken by agents in StateSpace.

    arguments: (all functions)
    agent - 'F' for female agent; 'M' for male agent
    ssObj - StateSpace Class object
    """
    def isPickupApplicable(self, agent, ssObj):
        """
        returns True if agent can validly pick up a block and False otherwise
        """
        loc = ssObj.getLocation(agent)
        
        # check cell type
        if ssObj.state_space[loc[0], loc[1], loc[2]].getType() != 'Pickup':
            return False

        # check carrying
        if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
            if ssObj.carF:
                return False
        if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
            if ssObj.carM:
                return False

        # check number of blocks
        if ssObj.state_space[loc[0], loc[1], loc[2]].getNumBlocks() <= 0:
            return False

        return True

    def isDropoffApplicable(self, agent, ssObj):
        """
        returns True if agent can validly drop off a block and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # check cell type
        if ssObj.state_space[loc[0], loc[1], loc[2]].getType() != 'Dropoff':
            return False

        # check carrying
        if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
            if not ssObj.carF:
                return False
        if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
            if not ssObj.carM:
                return False

        # check number of blocks
        if ssObj.state_space[loc[0], loc[1], loc[2]].getNumBlocks() >= 5:
            return False

        return True

    def isEastApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move east and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[0] >= 2:
            return False
        # occupied check
        loc = [loc[0] + 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isWestApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move west and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[0] <= 0:
            return False
        # occupied check
        loc = [loc[0] - 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isNorthApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move north and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[1] >= 2:
            return False
        # occupied check
        loc = [loc[0], loc[1] + 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isSouthApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move south and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[1] <= 0:
            return False
        # occupied check
        loc = [loc[0], loc[1] - 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isUpApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move up and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[2] >= 2:
            return False
        # occupied check
        loc = [loc[0], loc[1], loc[2] + 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isDownApplicable(self, agent, ssObj):
        """
        returns True if agent can validly move down and False otherwise
        """
        loc = ssObj.getLocation(agent)

        # bounds check
        if loc[2] <= 0:
            return False
        # occupied check
        loc = [loc[0], loc[1], loc[2] - 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def moveEast(self, agent, ssObj):
        """
        moves an agent east by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isEastApplicable(agent, ssObj):
            newLoc = [loc[0]+1, loc[1], loc[2]]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def moveWest(self, agent, ssObj):
        """
        moves an agent west by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isWestApplicable(agent, ssObj):
            newLoc = [loc[0]-1, loc[1], loc[2]]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def moveNorth(self, agent, ssObj):
        """
        moves an agent north by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isNorthApplicable(agent, ssObj):
            newLoc = [loc[0], loc[1]+1, loc[2]]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def moveSouth(self, agent, ssObj):
        """
        moves an agent south by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isSouthApplicable(agent, ssObj):
            newLoc = [loc[0], loc[1]-1, loc[2]]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def moveUp(self, agent, ssObj):
        """
        moves an agent up by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isUpApplicable(agent, ssObj):
            newLoc = [loc[0], loc[1], loc[2]+1]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def moveDown(self, agent, ssObj):
        """
        moves an agent down by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isDownApplicable(agent, ssObj):
            newLoc = [loc[0], loc[1], loc[2]-1]
            agent = ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent()

            # update state space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeAgent(agent)
            ssObj.state_space[newLoc[0], newLoc[1], newLoc[2]].addAgent(agent)

            # update agent location
            if agent == 'F':
                ssObj.locF = newLoc
            if agent == 'M':
                ssObj.locM = newLoc

    def pickupBlock(self, agent, ssObj):
        """
        picks up a block by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isPickupApplicable(agent, ssObj):
            # update .state_space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeBlock()
            # update agent carrying
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
                ssObj.carF = True
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
                ssObj.carM = True

    def dropoffBlock(self, agent, ssObj):
        """
        drops off a block by updating state space object
        returns nothing
        """
        loc = ssObj.getLocation(agent)

        # perform check
        if self.isDropoffApplicable(agent, ssObj):
            # update .state_space
            ssObj.state_space[loc[0], loc[1], loc[2]].addBlock()
            # update agent carrying
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
                ssObj.carF = False
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
                ssObj.carM = False