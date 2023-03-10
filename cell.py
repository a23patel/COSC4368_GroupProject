import numpy as np

class Cell:
    def __init__(self):
        self.type = 'Basic'
        self.occupancy = []
        self.numBlocks = 0
        # cost? = -1 for Basic & = -2 for Risk cells
    
    # type methods
    def getType(self): # Basic, Pickup, Dropoff, Risk
        return self.type
    def setType(self, _type):
        if _type == 'Pickup':
            self.numBlocks = 10
        self.type = _type
    
    # agent methods
    def occupied(self):
        return self.occupancy # returns false if occupancy list is empty
    def whichAgent(self):
        if self.occupied():
            return self.occupancy[0]
    def addAgent(self, _agent):
        if not(self.occupied()):
            self.occupancy.append(_agent)
    def rmAgent(self, _agent):
        if self.occupied():
            self.occupancy.remove(_agent)

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

# visualize SS to compare to assignment description
for z in range(StateSpace.shape[0]):
    for y in range(StateSpace.shape[1]):
        for x in range(StateSpace.shape[2]):
            cell = StateSpace[x,y,z]
            print(f"location: ({x+1},{y+1},{z+1})\n\ttype: {cell.getType()}\n" +
                  f"\tnumber of blocks: {cell.getNumBlocks()}\n" +
                  f"\twhich agent: {cell.whichAgent()}\n")