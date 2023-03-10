import numpy as np

class Cell:
    def __init__(self):
        self.type = 'Basic'
        self.occupancy = ['None'] # better way to do this?
        self.numBlocks = 0
    
    # type methods
    def getType(self): # Basic, Pickup, Dropoff, Risk
        return self.type
    def setType(self, _type):
        if _type == 'Pickup':
            self.numBlocks = 10
        self.type = _type
    
    # agent methods
    def isOccupied(self):
        return self.occupancy[0] != 'None' # returns false if unoccupied
    def whichAgent(self):
        if self.isOccupied: # unnecessary check w/ current implementation
            return self.occupancy[0]
    def addAgent(self, _agent):
        self.occupancy.remove('None')
        self.occupancy.append(_agent)
    def rmAgent(self, _agent):
        self.occupancy.remove(_agent)
        self.occupancy.append('None')

    # block methods
    def getNumBlocks(self):
        return self.numBlocks
    def addBlock(self):
        if self.type == 'Dropoff' and self.numBlocks < 5: # capacity is 5 blocks
            self.numBlocks += 1
    def rmBlock(self):
        if self.numBlocks > 0:
            self.numBlocks -= 1

StateSpace = np.empty(shape=(3,3,3), dtype=object, order='C') # 'C' means row-major order in memory

# initialize StateSpace as all basic cells
for x in range(StateSpace.shape[0]):
    for y in range(StateSpace.shape[1]):
        for z in range(StateSpace.shape[2]):
            StateSpace[x,y,z] = Cell()

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

# visualize SS
for z in range(StateSpace.shape[0]):
    for y in range(StateSpace.shape[1]):
        for x in range(StateSpace.shape[2]):
            cell = StateSpace[x,y,z]
            print(f"location: ({x},{y},{z})\n\ttype: {cell.getType()}\n" +
                  f"\tnumber of blocks: {cell.getNumBlocks()}\n" +
                  f"\twhich agent: {cell.whichAgent()}\n")