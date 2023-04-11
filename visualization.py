import pygame
import os
from pygame.font import Font
from queue import Queue
import numpy as np

################## GLOBALS ##################

# controls overall size
SCALE = 1

# window
WIDTH, HEIGHT = (SCALE*1200), (SCALE*400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning Visualization")

# colors
WHITE = (255, 255, 255)
LIGHT_YELLOW = (255, 255, 204)
PURPLE = (128, 0, 128)

# speed of execution
FPS = 3

# import assets

# 3x3 grid
Z_LEVEL = pygame.image.load(os.path.join('assets', 'grid.png'))

# grid labels
# Create font object and set font size
pygame.font.init()
font = Font(None, int(SCALE*28))
# Create text surfaces for the labels
Z1_LABEL = font.render('z=1', True, PURPLE)
Z2_LABEL = font.render('z=2', True, PURPLE)
Z3_LABEL = font.render('z=3', True, PURPLE)

# Pickup, Dropoff, Risk cell labels
P = pygame.image.load(os.path.join('assets','p_pix.png'))
D = pygame.image.load(os.path.join('assets','d_pix.png'))
R = pygame.image.load(os.path.join('assets','r_pix.png'))

# agents
FEMALE_AGENT = pygame.image.load(os.path.join('assets', 'female_agent.png'))
FEMALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'female_agent_simple.png'))
MALE_AGENT = pygame.image.load(os.path.join('assets', 'male_agent.png'))
MALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'male_agent_simple.png'))

# block to pickup/dropoff
BLOCK = pygame.image.load(os.path.join('assets', 'block.png'))

# define new asset sizes
RESIZED_Z_LEVEL = (SCALE*360,SCALE*360)
RESIZED_LETTERS = (SCALE*35,SCALE*45)
RESIZED_AGENTS = (SCALE*35,SCALE*45)
RESIZED_BLOCK = (SCALE*25,SCALE*25)

# resize assets
grid = pygame.transform.scale(Z_LEVEL,RESIZED_Z_LEVEL)
p = pygame.transform.scale(P,RESIZED_LETTERS)
d = pygame.transform.scale(D,RESIZED_LETTERS)
r = pygame.transform.scale(R,RESIZED_LETTERS)
f_not_carrying = pygame.transform.scale(FEMALE_AGENT_SIMPLE,RESIZED_AGENTS)
f_carrying = pygame.transform.scale(FEMALE_AGENT,RESIZED_AGENTS)
m_not_carrying = pygame.transform.scale(MALE_AGENT_SIMPLE,RESIZED_AGENTS)
m_carrying = pygame.transform.scale(MALE_AGENT,RESIZED_AGENTS)
block = pygame.transform.scale(BLOCK,RESIZED_BLOCK)

# asset locations

# z levels
Z1_LOCATION = (SCALE*10,SCALE*10)
Z2_LOCATION = (SCALE*420,SCALE*10)
Z3_LOCATION = (SCALE*830,SCALE*10)

# grid labels
Z1_LABEL_LOCATION = (SCALE*178,SCALE*373)
Z2_LABEL_LOCATION = (SCALE*579,SCALE*373)
Z3_LABEL_LOCATION = (SCALE*988,SCALE*373)

# pickup labels
P_LOCATION_221 = (SCALE*135,SCALE*200)
P_LOCATION_332 = (SCALE*660,SCALE*85)

# dropoff labels
D_LOCATION_311 = (SCALE*250,SCALE*320)
D_LOCATION_112 = (SCALE*425,SCALE*320)
D_LOCATION_113 = (SCALE*835,SCALE*320)
D_LOCATION_323 = (SCALE*1070,SCALE*200)

# risk labels
R_LOCATION_321 = (SCALE*250,SCALE*200)
R_LOCATION_222 = (SCALE*545,SCALE*200)

# agents
F_START = (SCALE*55, SCALE*285)
M_START = (SCALE*(990+120), SCALE*(120+55))

# Z=1 agent blit locations
LOC_111 = (SCALE*55, SCALE*285) # F <- LOC_MATRIX[0][0][0]
LOC_211 = (SCALE*175, SCALE*285)
LOC_311 = (SCALE*295, SCALE*285)
LOC_121 = (SCALE*55, SCALE*165)
LOC_221 = (SCALE*175, SCALE*165)
LOC_321 = (SCALE*295, SCALE*165)
LOC_131 = (SCALE*55, SCALE*45) # LOC_MATRIX[0][2][0]
LOC_231 = (SCALE*175, SCALE*45)
LOC_331 = (SCALE*295, SCALE*45)

# Z=2 agent blit locations
LOC_112 = (SCALE*465, SCALE*285)
LOC_212 = (SCALE*585, SCALE*285)
LOC_312 = (SCALE*705, SCALE*285)
LOC_122 = (SCALE*465, SCALE*165)
LOC_222 = (SCALE*585, SCALE*165)
LOC_322 = (SCALE*705, SCALE*165)
LOC_132 = (SCALE*465, SCALE*45)
LOC_232 = (SCALE*585, SCALE*45)
LOC_332 = (SCALE*705, SCALE*45)

