# Example file showing a basic pygame "game loop"
import pygame
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
w, h = pygame.display.get_surface().get_size()

letter_f = pygame.font.SysFont("sans", 45)

rad = 50
gap = 5
buttons = []
firstx = round((w+500 - (rad * 2 + gap) * 6)/2)
firsty = 30
firstl = 65
for i in range(26):
    x = firstx + gap * 2 + ((rad * 2 + gap) * (i % 6))
    y = firsty + ((i // 6) * (gap + rad * 2))
    buttons.append([x, y, chr(firstl+i), True])

# load images
images = []
for i in range(7):
    image = pygame.image.load("images/hangman" + str(i) + ".png")
    images.append(image)

num_hangman = 0
key_w = w-700
key_h = 100

def draw():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for char in buttons:
        x, y, letter, visibility = char
        if visibility:
            pygame.draw.rect(screen, "black", pygame.Rect(x,y,rad, rad))
            t = letter_f.render(letter,1, "green")
            screen.blit(t, (x+(rad/4),y))

    # pygame.draw.rect(screen, "red", pygame.Rect(x,y,50, 50))
    # RENDER YOUR GAME HERE
    screen.blit(images[num_hangman], (w-w+50, 25))

    # flip() the display to put your work on screen
    pygame.display.flip()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for char in buttons:
                x, y, letter, visibility = char
                if visibility:
                    square = pygame.Rect(x, y, rad, rad)
                    if square.collidepoint(mouse_pos):
                        char[3] = False
    draw()

    clock.tick(60)  # limits FPS to 60

pygame.quit()