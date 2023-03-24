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


def experiment(id, seed):
    """
    Implements the event loop for experiments
    arguments:
    id - '1a', '1b', '1c', '2', '3a', '3b', '4'
    seed - seed value for reproducibility
    """
    if id == '1a' or id == '1b' or id == '1c' or id == '2' or id == '4':
        alpha = 0.3
    if id == '3a':
        alpha = 0.1
    if id == '3b':
        alpha = 0.5
    gamma = 0.5

    # real world state space
    RW = StateSpace('original')

    # reinforcement learning state space
    RLW = VSSpace()

    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    policyF = PRandom('F', RLW, actions, seed=seed)
    policyM = PRandom('M', RLW, actions, seed=seed)

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

    # number of terminal states reached
    terminal = 0

    # number of iterations
    n = 0
    while True:
        # 'F' or 'M'
        curAgent = q.get()

        # choose action
        if n == 0:
            state = iState
        if curAgent == 'F':
            action = agentF.choose_action(state)
        if curAgent == 'M':
            action = agentM.choose_action(state)

        # perform action
        reward = RW.perform_action(curAgent, action)

        # agent updates its Qtable
        state = RW.get_state_representation()
        if curAgent == 'F':
            agentF.update(state, reward)
        if curAgent == 'M':
            agentM.update(state, reward)

        rewardList.append(reward)

        # check completion criterion
        if RW.is_complete():
            terminal += 1
            if id == '4' and (terminal == 1 or terminal == 2):
                RW = StateSpace('original')
            if id == '4' and (terminal == 3 or terminal == 4 or terminal == 5):
                RW = StateSpace('modified')
            if id == '4' and terminal == 6:
                break
            if id != '4':
                RW = StateSpace('original')

        # TODO visualization
        if n+1 % 5000 == 0:
            RW.print_ss()
        # RW.visualize()

        # store distance between agents after 'M' moves
        if n % 2 != 0:
            distList.append(distance(RW.locF, RW.locM))

        q.put(curAgent)
        n += 1

        # switch policy after first 500 moves for 1b, 1c, 2
        if id != '1a':
            if n == 500:
                if id == '1b':
                    policyF = PGreedy('F', RLW, actions, seed=seed)
                    policyM = PGreedy('M', RLW, actions, seed=seed)
                if id == '1c' or id == '3' or id == '4':
                    policyF = PExploit('F', RLW, actions, seed=seed)
                    policyM = PExploit('M', RLW, actions, seed=seed)
                # TODO
                if id == '2':
                    # run the SARSA q-learning variation for 9500 steps
                    pass

        # stop after 10,000 moves
        if n == 10000:
            break


def main():
    """
    Driver code to conduct experiments
    """
    # experiment('1a', 1)
    # experiment('1a', 42)

    # experiment('1b', 1)
    # experiment('1b', 42)

    # experiment('1c', 1)
    # experiment('1c', 42)

    # experiment('2', 1)
    # experiment('2', 42)

    # experiment('3a', 1)
    # experiment('3a', 42)

    # experiment('3b', 1)
    # experiment('3b', 42)

    # experiment('4', 1)
    # experiment('4', 42)

    # testing rewards
    # RW = StateSpace('original')
    # RW.print_ss()
    # print('##################################################')
    # print(RW.perform_action('F','N')) # -1
    # print(RW.perform_action('F','E')) # -1
    # print(RW.perform_action('F','Pickup')) # 14
    # print(RW.perform_action('F','S')) # -1
    # print(RW.perform_action('F','E')) # -1
    # print(RW.perform_action('F','Dropoff')) # -14
    # RW.print_ss()
    # # expecting the following:
    # # F at Dropoff (3,1,1) with 1 block
    # # Pickup (2,2,1) has 9 blocks

    # # test risk reward
    # print(RW.perform_action('F','N')) # -1
    # print(RW.perform_action('F','N')) # -2 bc risk cell

    # testing get_state_representation function
    # expecting [0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 10, 10]
    # RW = StateSpace('original')
    # state = RW.get_state_representation()
    # print(state)
    # # slice locF
    # locF = state[0:3]
    # print(locF)
    # locM = state[3:6]
    # print(locM)


if __name__ == "__main__":
    main()