# Z=3 agent blit locations
LOC_113 = (SCALE*875, SCALE*285)
LOC_213 = (SCALE*995, SCALE*285)
LOC_313 = (SCALE*1115, SCALE*285)
LOC_123 = (SCALE*875, SCALE*165)
LOC_223 = (SCALE*995, SCALE*165)
LOC_323 = (SCALE*1115, SCALE*165) # M <- LOC_MATRIX[2][1][2]
LOC_133 = (SCALE*875, SCALE*45)
LOC_233 = (SCALE*995, SCALE*45)
LOC_333 = (SCALE*1115, SCALE*45)

# put into 3d array
LOC_MATRIX = np.empty(shape=(3, 3, 3), dtype=object, order='C')

LOC_MATRIX[0,0,0] = LOC_111
LOC_MATRIX[1,0,0] = LOC_211
LOC_MATRIX[2,0,0] = LOC_311
LOC_MATRIX[0,1,0] = LOC_121
LOC_MATRIX[1,1,0] = LOC_221
LOC_MATRIX[2,1,0] = LOC_321
LOC_MATRIX[0,2,0] = LOC_131
LOC_MATRIX[1,2,0] = LOC_231
LOC_MATRIX[2,2,0] = LOC_331

LOC_MATRIX[0,0,1] = LOC_112
LOC_MATRIX[1,0,1] = LOC_212
LOC_MATRIX[2,0,1] = LOC_312
LOC_MATRIX[0,1,1] = LOC_122
LOC_MATRIX[1,1,1] = LOC_222
LOC_MATRIX[2,1,1] = LOC_322
LOC_MATRIX[0,2,1] = LOC_132
LOC_MATRIX[1,2,1] = LOC_232
LOC_MATRIX[2,2,1] = LOC_332

LOC_MATRIX[0,0,2] = LOC_113
LOC_MATRIX[1,0,2] = LOC_213
LOC_MATRIX[2,0,2] = LOC_313
LOC_MATRIX[0,1,2] = LOC_123
LOC_MATRIX[1,1,2] = LOC_223
LOC_MATRIX[2,1,2] = LOC_323
LOC_MATRIX[0,2,2] = LOC_133
LOC_MATRIX[1,2,2] = LOC_233
LOC_MATRIX[2,2,2] = LOC_333

if LOC_MATRIX[1][2][0] == LOC_231:
    print("Correctly built")
else:
    print("Incorrectly built")



# TODO block stack locations


# move offset values
# E, W -> +x, -x
# N, S -> -y, +y
# U, D -> +x, -x
MOVE_OFFSET_NESW = SCALE*120
MOVE_OFFSET_UD = SCALE*410


################ END GLOBALS ################

###########
# TODO implement function to draw stacked blocks - Alex
# block_arr_one = [] #floor 1 
# block_arr_two = [] #floor 2

# block_one_y = (220 * SCALE)
# block_two_y = 105 * SCALE)

# offset = 11 * SCALE

# for i in range(10):
#     block1 = (SCALE * 220,block_one_y)
#     block2 = (SCALE * 750,block_two_y)
#     block_arr_one.append(block1)
#     block_arr_two.append(block2)
#     block_one_y = block_one_y - offset
#     block_two_y = block_two_y - offset

    # for itr in range(10):
        #     game_block1 = block_arr_one[itr]
        #     game_block2 = block_arr_two[itr]

        #     WIN.blit(block,(game_block1[0],game_block1[1]))
        #     WIN.blit(block,(game_block2[0],game_block2[1]))

################
# p_list = ["right", "right","down","up"]
# p2_list = ["right", "right","down","up"]

class Agent:
    def __init__(self, _id, _loc, _asset, _actionList):
        self.id = _id # F or M
        # TODO represent cell locations in 3D array to avoid compounding errors
        self.loc = _loc
        self.asset = _asset
        self.actionList = _actionList
        self.index = 0
    
    def set_asset(self, _asset):
        self.asset = _asset

    def move_east(self):
        # update loc
        # self.loc = (self.loc[0]+MOVE_OFFSET_NESW, self.loc[1])
        # check bounds
        # if self.loc[0] < 2:
        self.loc = (self.loc[0]+1, self.loc[1], self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_west(self):
        # update loc
        # self.loc = (self.loc[0]-MOVE_OFFSET_NESW, self.loc[1])
        # check bounds
        # if self.loc[0] > 0:
        self.loc = (self.loc[0]-1, self.loc[1], self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])
  

    def move_north(self):
        # update loc
        # self.loc = (self.loc[0], self.loc[1]-MOVE_OFFSET_NESW)
        # check bounds
        # if self.loc[1] < 2:
        self.loc = (self.loc[0], self.loc[1]+1, self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_south(self):
        # update loc
        # check bounds
        # if self.loc[1] > 0:
        self.loc = (self.loc[0], self.loc[1]-1, self.loc[2])
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def move_up(self):
        # update loc
        # check bounds
        
        self.loc = (self.loc[0], self.loc[1], self.loc[2]+1)
        if self.loc[2] > 2:
            print(f"agent {self.id} z coordinate = {self.loc[2]}")
            print(f"problematic move on line {self.index+1}")
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])
    
    def move_down(self):
        # update loc
        # check bounds
        # if self.loc[2] > 0:
        self.loc = (self.loc[0], self.loc[1], self.loc[2]-1)
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def pickup(self):
        if self.id == 'F':
            self.asset = f_carrying
        elif self.id == 'M':
            self.asset = m_carrying
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

    def dropoff(self):
        if self.id == 'F':
            self.asset = f_not_carrying
        elif self.id == 'M':
            self.asset = m_not_carrying
        self.index += 1
        WIN.blit(self.asset, LOC_MATRIX[self.loc[0]][self.loc[1]][self.loc[2]])

