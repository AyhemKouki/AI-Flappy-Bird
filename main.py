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
        
    def Gravity(self):
        #GRAVITY
        if self.rect.y < SCREEN_HEIGHT - 136:  # If bird is above the base
            self.y_vel += self.gravity
            if self.y_vel >= self.max_fall_speed:
                self.y_vel = self.max_fall_speed

        #you can jump again when the bird starts falling
        if self.y_vel >0:
            self.flap = False

        self.rect.y += self.y_vel * 0.9
        
        # bird stay at ground level when it hits the ground
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
        self.Gravity()
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

# 336 is the length of a base image
base_list = [Base(0) , Base(336),Base(672)]
pipe_list = []

def fitness(genomes , config):
    global score 
    score = 0
    timer = 180
    birds = []
    nets = []
    genomes_list = []

    # Clear the pipe list for the new generation
    pipe_list = []

    for _,genome in genomes:
        birds.append(Bird())
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        genomes_list.append(genome)
        genome.fitness = 0

    while len(birds)>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(BG_IMG,(0,-100))

        # Increment fitness for surviving longer
        for index in range(len(birds)):
            genomes_list[index].fitness += 0.1 

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

        #move base
        for base in base_list:
            base.update()
            
        birds_to_remove = []
        for index , bird in enumerate(birds[:]):
            # Find the closest pipe in front of the bird
            closest_pipe = None
            for pipe in pipe_list:
                if pipe.rect.x + pipe.rect.width > bird.rect.x:
                    closest_pipe = pipe
                    break

            if closest_pipe:
                # Input features for the neural network
                bird_y = bird.rect.y
                bird_velocity = bird.y_vel
                bottom_gap_y = closest_pipe.rect.y
                top_gap_y = closest_pipe.rotated_rect.bottom
                distance_to_pipe = closest_pipe.rect.x - bird.rect.x

                # the inputs
                inputs = [
                    bird_y ,
                    bird_velocity,
                    distance_to_pipe,
                    bird_y - top_gap_y,
                    bottom_gap_y - bird_y,
                ]

                output = nets[index].activate(inputs)
                #JUMP
                if output[0] > 0.5:  # Threshold for jumping
                    bird.y_vel = -8
                    bird.flap = True

            bird.update_bird()

            # CHECK COLLISION
            for pipe in pipe_list:
                if bird.rect.colliderect(pipe.rect) or bird.rect.colliderect(pipe.rotated_rect) or bird.rect.bottom >= SCREEN_HEIGHT - 136 or bird.rect.y < 0:
                    genomes_list[index].fitness -= 1 # Penalize
                    birds_to_remove.append(index)
            
                # Update and display the score
                if not pipe.passed and pipe.rect.x < bird.rect.x: 
                    pipe.passed = True  # Mark the pipe as passed
                    score += 1  # Increment the score
                    genomes_list[index].fitness += 5 

        # Remove collided birds 
        for i in sorted(birds_to_remove, reverse=True):
            birds.pop(i)
            nets.pop(i)
            genomes_list.pop(i)

        #display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        clock.tick(FPS)
        pygame.display.flip()

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