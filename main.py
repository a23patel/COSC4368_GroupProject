from queue import Queue
from stateSpace import StateSpace
from action import Action
from agent import Agent
from rlw import VSSpace, SSSpace, CSpace, C2Space, SSV1Space
from policy import PGreedy, PExploit, PRandom
import argparse
import copy
import csv

# Manhattan
def distance(locF, locM):
    return (abs(locF[0] - locM[0])
            + abs(locF[1] - locM[1])
            + abs(locF[2] - locM[2]))

def write_actions(agentFActions, agentMActions, id, seed, rewardList, distList):
    with open('f_actions', 'w', encoding="utf-8") as f:
        for action in agentFActions:
            f.write('%s\n' % action)
    with open('m_actions', 'w', encoding="utf-8") as f:
        for action in agentMActions:
            f.write('%s\n' % action)
    with open('experiment_id', 'w', encoding="utf-8") as f:
        f.write(id)
    with open('experiment_seed', 'w', encoding="utf-8") as f:
        f.write(seed)
    with open('var_visualization.csv', 'w', newline='',encoding="utf-8") as f:
        write = csv.writer(f, delimiter='\t')
        write.writerow(['Index','Rewards', ' Distance'])
        for i, (rewards, distance) in enumerate(zip(rewardList, distList)):
            write.writerow([f"{i:<10}{rewards:<10}{distance}"])
            
def write_table(agentFtable, agentMtable):
    with open('f_table.txt', 'w', encoding="utf-8") as f:
        for table in agentFtable:
            f.write('%s\n' % str(table))
    with open('m_table.txt', 'w', encoding="utf-8") as f:
        for table in agentMtable:
            f.write('%s\n' % str(table))

def experiment(id, seed, produce_history, dump_table, rl_type):
    """
    Implements the event loop for experiments
    arguments:
    id - '1a', '1b', '1c', '2', '3a', '3b', '4'
    seed - seed value for reproducibility
    produce_history - 
    dumpy_table - 
    rl_type - 
    """
    alpha = 0.3
    
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

    # reinforcement learning state space
    RLW = SSSpace()
    if rl_type == 'ss':
        RLW = SSSpace()
    elif rl_type == 'vs':
        RLW = VSSpace()
    elif rl_type == 'cs':
        RLW = CSpace()
    elif rl_type == 'c2':
        RLW = C2Space()
    elif rl_type == 'ssv1':
        RLW = SSV1Space()
    
    actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

    policyF = PRandom('F', RLW, actions, seed=seed)
    policyM = PRandom('M', RLW, actions, seed=seed)

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

    # stores the qtable dumps of agent 'F'
    agentFtable = []

    # stores the qtable dumps of agent 'M'
    agentMtable = []

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
            if produce_history:
                agentFActions.append(action)
        elif curAgent == 'M':
            action = agentM.choose_action(RW)
            if produce_history:
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

        # dump qtable
        if dump_table:
            if curAgent == 'F':
                agentFtable.append(agentF.extract_table(copy.deepcopy(RW)))
            elif curAgent == 'M':
                agentMtable.append(agentM.extract_table(copy.deepcopy(RW)))

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
                if produce_history:
                    write_actions(agentFActions, agentMActions, id, str(seed), rewardList, distList)
                if dump_table:
                    #print(agentFtable)
                    write_table(agentFtable, agentMtable)
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
            if produce_history:
                write_actions(agentFActions, agentMActions, id, str(seed), rewardList, distList)
            if dump_table:
                #print(agentFtable)
                write_table(agentFtable, agentMtable)
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
    arg_parser.add_argument("--dump-tables",
        dest="dump_tables",
        help="Dump Q-tables to files m_table.txt and f_table.txt",
        required=False,
        action="store_true")
    arg_parser.add_argument("--rl",
        dest="rl_type",
        help="Choose RL state space type",
        required=False,
        type=str,
        default='ss')
    args = arg_parser.parse_args()
    experiment(args.experiment, 
               args.seed, 
               args.produce_history, 
               args.dump_tables, 
               args.rl_type)

if __name__ == "__main__":
    main()
