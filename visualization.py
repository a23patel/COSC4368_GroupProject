import pygame
import os

# import action lists
# agentFActions = []
# agentMActions = []
# with open('f_actions', 'r', encoding="utf-8") as f:
#     for line in f:
#         x = line[:-1]
#         agentFActions.append(x)
# with open('m_actions', 'r', encoding="utf-8") as f:
#     for line in f:
#         x = line[:-1]
#         agentMActions.append(x)

# TODO list
# 1. Agree on LARGE window dimensions - DONE
# 2. Resize assets such that busiest cell fits all assets - DONE
# 3. Define all locations - dont need this i think
# 4. Write a function to show intial state
    # 1. white window - done
    # 2. blit zlevels side by side & perhaps label them (z=1, z=2, z=3) - Abraar can add this
    # 3. blit every asset to the appropriate postion - need boxes
# 5. Incorporate action lists into the logic
# 6. Check terminal state reached, and reset (dropoffCounter == 20)
# 7. Display someting to indicate end of experiment

# maybe a more elegant solution to movement logic is:
# if aciton != U or D then
    # add or substract appropriate length (number of pixels) to x or y
# else if action == U or D then
    # if statements to perform large change in x coordinates (y never changes)

pygame.init()


WIN = pygame.display.set_mode((1200, 500))
pygame.display.set_caption("Reinforcement Learning Visualization")
WHITE = (255, 255, 255)
FPS = 60
default_size = (35,45)
default_block = (25,25)
default_grid = (360,360)

#clock 
clock = pygame.time.Clock()
FPS = 5

FEMALE_AGENT = pygame.image.load(os.path.join('assets', 'female_agent.png'))
FEMALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'female_agent_simple.png'))
MALE_AGENT = pygame.image.load(os.path.join('assets', 'male_agent.png'))
MALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'male_agent_simple.png'))
Z_LEVEL = pygame.image.load(os.path.join('assets', 'grid.png'))
BLOCK = pygame.image.load(os.path.join('assets', 'block.png'))
P = pygame.image.load(os.path.join('assets','p_pix.png'))
D = pygame.image.load(os.path.join('assets','d_pix.png'))
R = pygame.image.load(os.path.join('assets','r_pix.png'))

image_f = pygame.transform.scale(FEMALE_AGENT_SIMPLE,default_size)
busy_f = pygame.transform.scale(FEMALE_AGENT,default_size)

image_m = pygame.transform.scale(MALE_AGENT_SIMPLE,default_size)
busy_m = pygame.transform.scale(MALE_AGENT,default_size)

grid_1 = pygame.transform.scale(Z_LEVEL,default_grid)

resized_block = pygame.transform.scale(BLOCK,default_size)

resized_pick = pygame.transform.scale(P,default_size)
resized_d = pygame.transform.scale(D,default_size)
resized_r = pygame.transform.scale(R,default_size)

class block(pygame.sprite.Sprite):
    def __init__(self, x,y) -> None:
        super().__init__()
        self.image = resized_block
        self.x = x
        self.y = y



block_array = []

starting_x_f = 985
starting_y_f = 45


starting_m_x = 45
starting_m_y = 285

p_list = ["right", "right","down","up"]
p2_list = ["right", "right","down","up"]

#main loop
#for i,j in zip(p_list,p2_list):
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(FPS)
    
    WIN.fill(WHITE)
    WIN.blit(grid_1, (10,10))
    WIN.blit(grid_1, (420,10))
    WIN.blit(grid_1, (830,10))

    WIN.blit(resized_d,(285,285))
    WIN.blit(resized_d,(455,285))
    WIN.blit(resized_d,(875,285))
    WIN.blit(resized_d,(980,165))

    WIN.blit(resized_r,(285,165))
    WIN.blit(resized_r,(575,165))

    WIN.blit(resized_pick,(165,165))
    WIN.blit(resized_pick,(700,45))

    WIN.blit(image_f,(starting_x_f,starting_y_f))
    WIN.blit(image_m,(starting_m_x,starting_m_y))

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


    pygame.display.update()
