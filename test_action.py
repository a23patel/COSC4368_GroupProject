from stateSpace import StateSpace
from action import Action

# TODO replace with unit tests

# test constructors
RW = StateSpace('original')
# RW.print_ss()
# print('##################################################')
# RW_modified = StateSpace('modified')
# RW_modified.print_ss()

# test actions
rewards = []
rewards.append(RW.perform_action('F','N'))       # -1
rewards.append(RW.perform_action('F','E'))       # -1
rewards.append(RW.perform_action('F','Pickup'))  # 14
rewards.append(RW.perform_action('F','S'))       # -1
rewards.append(RW.perform_action('F','E'))       # -1
rewards.append(RW.perform_action('F','Dropoff')) # -14
# expecting F at Dropoff (3,1,1) with 1 block & Pickup (2,2,1) has 9 blocks
RW.print_ss() 

# test rewards, expecting [-1,-1,14,-1,-1,14,-1,-2]
rewards.append(RW.perform_action('F','N'))       # -1
rewards.append(RW.perform_action('F','N'))       # -2
print(rewards)

# test get_state_representation function
# expecting [2, 2, 0, 2, 1, 2, 0, 0, 0, 0, 1, 0, 9, 10]
state = RW.get_state_representation()
print(state)
# expecting [0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 10, 10]
RW = StateSpace('original')
state = RW.get_state_representation()
print(state)