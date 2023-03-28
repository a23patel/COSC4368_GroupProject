import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reinforcement Learning Visualization")
WHITE = (255, 255, 255)
FPS = 60

FEMALE_AGENT = pygame.image.load(os.path.join('assets', 'female_agent.png'))
FEMALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'female_agent_simple.png'))
MALE_AGENT = pygame.image.load(os.path.join('assets', 'male_agent.png'))
MALE_AGENT_SIMPLE = pygame.image.load(os.path.join('assets', 'male_agent_simple.png'))
Z_LEVEL = pygame.image.load(os.path.join('assets', 'grid.png'))
BLOCK = pygame.image.load(os.path.join('assets', 'block.png'))

def draw_window():
    WIN.fill(WHITE)
    WIN.blit(Z_LEVEL, (10,10))
    WIN.blit(Z_LEVEL, (322,10))
    WIN.blit(Z_LEVEL, (634,10))
    WIN.blit(FEMALE_AGENT, (50,125))
    WIN.blit(MALE_AGENT, (250,125))
    WIN.blit(BLOCK, (530,125))
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