from queue import Queue
from stateSpace import StateSpace
from action import Action
from agent import Agent
from rlw import VSSpace, SSSpace
from policy import PGreedy, PExploit, PRandom
import argparse

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
            + abs(locF[1] - locM[1])
            + abs(locF[2] - locM[2]))

def write_actions(agentFActions, agentMActions):
    # write move lists to files
    with open('f_actions', 'w', encoding="utf-8") as f:
        for action in agentFActions:
            f.write('%s\n' % action)
    with open('m_actions', 'w', encoding="utf-8") as f:
        for action in agentMActions:
            f.write('%s\n' % action)

def experiment(id, seed):
    """
    Implements the event loop for experiments
    arguments:
    id - '1a', '1b', '1c', '2', '3a', '3b', '4'
    seed - seed value for reproducibility
    """
    print(f"\n### Experiment {id} running with seed {seed} ###\n")
    if id == '1a' or id == '1b' or id == '1c' or id == '2' or id == '4':
        alpha = 0.3
    elif id == '3a':
        alpha = 0.1
    elif id == '3b':
        alpha = 0.5
    gamma = 0.5

    # real world state space
    RW = StateSpace('original')

    # TODO add an argument to determine this?
    # reinforcement learning state space
    # RLW = VSSpace()
    RLW = SSSpace()

    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    policyF = PRandom('F', RLW, actions, seed=seed)
    policyM = PRandom('M', RLW, actions, seed=seed)

    # TODO pass list or obj? -> agent needs RW object
    agentF = Agent('F', RLW, policyF, RW, alpha, gamma)
    agentM = Agent('M', RLW, policyM, RW, alpha, gamma)

    q = Queue(maxsize=2)
    q.put('F')
    q.put('M')

    # stores the rewards obtained for analytics
    rewardList = []

    # stores the distance between agents for analytics
    distList = []

    # stores the actions taken by agent 'F'
    agentFActions = []

    # stores the actions taken by agent 'M'
    agentMActions = []

    # number of terminal states reached
    terminal = 0

    # number of iterations
    n = 0

    # number of actions between terminal states
    numActions = 0

    # just terminated flag
    justTerminated = False

    while True:
        # 'F' or 'M'
        curAgent = q.get()

        # choose action
        if curAgent == 'F':
            action = agentF.choose_action(RW)
            agentFActions.append(action)
        elif curAgent == 'M':
            action = agentM.choose_action(RW)
            agentMActions.append(action)

        # perform action
        reward = RW.perform_action(curAgent, action)
        numActions += 1

        # update qtable
        if curAgent == 'F':
            agentF.update(RW, reward)
        elif curAgent == 'M':
            agentM.update(RW, reward)

        rewardList.append(reward)

        if RW.is_first_dropoff_filled():
            # TODO dump qtable
            pass

        # check completion criterion
        if RW.is_complete():
            justTerminated = True
            # TODO dump qtable
            terminal += 1
            print(f"Terminal state {terminal} reached after {numActions} actions\n")
            numActions = 0
            if id == '4' and (terminal == 1 or terminal == 2):
                RW = StateSpace('original')
                # empty queue and load F first then M
                q.get()
                q.put('F')
                q.put('M')
            elif id == '4' and (terminal == 3 or terminal == 4 or terminal == 5):
                if terminal == 3:
                    print("Pickup locations modified\n")
                RW = StateSpace('modified')
                # empty queue and load F first then M
                q.get()
                q.put('F')
                q.put('M')
            elif id == '4' and terminal == 6:
                print(f"Total number of terminal states reached: {terminal}") # 6
                write_actions(agentFActions, agentMActions)
                break
            elif id != '4':
                RW = StateSpace('original')
                # empty queue and load F first then M
                q.get()
                q.put('F')
                q.put('M')

        # TODO visualization in pyGame
        if n % (250-1) == 0:
            print(RW.get_state_representation())
        # RW.visualize()

        # store distance between agents after 'M' moves
        if n % 2 != 0:
            distList.append(distance(RW.locF, RW.locM))
        
        if not justTerminated:
            q.put(curAgent)
        
        justTerminated = False
        
        n += 1

        # switch policy after first 500 moves for 1b, 1c, 2, 3, & 4
        if id != '1a':
            if n == 500:
                if id == '1b':
                    agentF.set_policy(PGreedy('F', RLW, actions, seed=seed))
                    agentM.set_policy(PGreedy('M', RLW, actions, seed=seed))
                elif id == '1c' or id == '2' or id == '3' or id == '4':
                    agentF.set_policy(PExploit('F', RLW, actions, seed=seed))
                    agentM.set_policy(PExploit('M', RLW, actions, seed=seed))
                if id == '2':
                    # run the SARSA q-learning variation for 9500 steps
                    agentF.set_learning('sarsa')
                    agentM.set_learning('sarsa')

        # stop after 10,000 moves
        if n == 10000:
            # TODO dump qtable
            print(f"\nTotal number of terminal states reached: {terminal}")
            write_actions(agentFActions, agentMActions)
            break


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("experiment", help="Experiment to run", type=str)
    arg_parser.add_argument("seed", help="Random seed to use", type=int)
    arg_parser.add_argument("--history",
        dest="produce_history",
        help="Produce history for visualization",
        required=False,
        action="store_true")
    args = arg_parser.parse_args()
    experiment(args.experiment, args.seed)

if __name__ == "__main__":
    main()
