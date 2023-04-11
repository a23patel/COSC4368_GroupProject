import pygame
import os
from pygame.font import Font

################## GLOBALS ##################

# controls overall size
SCALE = 1.05

# window
WIDTH, HEIGHT = (SCALE*1200), (SCALE*400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning Visualization")

# colors
WHITE = (255, 255, 255)
LIGHT_YELLOW = (255, 255, 204)
PURPLE = (128, 0, 128)

# speed of execution
FPS = 60

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
F_START = (SCALE*990, SCALE*55)
M_START = (SCALE*55, SCALE*285)

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
p_list = ["right", "right","down","up"]
p2_list = ["right", "right","down","up"]

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

def draw_window(_n):
    WIN.fill(WHITE)

    WIN.blit(grid, (Z1_LOCATION[0],Z1_LOCATION[1]))
    WIN.blit(grid, (Z2_LOCATION[0],Z2_LOCATION[1]))
    WIN.blit(grid, (Z3_LOCATION[0],Z3_LOCATION[1]))

    WIN.blit(Z1_LABEL, (Z1_LABEL_LOCATION[0], Z1_LABEL_LOCATION[1]))
    WIN.blit(Z2_LABEL, (Z2_LABEL_LOCATION[0], Z2_LABEL_LOCATION[1]))
    WIN.blit(Z3_LABEL, (Z3_LABEL_LOCATION[0], Z3_LABEL_LOCATION[1]))
    
    WIN.blit(p,(P_LOCATION_221[0],P_LOCATION_221[1]))
    WIN.blit(p,(P_LOCATION_332[0],P_LOCATION_332[1]))

    WIN.blit(d,(D_LOCATION_311[0],D_LOCATION_311[1]))
    WIN.blit(d,(D_LOCATION_112[0],D_LOCATION_112[1]))
    WIN.blit(d,(D_LOCATION_113[0],D_LOCATION_113[1]))
    WIN.blit(d,(D_LOCATION_323[0],D_LOCATION_323[1]))

    WIN.blit(r,(R_LOCATION_321[0],R_LOCATION_321[1]))
    WIN.blit(r,(R_LOCATION_222[0],R_LOCATION_222[1]))
    
    # draw_action(_n, curLoc, action)

    # test agent loc
    WIN.blit(f_not_carrying,(F_START[0], F_START[1]))
    WIN.blit(m_not_carrying,(M_START[0]+MOVE_OFFSET_UD, M_START[1]))

    pygame.display.update()

def draw_action(_n, curLoc, action):
    # conditionally blit dynamic assets (agents, blocks)
    if _n == 0:
        WIN.blit(f_not_carrying,(F_START[0], F_START[1]))
        WIN.blit(m_not_carrying,(M_START[0], M_START[1]))
        # TODO draw blocks
    else:
        
        pass

#main loop
#for i,j in zip(p_list,p2_list):

def main():
    run = True
    clock = pygame.time.Clock()
    # number of iterations
    n = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(n)
        n += 1

    pygame.quit()

if __name__ == "__main__":
    main()
        
       
        
        
        
        
        
        # if i == "right":
        #     x += 120
        # elif i == "left":
        #     x -= 120
        # elif i == "down":
        #     y += 120
        # else:
        #     y -= 120

        # if j == "right":
        #     m_x += 120
        # elif j == "left":
        #     m_x -= 120
        # elif j == "down":
        #     m_y += 120
        # elif j == "up":
        #     m_y -= 120 


    

