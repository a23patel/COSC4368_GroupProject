from queue import Queue
from stateSpace import StateSpace
from action import Action
from agent import QLAgent, SARSAAgent, VSAgent, VSQRandomAgent, VSSpace
from policy import PGreedy, PExploit, PRandom

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
          + abs(locF[1] - locM[1])
          + abs(locF[2] - locM[2]))

def experiment_1(subExperiment):
    """
    Implements the main event loop for experiment 1
    argument:
    subExperiment - 'a', 'b', or 'c' to run each sub experiment
    """
    alpha = 0.3
    gamma = 0.5

    # real world state space
    RW = StateSpace('original')

    # reinforcement learning world state space
    RLW = VSSpace()

    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    policyF = PRandom('F', RLW, actions, seed=1)
    policyM = PRandom('M', RLW, actions, seed=1)

    agentF = QLAgent('F', RLW, policyF, RW)
    agentM = QLAgent('M', RLW, policyM, RW)

    q = Queue(maxsize=2)
    q.put('F')
    q.put('M')

    # stores the distance between agents for analytics
    distList = []
    
    # number of iterations
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
        if whichAgent == 'F':
            action = agentF.chooseAction(state)
        if whichAgent == 'M':
            action = agentF.chooseAction(state)
        
        # perform action (assuming action is a character)
        RW.performAction(whichAgent, action)

        # TODO rewards

        # agent updates its Qtable
        if whichAgent == 'F':
            agentF._update_table()
        if whichAgent == 'M':
            agentM._update_table()
        
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

        # switch policy after first 500 moves for 1b & 1c
        if subExperiment != 'a':
            if n == 500:
                if subExperiment == 'b':
                    policyF = PGreedy('F', RLW, actions, seed=1)
                    policyM = PGreedy('M', RLW, actions, seed=1)
                if subExperiment == 'c':
                    policyF = PExploit('F', RLW, actions, seed=1)
                    policyM = PExploit('M', RLW, actions, seed=1)
        
        # stop after 10,000 moves
        if n == 10000:
            break

def main():
    
    # testing StateSpace & Action classes
    RW = StateSpace('original')
    RW.printSS()
    print('##################################################')
    RW.performAction('F','N')
    RW.performAction('F','E')
    RW.performAction('F','Pickup')
    RW.performAction('F','S')
    RW.performAction('F','E')
    RW.performAction('F','Dropoff')
    RW.printSS()

    # visualize the StateSpace
    # ss.visualize()

if __name__ == "__main__":
    main()