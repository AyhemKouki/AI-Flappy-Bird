import pygame , sys 

pygame.init()

SCREEN_WIDTH , SCREEN_HEIGHT = 576 , 800
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

BIRD_IMAGES = [pygame.image.load(f"imgs/bird{i+1}.png").convert_alpha() for i in range(3)]
PIPE_IMG =  pygame.image.load("imgs/pipe.png").convert_alpha()
BG_IMG = pygame.transform.scale2x(pygame.image.load("imgs/bg.png").convert_alpha())
BASE_IMG =  pygame.image.load("imgs/base.png").convert_alpha()

class Base:
    def __init__(self , x):
        self.base_img = BASE_IMG
        self.rect = BASE_IMG.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def move_base(self):
        self.rect.x -= 1

        if self.rect.right <= 0:
            self.rect.x = self.rect.width * 2

    def draw(self):
        screen.blit(self.base_img,self.rect)
    
    def update(self):
        self.move_base()
        self.draw()

# 336 is the length of a base image
base_list = [Base(0) , Base(336),Base(672)]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(BG_IMG,(0,-100))
    for index , base in enumerate(base_list):
        base.update()

    clock.tick(FPS)

    pygame.display.flip()