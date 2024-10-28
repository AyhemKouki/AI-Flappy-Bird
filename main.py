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

pygame.display.set_icon(BIRD_IMAGES[1])

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

class Bird:
    def __init__(self):
        self.bird_img = BIRD_IMAGES[0]
        self.rect = self.bird_img.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT//2
        self.max_fall_speed = 10
        self.gravity = 0.5
        self.y_vel = 0
        self.flap = False
        self.frame = 0
        
    def jump(self):
        #GRAVITY
        if self.rect.y < SCREEN_HEIGHT - 136:  # If bird is above the base
            self.y_vel += self.gravity
            if self.y_vel >= self.max_fall_speed:
                self.y_vel = self.max_fall_speed
        
        #JUMP
        press = pygame.key.get_pressed()
        if press[pygame.K_SPACE] and not self.flap and self.rect.top > 0:
            self.y_vel = -8
            self.flap = True

        #you can jump again when the bird starts falling
        if self.y_vel >0:
            self.flap = False

        self.rect.y += self.y_vel * 0.9
        
        if self.rect.y >= SCREEN_HEIGHT - 136:
            self.rect.y = SCREEN_HEIGHT - 136
            self.y_vel = 0

    def animation(self):
        if self.frame < FPS//6:
            self.bird_img = BIRD_IMAGES[0]
        elif FPS//6<= self.frame < FPS//3:
            self.bird_img = BIRD_IMAGES[1]
        else:
            self.bird_img = BIRD_IMAGES[2]

        if self.frame > (FPS//3)*2 :
            self.frame = 0
        self.frame += 1
        
    def draw_bird(self):
        angle = min(max(self.y_vel * -5, -25), 25)
        rotated_bird = pygame.transform.rotate(self.bird_img, angle) # Cap angle between -25 and 25 degrees
        rotated_rect = rotated_bird.get_rect(center=self.rect.center)
        screen.blit(rotated_bird, rotated_rect)

    def update_bird(self):
        self.animation()
        self.jump()
        self.draw_bird()

# 336 is the length of a base image
base_list = [Base(0) , Base(336),Base(672)]
bird = Bird()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(BG_IMG,(0,-100))
    for index , base in enumerate(base_list):
        base.update()
    bird.update_bird()

    clock.tick(FPS)

    pygame.display.flip()