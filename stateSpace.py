from cell import Cell
from action import Action
import numpy as np
import cv2


class StateSpace:
    def __init__(self, experiment):
        """
        Constructor for RW state space.

        Argument:
        experiment - 'original' or 'modified'
        original corresponds to experiments 1, 2, 3, & part of 4
        modified corresponds to part of experiment 4

        Properties:
        state_space - a 3D NumPy array of Cells
        locF - (x,y,z) coordinates of female agent
        locM - (x,y,z) coordinates of male agent
        carF - True if female agent is carrying a block and False otherwise
        carM - True if male agent is carrying a block and False otherwise
        locDrop - list of (x,y,z) coordinates of each Dropoff cell
        locPick - list of (x,y,z) coordinates of each Pickup cell
        """
        self.state_space = np.empty(shape=(
            3, 3, 3), dtype=object, order='C')   # 'C' means row-major order in memory
        self.locF = None
        self.locM = None
        self.carF = False
        self.carM = False
        self.locDrop = []
        self.locPick = []

        # initializing state_space as all basic cells
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x, y, z] = Cell()

        # female agent
        self.state_space[0, 0, 0].addAgent('F')
        self.locF = [0, 0, 0]

        # male agent
        self.state_space[2, 1, 2].addAgent('M')
        self.locM = [2, 1, 2]

        # pickup cells
        if experiment == 'original':
            self.state_space[1, 1, 0].setType('Pickup')
            self.locPick.append([1, 1, 0])
            self.state_space[2, 2, 1].setType('Pickup')
            self.locPick.append([2, 2, 1])
        elif experiment == 'modified':
            self.state_space[1, 2, 2].setType('Pickup')
            self.locPick.append([1, 2, 2])
            self.state_space[0, 2, 0].setType('Pickup')
            self.locPick.append([0, 2, 0])

        # dropoff cells
        self.state_space[0, 0, 1].setType('Dropoff')
        self.locDrop.append([0, 0, 1])
        self.state_space[0, 0, 2].setType('Dropoff')
        self.locDrop.append([0, 0, 2])
        self.state_space[2, 0, 0].setType('Dropoff')
        self.locDrop.append([2, 0, 0])
        self.state_space[2, 1, 2].setType('Dropoff')
        self.locDrop.append([2, 1, 2])

        # risk cells
        self.state_space[1, 1, 1].setType('Risk')
        self.state_space[2, 1, 0].setType('Risk')

    def getLocation(self, agent):
        """
        returns (x,y,z) coordinates of agent
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if agent == 'F':
            return self.locF
        if agent == 'M':
            return self.locM

    def isAgentCarrying(self, agent):
        """
        returns True if agent is carrying a block and False otherwise
        argument:
        agent - 'F' for female agent; 'M' for male agent
        """
        if agent == 'F':
            return self.carF
        if agent == 'M':
            return self.carM

    def isPickup(self, loc):
        """
        returns True if cell is Pickup and False otherwise
        argument:
        loc - (x,y,z) coordinates of a cell
        """
        return self.state_space[loc[0], loc[1], loc[2]].getType() == 'Pickup'

    def isDropoff(self, loc):
        """
        returns True if cell is Dropoff and False otherwise
        argument:
        loc - (x,y,z) coordinates of a cell
        """
        return self.state_space[loc[0], loc[1], loc[2]].getType() == 'Dropoff'
    
    def performAction(self, agent, action):
        """
        performs action by calling appropriate Action method
        arguments:
        agent - 'F' for female agent; 'M' for male agent
        action - 'Pickup', 'Dropoff', 'E', 'W', 'N', 'S', 'U', or 'D'
        """
        a = Action()
        if action == 'Pickup':
            a.pickupBlock(agent, self)
        if action == 'Dropoff':
            a.dropoffBlock(agent, self)
        if action == 'E':
            a.moveEast(agent, self)
        if action == 'W':
            a.moveWest(agent, self)
        if action == 'N':
            a.moveNorth(agent, self)
        if action == 'S':
            a.moveSouth(agent, self)
        if action == 'U':
            a.moveUp(agent, self)
        if action == 'D':
            a.moveDown(agent, self)

    def visualize(self):
        block_size = 50  # size of each cell in pixels
        grid_width = self.state_space.shape[0] * block_size
        grid_height = self.state_space.shape[1] * block_size

        # initialize grid as black image
        grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

        cell = Cell()

        # draw cells onto the grid
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x, y, z]
                    agent = cell.whichAgent()
                    block_type = cell.getType()

                    # calculate top-left corner of cell
                    top_left = (x * block_size, y * block_size)

                    # draw cell as a rectangle
                    color = (255, 255, 255)  # white color for basic cell
                    if block_type == 'Pickup':
                        color = (0, 255, 0)  # green color for pickup cell
                    elif block_type == 'Dropoff':
                        color = (0, 0, 255)  # red color for dropoff cell
                    cv2.rectangle(
                        grid, top_left, (top_left[0] + block_size, top_left[1] + block_size), color, -1)

                    # draw agent in a cell
                    if agent is not None:
                        self.getLocation(agent)
                        cv2.circle(grid, (int(top_left[0] + block_size/2), int(top_left[1] + block_size/2)), int(
                            block_size/4), (255, 255, 0), -1)  # yellow circle for agent

        cv2.imshow('State Space', grid)
        cv2.waitKey(0)

    def printSS(self):
        """
        prints information about each cell in state_space
        """
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    cell = self.state_space[x, y, z]
                    print(f"({x+1},{y+1},{z+1})\n"
                          f"\ttype:\t{cell.getType()}\n"
                          f"\tagent:\t{cell.whichAgent()}\n"
                          f"\tblocks:\t{cell.getNumBlocks()}\n"
                          f"\tcost:\t{cell.getCost()}")

    def complete(self):
        """
        returns True if all Pickup cells contain 5 blocks and False otherwise
        """
        loc = self.locDrop
        if (self.state_space[loc[0, 0], loc[0, 1], loc[0, 2]].numBlocks == 5 and
           self.state_space[loc[1, 0], loc[1, 1], loc[1, 2]].numBlocks == 5 and
           self.state_space[loc[2, 0], loc[2, 1], loc[2, 2]].numBlocks == 5 and
           self.state_space[loc[3, 0], loc[3, 1], loc[3, 2]].numBlocks == 5):
            return True
        else:
            return False