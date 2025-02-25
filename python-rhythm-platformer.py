import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (30, 30, 30)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Platformer")
clock = pygame.time.Clock()

# Load assets
def load_image(name):
    return pygame.image.load(os.path.join('images', name)).convert_alpha()

# Player class
class Player:
    def __init__(self, ground_level):
        self.x = 100
        self.y = 300
        self.velocity = 0
        self.gravity = 0.8
        self.jump_force = -15
        self.size = 30
        self.is_jumping = False
        self.frame_count = 0
        self.current_frame = 0
        self.animation_speed = 0.2
        self.sprite_width = 32
        self.sprite_height = 32
        self.total_frames = 4
        self.spritesheet = pygame.image.load(os.path.join('images', 'player.png')).convert_alpha()
        self.ground = ground_level

    def get_sprite(self):
        self.frame_count += self.animation_speed
        self.current_frame = int(self.frame_count) % self.total_frames
        return pygame.Rect(
            self.current_frame * self.sprite_width, 
            0, 
            self.sprite_width, 
            self.sprite_height
        )

    def jump(self):
        if not self.is_jumping:
            self.velocity = self.jump_force
            self.is_jumping = True

    def update(self, obstacles):
        # Apply gravity
        self.velocity += self.gravity
        self.y += self.velocity

        # Check ground collision
        if self.y > self.ground - self.size/2:
            self.y = self.ground - self.size/2
            self.velocity = 0
            self.is_jumping = False

        # Check platform collisions
        for obstacle in obstacles:
            bounds = obstacle.get_bounds()
            player_bounds = self.get_bounds()
            
            if self.velocity > 0:  # Only check when falling
                was_above_platform = player_bounds['bottom'] - self.velocity <= bounds['top']
                is_overlapping_x = player_bounds['right'] > bounds['left'] and player_bounds['left'] < bounds['right']
                
                if was_above_platform and is_overlapping_x and player_bounds['bottom'] >= bounds['top']:
                    self.y = bounds['top'] - self.size/2
                    self.velocity = 0
                    self.is_jumping = False

    def draw(self, surface):
        sprite_rect = self.get_sprite()
        # Create a subsurface from the spritesheet
        sprite = self.spritesheet.subsurface(sprite_rect)
        # Scale the sprite to the desired size
        scaled_sprite = pygame.transform.scale(sprite, (self.size, self.size))
        # Draw the sprite
        surface.blit(scaled_sprite, (self.x - self.size/2, self.y - self.size/2))

    def get_bounds(self):
        return {
            'left': self.x - self.size/2,
            'right': self.x + self.size/2,
            'top': self.y - self.size/2,
            'bottom': self.y + self.size/2
        }

# Obstacle class
class Obstacle:
    def __init__(self, x, ground_level, obstacles_passed, player):
        self.ground = ground_level
        
        # Calculate difficulty based on obstacles passed
        difficulty_multiplier = 1 + (obstacles_passed / 50)
        platform_roll = random.random()
        
        # Determine platform type
        is_narrow = platform_roll < 0.3 * difficulty_multiplier
        is_extra_wide = platform_roll > 0.8
        
        # Set width based on platform type
        if is_narrow:
            self.width = random.randint(20, 35)
            self.sprite = platform_sprites['narrow']
        elif is_extra_wide:
            self.width = random.randint(120, 200)
            self.sprite = platform_sprites['wide']
        else:
            self.width = random.randint(40, 80)
            self.sprite = platform_sprites['normal']
            
        # Calculate maximum jump height based on player physics
        max_jump_height = (player.jump_force * player.jump_force) / (2 * player.gravity)
        
        # Set height based on platform type
        if is_narrow:
            self.height = random.randint(40, int(max_jump_height * 0.6))
        elif is_extra_wide:
            self.height = random.randint(50, int(max_jump_height * 0.85))
        else:
            self.height = random.randint(45, int(max_jump_height * 0.75))
            
        self.x = x
        self.y = ground_level - self.height
        
        # Calculate speed based on obstacles passed
        max_speed_increase = 8
        speed_increase = min(obstacles_passed / 25, max_speed_increase)
        self.speed = 7 + speed_increase
        self.passed = False

    def update(self, player, obstacles_passed):
        self.x -= self.speed
        
        # Check if player has passed this obstacle
        if not self.passed and self.x < player.x:
            self.passed = True
            return True  # Return True if obstacle was just passed
        return False

    def draw(self, surface):
        # Scale the sprite to the obstacle dimensions
        scaled_sprite = pygame.transform.scale(self.sprite, (int(self.width), int(self.height)))
        surface.blit(scaled_sprite, (int(self.x), int(self.y)))

    def get_bounds(self):
        return {
            'left': self.x,
            'right': self.x + self.width,
            'top': self.y,
            'bottom': self.y + self.height
        }

