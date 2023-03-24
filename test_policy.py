from stateSpace import StateSpace
from policy import Policy, PRandom
from agent import QLAgent, VSSpace

# TODO replace with unit tests

# test get_applicable actions function
RW = StateSpace('original')
RLW = VSSpace()
actions = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']
policy = Policy('F', RLW, actions, seed=1)
# expecting ['N', 'E', 'U']
print(policy.get_applicable_actions(RW))