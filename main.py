import pygame , sys , random , neat , os

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

font = pygame.font.Font(pygame.font.get_default_font(), 30)

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

class Pipe():
    def __init__(self , x , y):
        self.pipe_img = PIPE_IMG
        self.rotated_pipe_img = pygame.transform.rotate(PIPE_IMG,180)
        self.rect = self.pipe_img.get_rect()
        self.rotated_rect = self.rotated_pipe_img.get_rect()
        self.gap = 140
        self.rect.x = x
        self.rotated_rect.x = x
        self.rect.y = y
        self.rotated_rect.bottom = y - self.gap
        self.passed = False
        
    def move_pipe(self):
        self.rect.x -= 1
        self.rotated_rect.x -= 1

    def draw_pipe(self):
        screen.blit(self.pipe_img,self.rect)
        screen.blit(self.rotated_pipe_img,self.rotated_rect)

    def update_pipe(self):
        self.draw_pipe()
        self.move_pipe()

def update_score():
    global score
    for pipe in pipe_list:
        if pipe.rect.right < bird.rect.left and not pipe.passed:
            score += 1
            pipe.passed = True 

def display_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

# 336 is the length of a base image
base_list = [Base(0) , Base(336),Base(672)]
bird = Bird()
pipe_list = []
score = 0

def check_collision():
    global score
    for pipe in pipe_list:
        if bird.rect.colliderect(pipe.rect) or bird.rect.colliderect(pipe.rotated_rect):
            print("collision with pipe")
            score = 0

    if bird.rect.bottom >= SCREEN_HEIGHT - 136:  # Collision with the base
        print("collision with base")
        score = 0

def fitness():
    timer = 180
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(BG_IMG,(0,-100))

        #PIPE SPAWN EVERY 3s
        if timer == 180 :
            y = random.randint(240,588)
            pipe_list.append(Pipe(SCREEN_WIDTH,y))
            timer =  0
        timer += 1
        for pipe in pipe_list[:]:  # we use a copy of the list to avoid modification issues
            pipe.update_pipe()
            if pipe.rect.x < -60:
                pipe_list.remove(pipe)

        # Update and display the score
        update_score()
        display_score()

        for base in base_list:
            base.update()
        bird.update_bird()

        check_collision()

        clock.tick(FPS)

        pygame.display.flip()
fitness()

def run_neat(config_file):
    config = neat.config.Config(
                        neat.DefaultGenome, 
                        neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, 
                        neat.DefaultStagnation,
                        config_file
            )
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # 50 is the max generations will be created
    population.run(fitness,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run_neat(config_path)