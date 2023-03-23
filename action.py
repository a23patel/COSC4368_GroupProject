class Action:
    """
    Class to facilitate actions taken by agents in StateSpace.

    arguments: (all functions)
    loc - location of agent
    ssObj - StateSpace Class object
    """

    def isPickupApplicable(self, loc, ssObj):
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

    def isDropoffApplicable(self, loc, ssObj):
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

    def isEastApplicable(self, loc, ssObj):
        # bounds check
        if loc[0] >= 2:
            return False
        # occupied check
        loc = [loc[0] + 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isWestApplicable(self, loc, ssObj):
        # bounds check
        if loc[0] <= 0:
            return False
        # occupied check
        loc = [loc[0] - 1, loc[1], loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isNorthApplicable(self, loc, ssObj):
        # bounds check
        if loc[1] >= 2:
            return False
        # occupied check
        loc = [loc[0], loc[1] + 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isSouthApplicable(self, loc, ssObj):
        # bounds check
        if loc[1] <= 0:
            return False
        # occupied check
        loc = [loc[0], loc[1] - 1, loc[2]]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isUpApplicable(self, loc, ssObj):
        # bounds check
        if loc[2] >= 2:
            return False
        # occupied check
        loc = [loc[0], loc[1], loc[2] + 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def isDownApplicable(self, loc, ssObj):
        # bounds check
        if loc[2] <= 0:
            return False
        # occupied check
        loc = [loc[0], loc[1], loc[2] - 1]
        if ssObj.state_space[loc[0], loc[1], loc[2]].is_occupied():
            return False

        return True

    def moveEast(self, loc, ssObj):
        """
        moves an agent east by updating state space object
        returns nothing
        """
        # perform check
        if self.isEastApplicable(loc, ssObj):
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

    def moveWest(self, loc, ssObj):
        """
        moves an agent west by updating state space object
        returns nothing
        """
        # perform check
        if self.isWestApplicable(loc, ssObj):
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

    def moveNorth(self, loc, ssObj):
        """
        moves an agent north by updating state space object
        returns nothing
        """
        # perform check
        if self.isNorthApplicable(loc, ssObj):
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

    def moveSouth(self, loc, ssObj):
        """
        moves an agent south by updating state space object
        returns nothing
        """
        # perform check
        if self.isSouthApplicable(loc, ssObj):
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

    def moveUp(self, loc, ssObj):
        """
        moves an agent up by updating state space object
        returns nothing
        """
        # perform check
        if self.isUpApplicable(loc, ssObj):
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

    def moveDown(self, loc, ssObj):
        """
        moves an agent down by updating state space object
        returns nothing
        """
        # perform check
        if self.isDownApplicable(loc, ssObj):
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

    def pickupBlock(self, loc, ssObj):
        """
        picks up a block by updating state space object
        returns nothing
        """
        # perform check
        if self.isPickupApplicable(loc, ssObj):
            # update .state_space
            ssObj.state_space[loc[0], loc[1], loc[2]].removeBlock()
            # update agent carrying
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
                ssObj.carF = True
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
                ssObj.carM = True

    def dropoffBlock(self, loc, ssObj):
        """
        drops off a block by updating state space object
        returns nothing
        """
        # perform check
        if self.isDropoffApplicable(loc, ssObj):
            # update .state_space
            ssObj.state_space[loc[0], loc[1], loc[2]].addBlock()
            # update agent carrying
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'F':
                ssObj.carF = False
            if ssObj.state_space[loc[0], loc[1], loc[2]].whichAgent() == 'M':
                ssObj.carM = False