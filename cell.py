import numpy as np
import cv2

class Cells:
    def __init__(self):
        self.type = 'Basic'
        self.occupancy = []
        self.num_blocks = 0
        self.cost = -1   # default cost in traversing blocks to a particular cell is -1 for Basic cells 
    
    # type methods
    def getType(self):   # Basic, Pickup, Dropoff, Risk
        return self.type
    def setType(self, _type):
        if _type == 'Pickup':
            self.numBlocks = 10
        if _type == 'Risk':
            self.cost = -2
        self.type = _type
    
    # agent methods
    def is_occupied(self):
        return bool(self.occupancy)  # returns false if occupancy list is empty
    def whichAgent(self):
        if self.is_occupied():
            return self.occupancy[0]
    def addAgent(self, _agent):
        if not(self.is_occupied()):
            self.occupancy.append(_agent)
    def removeAgent(self, _agent):
        if self.is_occupied():
            self.occupancy.remove(_agent)

    # block methods
    def getNumBlocks(self):
        return self.num_blocks
    def addBlock(self):
        if self.type == 'Dropoff' and self.num_blocks < 5:   # capacity is 5 blocks
            self.numBlocks += 1
    def removeBlock(self):
        if self.numBlocks > 0:
            self.numBlocks -= 1
    def getCost(self):
        return self.cost


class StateSpace:
    def __init__(self):
        self.state_space = np.empty(shape=(3,3,3), dtype=object, order='C')   # 'C' means row-major order in memory

        # initializing StateSpace as all basic cells
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    self.state_space[x,y,z] = Cells()
        

        # agent locations
        agent1 = Cells()
        agent1.addAgent('F')
        self.state_space[0, 0, 0] = agent1

        agent2 = Cells()
        agent2.addAgent('M')
        self.state_space[2, 1, 2] = agent2
        
        #pickup cells
        pickup1 = Cells()
        pickup1.setType('Pickup')
        self.state_space[1, 1, 0] = pickup1

        pickup2 = Cells()
        pickup2.setType('Pickup')
        self.state_space[2, 2, 1] = pickup2
        # dropoff cells
        dropoff1 = Cells()
        dropoff1.setType('Dropoff')
        self.state_space[0, 0, 1] = dropoff1

        dropoff2 = Cells()
        dropoff2.setType('Dropoff')
        self.state_space[0, 0, 2] = dropoff2

        dropoff3 = Cells()
        dropoff3.setType('Dropoff')
        self.state_space[2, 0, 0] = dropoff3

        dropoff4 = Cells()
        dropoff4.setType('Dropoff')
        self.state_space[2, 1, 2] = dropoff4
    
    def getLocation(self, agent):
        for x in range(self.state_space.shape[0]):
            for y in range(self.state_space.shape[1]):
                for z in range(self.state_space.shape[2]):
                    if self.state_space[x,y,z].whichAgent() == agent:
                        return (x+1,y+1,z+1)
                    
    def visualize(self):
        block_size = 50  # size of each cell in pixels
        grid_width = self.state_space.shape[0] * block_size
        grid_height = self.state_space.shape[1] * block_size

        grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)  # initialize grid as black image

        cell = Cells()

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

# create a StateSpace instance
ss = StateSpace()

# visualize the StateSpace
ss.visualize()
