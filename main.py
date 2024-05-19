import pygame
import random

pygame.mixer.init()

# Load the audio file
pygame.mixer.music.load('audio.mp3')

# Play the audio
pygame.mixer.music.play(-1)  # Play in an infinite loop

screen_size = [360, 600]
screen = pygame.display.set_mode(screen_size)
pygame.font.init()

background = pygame.image.load('background.png')
user = pygame.image.load('user.png')
chicken = pygame.image.load('chicken.png')
restart_img = pygame.image.load('restart.webp')  # Load restart button image

def display_score(score):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    score_text = 'Score: ' + str(score)
    text_img = font.render(score_text, True, (0, 255, 0))
    screen.blit(text_img, [20, 10])

def random_offset():
    return -1*random.randint(100, 1500)

chicken_y = [random_offset(), random_offset(), random_offset()]
user_x = 150
score = 0

def crashed(idx):
    global score
    global keep_alive
    score = score - 50
    chicken_y[idx] = random_offset()
    if score < -500:
        keep_alive = False

def update_chicken_pos(idx):
    global score
    if chicken_y[idx] > 600:
        chicken_y[idx] = random_offset()
        score = score + 5
        print('score', score)
    else:
        chicken_y[idx] = chicken_y[idx] + 5

def display_restart_button():
    # Scale the restart image to a smaller size
    scaled_restart_img = pygame.transform.scale(restart_img, (200, 100))  # Adjust the size as needed
    
    # Fill the screen with the background color
    screen.blit(background, (0, 0))
    
    # Redraw the game elements (user, chickens, score)
    screen.blit(user, [user_x, 520])
    screen.blit(chicken, [0, chicken_y[0]])
    screen.blit(chicken, [150, chicken_y[1]]) 
    screen.blit(chicken, [280, chicken_y[2]])
    display_score(score)
    
    # Draw the restart button
    screen.blit(scaled_restart_img, (80, 400))
    
    pygame.display.update()

keep_alive = True
game_over = False
clock = pygame.time.Clock()

while keep_alive:
    pygame.event.get()
    keys = pygame.key.get_pressed()

    if game_over:
        # Game over state
        display_restart_button()
        
        # Check for restart
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                scaled_restart_img = pygame.transform.scale(restart_img, (200, 100))  # Scale the restart image
                if 80 < mouse_pos[0] < 80 + scaled_restart_img.get_width() and 400 < mouse_pos[1] < 400 + scaled_restart_img.get_height():
                    # Restart the game
                    game_over = False
                    score = 0
                    chicken_y = [random_offset(), random_offset(), random_offset()]
                    pygame.mixer.music.play(-1)  # Restart the music
    else:
        # Game is running
        if keys[pygame.K_RIGHT] and user_x < 280:
            user_x = user_x + 10
        elif keys[pygame.K_LEFT] and user_x > 0:
            user_x = user_x - 10

        update_chicken_pos(0)
        update_chicken_pos(1)
        update_chicken_pos(2)

        screen.blit(background, [0, 0])
        screen.blit(user, [user_x, 520])
        screen.blit(chicken, [0, chicken_y[0]])
        screen.blit(chicken, [150, chicken_y[1]])
        screen.blit(chicken, [280, chicken_y[2]])

        if chicken_y[0] > 500 and user_x < 70:
            crashed(0)
            game_over = True
            pygame.mixer.music.stop()  # Stop the music on game over

        if chicken_y[1] > 500 and user_x > 80 and user_x < 200:
            crashed(1)
            game_over = True
            pygame.mixer.music.stop()  # Stop the music on game over

        if chicken_y[2] > 500 and user_x > 220:
            crashed(2)
            game_over = True
            pygame.mixer.music.stop()  # Stop the music on game over

        display_score(score)

    pygame.display.update()
    clock.tick(60)