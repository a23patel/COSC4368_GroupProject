from cell import Cell
from action import Action
import numpy as np
import cv2

class StateSpace:
    def __init__(self):
        """
        Constructor for RW state space.

        Properties:
        state_space - a 3D NumPy array of Cells
        locF - (x,y,z) coordinates of female agent
        locM - (x,y,z) coordinates of male agent
        carF - True if female agent is carrying a block and False otherwise
        carM - True if male agent is carrying a block and False otherwise
        locDrop - list of (x,y,z) coordinates of each Dropoff cell
        ...
        """
        self.state_space = np.empty(shape=(3,3,3), dtype=object, order='C')   # 'C' means row-major order in memory
        self.locF = None
        self.locM = None

        # trying this out
        self.carF = False
        self.carM = False

        self.locDrop = []
        self.package = None 

        self.pickupLocations = [] # do we need this?
    
        # initializing state_space as all basic cells
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x,y,z] = Cell()
        
        # female agent
        self.state_space[0,0,0].addAgent('F')
        self.locF = [0,0,0]

        # male agent
        self.state_space[2,1,2].addAgent('M')
        self.locM = [2,1,2]
        
        # pickup cells
        self.state_space[1,1,0].setType('Pickup')
        self.pickupLocations.append([1,1,0])
        self.state_space[2,2,1].setType('Pickup')
        self.pickupLocations.append([2,2,1])

        # dropoff cells
        self.state_space[0,0,1].setType('Dropoff')
        self.locDrop.append([0,0,1])
        self.state_space[0,0,2].setType('Dropoff')
        self.locDrop.append([0,0,2])
        self.state_space[2,0,0].setType('Dropoff')
        self.locDrop.append([2,0,0])
        self.state_space[2,1,2].setType('Dropoff')
        self.locDrop.append([2,1,2])

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

    def isCarrying(self):
        return self.package is not None
    
    # checking if an agent is carrying a package/block corresponding to the location of the agent
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
        return self.state_space[loc[0],loc[1],loc[2]].getType() == 'Pickup'
    
    def isDropoff(self, loc):
        """
        returns True if cell is Dropoff and False otherwise
        argument:
        loc - (x,y,z) coordinates of a cell
        """
        return self.state_space[loc[0],loc[1],loc[2]].getType() == 'Dropoff'
    
    # remove?
    # def modifyLocation(self, old_loc, new_loc):
    #     # getting the cell object at the old location
    #     old_cell = self.state_space[old_loc[0], old_loc[1], old_loc[2]]
        
    #     # getting the cell object at the new location
    #     new_cell = self.state_space[new_loc[0], new_loc[1], new_loc[2]]
        
    #     # check if the new location is already occupied
    #     if new_cell.is_occupied():
    #         return False
        
    #     # updating the list of pickup or dropoff locations
    #     if new_cell.getType() == 'Pickup':
    #         self.pickupLocations.remove(old_loc)
    #         self.pickupLocations.append(new_loc)
    #     else:
    #         self.locDrop.remove(old_loc)
    #         self.locDrop.append(new_loc)
        
        
    #     return True
    
    def moveAgent(self, agent, direction):
        """
        changes the location of agent and updates state_space accordingly
        arguments:
        agent - 'F' for female agent; 'M' for male agent
        direction - 'E', 'W', 'N', 'S', 'U', or 'D'
        """
        if agent == 'F':
            loc = self.locF
        elif agent == 'M':
            loc = self.locM

        # apply action to agent location to get new location
        a = Action()
        if direction == 'E':
            newLoc = a.moveEast(loc, self)
        if direction == 'W':
            newLoc = a.moveWest(loc, self)
        if direction == 'N':
            newLoc = a.moveNorth(loc, self)
        if direction == 'S':
            newLoc = a.moveSouth(loc, self)
        if direction == 'U':
            newLoc = a.moveUp(loc, self)
        if direction == 'D':
            newLoc = a.moveDown(loc, self)

        # update state space
        self.state_space[loc[0],loc[1],loc[2]].removeAgent(agent)
        self.state_space[newLoc[0],newLoc[1],newLoc[2]].addAgent(agent)
    
        # update agent location
        if agent == 'F':
            self.locF = newLoc
        elif agent == 'M':
            self.locM = newLoc

    def visualize(self):
        block_size = 50  # size of each cell in pixels
        grid_width = self.state_space.shape[0] * block_size
        grid_height = self.state_space.shape[1] * block_size

        grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)  # initialize grid as black image

        cell = Cell()

        # draw cells onto the grid
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x,y,z]
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
                    cv2.rectangle(grid, top_left, (top_left[0] + block_size, top_left[1] + block_size), color, -1)

                    # draw agent in a cell
                    if agent is not None:
                        self.getLocation(agent)
                        cv2.circle(grid, (int(top_left[0] + block_size/2), int(top_left[1] + block_size/2)), int(block_size/4), (255, 255, 0), -1)  # yellow circle for agent

        cv2.imshow('State Space', grid)
        cv2.waitKey(0)

    def printSS(self):
        """
        prints information about each cell in state_space
        """
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    cell = self.state_space[x,y,z]
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
        if(self.state_space[loc[0,0],loc[0,1],loc[0,2]].numBlocks == 5 and
           self.state_space[loc[1,0],loc[1,1],loc[1,2]].numBlocks == 5 and
           self.state_space[loc[2,0],loc[2,1],loc[2,2]].numBlocks == 5 and
           self.state_space[loc[3,0],loc[3,1],loc[3,2]].numBlocks == 5):
            return True
        else:
            return False

# visualize the StateSpace
# ss.visualize()