# import action lists
agentFActions = []
agentMActions = []
with open('f_actions', 'r', encoding="utf-8") as f:
    for line in f:
        x = line[:-1]
        agentFActions.append(x)
with open('m_actions', 'r', encoding="utf-8") as f:
    for line in f:
        x = line[:-1]
        agentMActions.append(x)

# TODO consider experiment 4 with modified RW state space
def draw_window(c, agent):
    WIN.fill(LIGHT_YELLOW)

    WIN.blit(grid, Z1_LOCATION)
    WIN.blit(grid, Z2_LOCATION)
    WIN.blit(grid, Z3_LOCATION)

    WIN.blit(Z1_LABEL, Z1_LABEL_LOCATION)
    WIN.blit(Z2_LABEL, Z2_LABEL_LOCATION)
    WIN.blit(Z3_LABEL, Z3_LABEL_LOCATION)
    
    WIN.blit(p, P_LOCATION_221)
    WIN.blit(p, P_LOCATION_332)

    WIN.blit(d, D_LOCATION_311)
    WIN.blit(d, D_LOCATION_112)
    WIN.blit(d, D_LOCATION_113)
    WIN.blit(d, D_LOCATION_323)

    WIN.blit(r, R_LOCATION_321)
    WIN.blit(r, R_LOCATION_222)
    
    if c.numActions == 0:
        WIN.blit(f_not_carrying, LOC_MATRIX[0][0][0])
        WIN.blit(m_not_carrying, LOC_MATRIX[2][1][2])
    else:
        draw_action(c, agent)
        
        # pass
    
    # testing movement functions
    
    # WIN.blit(f_not_carrying,(F_START[0], F_START[1]))
    # agent.move_west()
    # WIN.blit(m_not_carrying,(M_START[0], M_START[1]))

    pygame.display.update()

def draw_action(c, agent):
    # conditionally blit dynamic assets (agents, blocks)
    # TODO draw blocks
    i = agent.index
    action = agent.actionList[i]
    # if c.numTerminal == 8:
    #     print(f"Agent {agent.id}'s index is {agent.index} and performing {action}")
    if action == 'E':
        agent.move_east()
    elif action == 'W':
        agent.move_west()
    elif action == 'N':
        agent.move_north()
    elif action == 'S':
        agent.move_south()
    elif action == 'U':
        agent.move_up()
    elif action == 'D':
        agent.move_down()
    elif action == 'Pickup':
        agent.pickup()
    elif action == 'Dropoff':
        agent.dropoff()
        c.numDropoff += 1

class Conditions:
    def __init__(self):
        self.numDropoff = 0
        self.numActions = 0
        self.numTerminal = 0

def main():
    
    c = Conditions()

    F = Agent('F', [0,0,0], f_not_carrying, agentFActions)
    M = Agent('M', [2,1,2], m_not_carrying, agentMActions)

    q = Queue(maxsize=2)
    q.put(M)
    q.put(F)

    run = True
    clock = pygame.time.Clock()

    # number of total iterations
    n = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        curAgent = q.get()

        draw_window(c, curAgent)
        c.numActions += 1
        # draw_window(0, F)

        q.put(curAgent)
        
        # redraw inactive agent
        if c.numActions != 0:
            if curAgent.id == 'F':
                WIN.blit(M.asset, LOC_MATRIX[M.loc[0]][M.loc[1]][M.loc[2]])
            else:
                WIN.blit(F.asset, LOC_MATRIX[F.loc[0]][F.loc[1]][F.loc[2]])
            pygame.display.update()

        # check terminal state & reset if true
        if c.numDropoff == 20:
            c.numTerminal += 1
            print(f"terminal state {c.numTerminal} reached")
            c.numActions = 0
            c.numDropoff = 0
            F.loc = [0,0,0]
            M.loc = [2,1,2]
            curAgent = q.get()
            curAgent = q.get()
            q.put(M)
            q.put(F)

        n += 1
        if n >= 10000:
            break # leave window open, TODO indicate end of experiment
        
        

    pygame.quit()

if __name__ == "__main__":
    main()