# Function to check collision between two bounding boxes
def check_collision(a, b):
    return not (a['right'] < b['left'] or a['left'] > b['right'] or 
                a['bottom'] < b['top'] or a['top'] > b['bottom'])

# Function to initialize the game
def init_game():
    global player, obstacles, obstacles_passed, game_over, game_won
    
    ground_level = SCREEN_HEIGHT - 50
    player = Player(ground_level)
    obstacles = []
    obstacles_passed = 0
    game_over = False
    game_won = False
    
    # Play background music
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    
    # Initialize with a few obstacles
    for i in range(3):
        obstacles.append(Obstacle(SCREEN_WIDTH + i * SCREEN_WIDTH/2, ground_level, obstacles_passed, player))

# Load assets
try:
    # Load platform sprites
    platform_sprites = {
        'narrow': load_image('narrow.png'),
        'normal': load_image('normal.png'),
        'wide': load_image('wide.png')
    }
    
    # Load background
    background_img = load_image('background.png')
    
    # Load and set up music
    pygame.mixer.music.load(os.path.join('audio.mp3'))
    pygame.mixer.music.set_volume(0.5)
    
except pygame.error as e:
    print(f"Couldn't load game assets: {e}")
    pygame.quit()
    sys.exit()

# Initialize game variables
init_game()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over and not game_won:
                    player.jump()
                else:
                    init_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle touch/click for mobile
            if not game_over and not game_won:
                player.jump()
            else:
                init_game()
    
    # Update game state if not game over or won
    if not game_over and not game_won:
        # Draw background
        screen.fill(DARK_GRAY)
        screen.blit(background_img, (0, 0))
        
        # Draw ground
        pygame.draw.rect(screen, GRAY, (0, player.ground, SCREEN_WIDTH, SCREEN_HEIGHT - player.ground))
        
        # Update player
        player.update(obstacles)
        
        # Update obstacles
        for i in range(len(obstacles) - 1, -1, -1):
            if obstacles[i].update(player, obstacles_passed):
                obstacles_passed += 1
                if obstacles_passed >= 100:
                    game_won = True
                    pygame.mixer.music.stop()
            
            # Check collision
            player_bounds = player.get_bounds()
            obstacle_bounds = obstacles[i].get_bounds()
            
            is_above_obstacle = player_bounds['bottom'] - player.velocity <= obstacle_bounds['top']
            if not is_above_obstacle and check_collision(player_bounds, obstacle_bounds):
                game_over = True
                pygame.mixer.music.stop()
            
            # Remove obstacles that are off-screen
            if obstacles[i].x + obstacles[i].width < 0:
                obstacles.pop(i)
        
        # Add new obstacles if needed
        if len(obstacles) < 3:
            last_obstacle = obstacles[-1]
            if SCREEN_WIDTH - last_obstacle.x > SCREEN_WIDTH/2:
                obstacles.append(Obstacle(SCREEN_WIDTH, player.ground, obstacles_passed, player))
        
        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw score
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Obstacles: {obstacles_passed}/100", True, BLACK)
        screen.blit(score_text, (20, 20))
    
    # Draw game over screen
    elif game_over:
        screen.fill(DARK_GRAY)
        font_large = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 24)
        
        game_over_text = font_large.render("Game Over!", True, WHITE)
        score_text = font_small.render(f"Obstacles cleared: {obstacles_passed}", True, WHITE)
        restart_text = font_small.render("Press SPACE to restart", True, WHITE)
        
        screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, SCREEN_HEIGHT/2))
        screen.blit(restart_text, (SCREEN_WIDTH/2 - restart_text.get_width()/2, SCREEN_HEIGHT/2 + 50))
    
    # Draw win screen
    elif game_won:
        screen.fill(DARK_GRAY)
        font_large = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 24)
        
        win_text = font_large.render("YOU WON!", True, WHITE)
        restart_text = font_small.render("Press SPACE to play again", True, WHITE)
        
        screen.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/2 - 25))
        screen.blit(restart_text, (SCREEN_WIDTH/2 - restart_text.get_width()/2, SCREEN_HEIGHT/2 + 50))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit game
pygame.quit()
sys.exit()
