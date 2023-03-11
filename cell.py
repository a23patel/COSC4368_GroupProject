import numpy as np

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
        if _type == 'Basic':
            self.cost = -1
        elif _type == 'Risk':
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
        if self.is_occupied():
            return None
        elif self.type == 'Basic' or self.type == 'Risk':
            return self.cost
        else:
            return self.num_blocks    


#creating the state space
StateSpace = np.empty(shape=(3,3,3), dtype=object, order='C')    # 'C' means row-major order in memory

# initialize StateSpace as all basic cells
for x in range(StateSpace.shape[0]):
    for y in range(StateSpace.shape[1]):
        for z in range(StateSpace.shape[2]):
            StateSpace[x,y,z] = Cells()

# update cells according to http://www2.cs.uh.edu/~ceick/ai/2023-World.pptx

# agent locations
StateSpace[0,0,0].addAgent('F')
StateSpace[2,1,2].addAgent('M')

# pickup cells
StateSpace[1,1,0].setType('Pickup')
StateSpace[2,2,1].setType('Pickup')

# dropoff cells
StateSpace[0,0,1].setType('Dropoff')
StateSpace[0,0,2].setType('Dropoff')
StateSpace[2,0,0].setType('Dropoff')
StateSpace[2,1,2].setType('Dropoff')

# visualizing state space to compare to project description
for x in range(StateSpace.shape[0]):
    for y in range(StateSpace.shape[1]):
        for z in range(StateSpace.shape[2]):
            cell = StateSpace[x,y,z]
            print(f"Location of blocks: ({x+1},{y+1},{z+1})\n\tType of Block: {cell.getType()}\n" +
                  f"\tNumber of blocks: {cell.getNumBlocks()}\n" +
                  f"\tAgent: {cell.whichAgent()}\n" +
                  f"\tCost of traversing blocks: {cell.getCost()}\n")