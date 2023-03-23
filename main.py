# Experiment 1

from queue import Queue
from stateSpace import StateSpace
from action import Action
from agent import QLAgent, SARSAAgent, VSAgent, VSQRandomAgent
from policy import PGreedy, PExploit, PRandom

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
          + abs(locF[1] - locM[1])
          + abs(locF[2] - locM[2]))

# main event loop
def main():
    
    q = Queue(maxsize=2)
    q.put('F') # always goes first
    q.put('M')

    RW = StateSpace('original')
    a = Action()
    agent = QLAgent()
    distList = []
    
    n = 0
    while True:
        
        # F or M
        whichAgent = q.get()
        
        if RW.carF:
            i = 1
        else:
            i = 0
        if RW.carM:
            iPrime = 1
        else:
            iPrime = 0

        # state of RW
        state = [RW.locF[0], RW.locF[1], RW.locF[2], # x, y, z,
                 RW.locM[0], RW.locM[1], RW.locM[2], # x', y', z',
                 i, iPrime,                          # i, i',
                 RW.locPick[0].getNumBlocks(),       # a,
                 RW.locPick[1].getNumBlocks(),       # b,
                 RW.locPick[2].getNumBlocks(),       # c,
                 RW.locPick[3].getNumBlocks(),       # d,
                 RW.locDrop[0].getNumBlocks(),       # e,
                 RW.locDrop[1].getNumBlocks()]       # f,
        
        # choose action
        action = agent.chooseAction(state) # or RW obj instead of state?
        
        # perform action (assuming action is a character)
        RW.performAction(whichAgent, action)

        # TODO rewards

        # agent updates its Qtable
        agent._update_table()

        # check completion criterion
        if RW.complete():
            break

        # visualization 
        if n % 1000 == 0: # every 1000 moves
            RW.printSS()

        # store distance between agents after M moves
        if n % 2 != 0:
            distList.append(distance(RW.locF, RW.locM))

        q.put(whichAgent)
        n += 1


    # testing StateSpace & Action classes
    
    # female agent
    # move to nearest pickup cell
    # RW.printSS()
    # print('##################################################')
    # RW.performAction('F','N')
    # RW.performAction('F','E')
    # RW.performAction('F','Pickup')
    # RW.performAction('F','S')
    # RW.performAction('F','E')
    # RW.performAction('F','Dropoff')
    # RW.printSS()

    # visualize the StateSpace
    # ss.visualize()

if __name__ == "__main__":
    main()