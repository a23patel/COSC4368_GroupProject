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

    # reinforcement learning state space
    RLW = VSSpace()

    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    policyF = PRandom('F', RLW, actions, seed=1)
    policyM = PRandom('M', RLW, actions, seed=1)

    iState = RW.get_state_representation()
    agentF = QLAgent('F', RLW, policyF, iState)
    agentM = QLAgent('M', RLW, policyM, iState)

    q = Queue(maxsize=2)
    q.put('F')
    q.put('M')

    # stores the rewards obtained for analytics
    rewardList = []

    # stores the distance between agents for analytics
    distList = []
    
    # number of iterations
    n = 0
    while True:
        # 'F' or 'M'
        curAgent = q.get()
       
        # choose action
        state = RW.get_state_representation()
        if curAgent == 'F':
            action = agentF.choose_action(state)
        if curAgent == 'M':
            action = agentF.choose_action(state)
        
        # perform action
        reward = RW.perform_action(curAgent, action)

        # agent updates its Qtable
        newState = RW.get_state_representation()
        if curAgent == 'F':
            # args: new_state, reward
            agentF.update(newState, reward)
        if curAgent == 'M':
            agentM.update(newState, reward)
        
        rewardList.append(reward)
        
        # check completion criterion
        if RW.is_complete():
            break

        # TODO visualization
        if n+1 % 5000 == 0:
            RW.print_ss()

        # store distance between agents after 'M' moves
        if n % 2 != 0:
            distList.append(distance(RW.locF, RW.locM))

        q.put(curAgent)
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
    RW.print_ss()
    print('##################################################')
    RW.perform_action('F','N')
    RW.perform_action('F','E')
    RW.perform_action('F','Pickup') # TODO fix
    RW.perform_action('F','S')
    RW.perform_action('F','E')
    RW.perform_action('F','Dropoff') # TODO fix
    RW.print_ss()
    # expecting the following:
    # F at Dropoff (3,1,1) with 1 block
    # Pickup (2,2,1) has 9 blocks

    # visualize the StateSpace
    # ss.visualize()

if __name__ == "__main__":
    main()