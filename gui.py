import math

import pygame
import sys
from network import Network
from _thread import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 8
BOX_SIZE = SCREEN_WIDTH // GRID_SIZE
OUTLINE_WIDTH = 1

# Colors
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

color = [RED, GREEN, BLUE, YELLOW, CYAN]
user_color = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN"]

# Player info
player_no = 0
player_color = color[0]
player_color_string = user_color[0]

# Font
font = pygame.font.Font('freesansbold.ttf', 16)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, 900))
pygame.display.set_caption('Color the Boxes')
screen.fill(WHITE)

# Player scores
P1_score = 0
P2_score = 0
P3_score = 0
P4_score = 0
P5_score = 0

# Player scores
scores = [0, 0, 0, 0, 0]

# Initialize grid
grid = [[GRAY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
# Initialize grid that keeps track which squares are in use
useGrid = [["empty" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)
timer = False
seconds = 0
minutes = 0

# Function to get the grid position based on mouse click
def get_grid_pos(pos):
    x, y = pos
    grid_x = x // BOX_SIZE
    grid_y = y // BOX_SIZE
    return grid_x, grid_y

# Draw text
def draw_text(text, x):
    screen.fill(pygame.Color("white"), (x, 15, 100, 20))
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (x, 15))

def update_colors(n):
    global P1_score
    global P2_score
    global P3_score
    global P4_score
    global P5_score
    global timer
    global seconds
    global minutes

    while True:
        try:
            # Draw the grid
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if useGrid[y][x] == "empty":
                        pygame.draw.rect(screen, GRAY, (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE))
                    pygame.draw.rect(screen, BLACK, (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE),
                                     OUTLINE_WIDTH)

            # Update the screen
            pygame.display.flip()

            # Get updates from server
            reply = n.getmsg()
            temp = reply.split()

            if temp[0] == "draw":
                y = int(temp[1])
                x = int(temp[2])
                useGrid[y][x] = "used"
                color_index = user_color.index(temp[3])
                pygame.draw.rect(screen, color[color_index], [int(temp[5]), int(temp[4]), 10, 10])
                pygame.display.flip()
            elif temp[0] == "fill":
                y = int(temp[2])
                x = int(temp[3])
                if temp[1] == "pass":
                    color_index = user_color.index(temp[4])
                    scores[color_index] += 1
                    grid[y][x] = color[color_index]
                    pygame.draw.rect(screen, color[color_index], (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE))
                    # update player score
                    draw_text("Player 1: {}".format(scores[0]), 150)
                    draw_text("Player 2: {}".format(scores[1]), 250)
                    draw_text("Player 3: {}".format(scores[2]), 350)
                    draw_text("Player 4: {}".format(scores[3]), 450)
                    draw_text("Player 5: {}".format(scores[4]), 550)
                elif temp[1] == "fail":
                    useGrid[y][x] = "empty"
                    pygame.draw.rect(screen, GRAY, (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE))
            elif temp[0] == "reset":
                print("reset received")
                timer = False
                seconds = 0
                minutes = 0

                pygame.draw.rect(screen, WHITE, [420, 40, 200, 55])

                for i in range(0,5):
                    scores[i] = 0

                    draw_text("Player 1: {}".format(scores[0]), 150)
                    draw_text("Player 2: {}".format(scores[1]), 250)
                    draw_text("Player 3: {}".format(scores[2]), 350)
                    draw_text("Player 4: {}".format(scores[3]), 450)
                    draw_text("Player 5: {}".format(scores[4]), 550)

                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        useGrid[y][x] = 'empty'

            elif temp[0] == "start":
                print("start received")

                timer = True

            elif temp[0] == "finish":
                timer = False
                winner = max(scores)
                winner_index = scores.index(winner)
                print(winner)
                print(winner_index)
                txt = font.render("Player {} wins!".format(winner_index + 1), True, BLACK)
                pygame.draw.rect(screen, WHITE, [420, 40, 180, 55])
                screen.blit(txt, (420 + 25, 55))

        except:
            pass

# Main game loop
def main():
    n = Network()
    print(n.msg)
    player_no = int(n.msg[-1])
    player_color = color[player_no - 1]
    player_color_string = user_color[player_no - 1]
    seconds, minutes = 0, 0

    running = True
    draw_text("Player 1: {}".format(scores[0]), 150)
    draw_text("Player 2: {}".format(scores[1]), 250)
    draw_text("Player 3: {}".format(scores[2]), 350)
    draw_text("Player 4: {}".format(scores[3]), 450)
    draw_text("Player 5: {}".format(scores[4]), 550)

    smallfont = pygame.font.SysFont('Corbel',35)
    text1 = smallfont.render('reset', True, RED)
    pygame.draw.rect(screen, BLACK, [650, 40, 140, 40])
    screen.blit(text1, (650 + 35, 40))

    if player_no == 1:
        smallfont = pygame.font.SysFont('Corbel', 35)
        text2 = smallfont.render('start', True, GREEN)
        pygame.draw.rect(screen, BLACK, [15, 40, 140, 40])
        screen.blit(text2, (15 + 35, 40))

    # draw grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            box_color = grid[y][x]
            pygame.draw.rect(screen, box_color, (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE))
            pygame.draw.rect(screen, BLACK, (x * BOX_SIZE, (y + 1) * BOX_SIZE, BOX_SIZE, BOX_SIZE),
                             OUTLINE_WIDTH)
    # Update the screen
    pygame.display.flip()

    start_new_thread(update_colors, (n,))

    drag = False
    sGrid = []
    start_grid_x, start_grid_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button


                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    drag = True
                    start_grid_x, start_grid_y = get_grid_pos((mouse_x, mouse_y - BOX_SIZE))
                    sGrid = [[0 for i in range(10)] for j in range(10)]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
                    colourTotal = 0
                    if 650 <= mouse_x <= 790 and 40 <= mouse_y <= 80:
                        n.send(("reset"))

                    if 50 <= mouse_x <= 190 and 40 <= mouse_y <= 80 and player_no == 1:
                        n.send(("start"))

                    for i in sGrid:
                        for k in i:
                            if k == 1:
                                colourTotal += 1
                    print("colourTotal: ", colourTotal)
                    squareCoords = str(start_grid_y) + ' ' + str(start_grid_x)
                    if colourTotal >= 50:
                        # send request to colour in the whole square the player's colour
                        n.send(("fill pass" + ' ' + squareCoords + ' ' + player_color_string + ' '))
                    else:
                        # send request to reset the square to blank
                        n.send(("fill fail" + ' ' + squareCoords + ' ' + player_color_string + ' '))
            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    motion_grid_x, motion_grid_y = get_grid_pos((mouse_x, mouse_y - BOX_SIZE))
                    if start_grid_x == motion_grid_x and start_grid_y == motion_grid_y:
                        squareCoords = str(start_grid_y) + ' ' + str(start_grid_x)
                        drawCoords = str(mouse_y - 3) + ' ' + str(mouse_x - 3)
                        if sGrid[int((mouse_x % 100) / 10)][int((mouse_y % 100) / 10)] == 0:
                            n.send(("draw" + ' ' + squareCoords + ' ' + player_color_string + ' ' + drawCoords + ' '))
                            sGrid[int((mouse_x % 100) / 10)][int((mouse_y % 100) / 10)] = 1

            elif event.type == timer_event:
                if timer:
                    clock = pygame.time.Clock()
                    seconds += 1
                    if seconds == 60:
                        seconds = 0
                        minutes += 1

                    counting_minutes = str(minutes).zfill(2)
                    counting_seconds = str(seconds).zfill(2)

                    counting_string = "%s:%s" % (counting_minutes, counting_seconds)

                    counting_text = pygame.font.SysFont('Corbel', 24).render("Timer: " + str(counting_string), 1, BLACK)
                    pygame.draw.rect(screen, WHITE, [230, 40, 200, 40])
                    screen.blit(counting_text, (230 + 25, 50))
                    pygame.display.update()
                    clock.tick(25)
                else:
                    pygame.draw.rect(screen, WHITE, [230, 40, 200, 40])
                    seconds = 0
                    minutes = 0
                    pygame.display.update()


    # Quit Pygame
    n.send("Q")
    pygame.quit()


if __name__ == '__main__':
    main()