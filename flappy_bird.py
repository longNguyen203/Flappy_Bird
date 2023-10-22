import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((432, 768)) # set size screen
clock = pygame.time.Clock()
gravity = 0.2
bird_movement = 0
game_active = True

background = pygame.image.load("assests/background-night.png").convert()
background = pygame.transform.scale2x(background)

floor = pygame.image.load("assests/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird = pygame.image.load("assests/yellowbird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 384))

pipe_surface = pygame.image.load("assests/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos+432, 650))
    
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-650))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -9
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
    
    screen.blit(background, (0, 0))
    
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
    
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
        draw_floor()
        
    pygame.display.update()       
    clock.tick(120)      