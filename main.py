# imports
import pygame
import json
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
w, h = pygame.display.get_surface().get_size()

# fonts
tiny_f = pygame.font.SysFont("sans", 20)
smaller_f = pygame.font.SysFont("sans", 30)
letter_f = pygame.font.SysFont("sans", 45)
bigger_f = pygame.font.SysFont("sans", 90)

# initializing variables
num_hangman = 0
key_w = w-700
key_h = 100
end_x = w/2-150
end_y = h/2-100
rad = 50
gap = 5
buttons = []
firstx = round((w+400 - (rad * 2 + gap) * 6)/2)
firsty = 30
firstl = 65

# for loop to create the placement for buttons
for i in range(26):
    x = firstx + gap * 2 + ((rad * 2 + gap) * (i % 7))
    y = firsty + ((i // 7) * (gap + rad * 2))
    buttons.append([x, y, chr(firstl+i), True])

# load images
images = []
for i in range(7):
    image = pygame.image.load("images/hangman" + str(i) + ".png")
    images.append(image)

# function to draw everything
def draw():
    screen.fill("white")
    
    # to check what words are guessed and should be drawn
    word_d = ""
    for i in word:
        if i in guessed:
            word_d += i + " "
        else:
            word_d += "_ "
    t = bigger_f.render(word_d, 1, "black")
    screen.blit(t, (50, 550))
        
    # for loop to draw all buttons
    for char in buttons:
        x, y, letter, visibility = char
        if visibility:
            pygame.draw.rect(screen, "black", pygame.Rect(x,y,rad, rad))
            t = letter_f.render(letter,1, "cyan")
            screen.blit(t, (x+(rad/4),y))

    screen.blit(images[num_hangman], (50, 25))
    pygame.display.flip()

# reset game function
def reset_game():
    global num_hangman, guessed, word
    num_hangman = 0
    guessed = []

    # reseting buttons to be all visible
    for char in buttons:
        char[3] = True

    # picking a random word    
    word_chose = random.randint(0, 49)
    with open("animal_list.json") as file:
        data = json.load(file)
    word = data[word_chose].upper()
    
# main function
def main():
    global running, num_hangman
    reset_game()
    
    # while loop for when the code is running
    while running:
        clock.tick(60)
        
        # for loop for any event to check it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # for loop to see if a button is pressed
                for char in buttons:
                    x, y, letter, visibility = char
                    if visibility:
                        square = pygame.Rect(x, y, rad, rad)
                        if square.collidepoint(mouse_pos):
                            char[3] = False
                            guessed.append(letter)
                            if letter not in word:
                                num_hangman += 1

        draw()
        # checking if they guessed the word
        end = True
        for i in word:
                if i not in guessed:
                    end = False
                    break
        # if to check if they won or lost
        if end or num_hangman == 6:
            pygame.draw.rect(screen, "grey", pygame.Rect(end_x,end_y,300, 200))  
            pygame.draw.rect(screen, "beige", pygame.Rect(end_x+ 50,end_y+ 140,200, 50))      
            message = "YOU GOT IT" if end else "YOU FAILED"
            t = letter_f.render(message, 1, "black")
            screen.blit(t,(w/2 - t.get_width()/2, end_y+20))
            t1 = smaller_f.render("NEW GAME",1, "black")
            screen.blit(t1,(w/2 - t.get_width()/2+ 40, end_y+150))
            t2 = tiny_f.render("Correct: " + word,1, "black")
            screen.blit(t2,(w/2 - t.get_width()/2 + 20, end_y+80))
            pygame.display.update()

            # checking for playing again
            play_again = False
            while not play_again:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # checking if the play again button is pressed
                        mouse_pos = pygame.mouse.get_pos()
                        square = pygame.Rect(end_x+ 50, end_y+ 80, 200, 100)
                        if square.collidepoint(mouse_pos):
                            play_again = True
                            reset_game()
                            break
main()
pygame.quit()