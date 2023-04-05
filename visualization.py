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
# 1. Agree on LARGE window dimensions ?DONE
# 2. Resize assets such that busiest cell fits all assets
# 3. Define all locations
# 4. Write a function to show intial state
    # 1. white window
    # 2. blit zlevels side by side & perhaps label them (z=1, z=2, z=3)
    # 3. blit every asset to the appropriate postion
# 5. Incorporate action lists into the logic
# 6. Check terminal state reached, and reset (dropoffCounter == 20)
# 7. Display someting to indicate end of experiment

WIDTH, HEIGHT = 900, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning Visualization")
WHITE = (255, 255, 255)
FPS = 60
default_size = (50,50)
# maybe a more elegant solution to movement logic is:
# if aciton != U or D then
    # add or substract appropriate length (number of pixels) to x or y
# else if action == U or D then
    # if statements to perform large change in x coordinates (y never changes)

# z=0 locations
LOC_000 = () 
LOC_100 = () 
LOC_200 = () 
LOC_010 = () 
LOC_110 = () 
LOC_210 = () 
LOC_020 = () 
LOC_120 = () 
LOC_220 = () 

# z=1 locations
LOC_001 = () 
LOC_101 = () 
LOC_201 = () 
LOC_011 = () 
LOC_111 = () 
LOC_211 = () 
LOC_021 = () 
LOC_121 = () 
LOC_221 = ()

# z=2 locations
LOC_002 = () 
LOC_102 = () 
LOC_202 = () 
LOC_012 = () 
LOC_112 = () 
LOC_212 = () 
LOC_022 = () 
LOC_122 = () 
LOC_222 = () 

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

#can move resized simple female image by adding or subtracting 85 for x and y movements, z movement is changed by adding 310 to x

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(Z_LEVEL, (10,10))
    WIN.blit(Z_LEVEL, (322,10))
    WIN.blit(Z_LEVEL, (634,10))
    # WIN.blit(FEMALE_AGENT, (50,125))
    # WIN.blit(MALE_AGENT, (250,125))
    #WIN.blit(BLOCK, (15,300))
    #WIN.blit(BLOCK, (15,200))
    WIN.blit(image_f,(505,25))
    # WIN.blit(P,(100,10))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()