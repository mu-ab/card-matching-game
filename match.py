import pygame
import time
from random import shuffle


pygame.init()

display_width = 900
display_height = 600
image_width = 150
image_height = 150

# colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
mmm_orange = (255, 136, 17)
mmm_orange_lite = (255, 157, 60)
mmm_yellow = (244, 208, 111)
mmm_blue = (157, 217, 210)
mmm_cream = (255, 248, 240)
mmm_purple = (128, 40, 70)
mmm_purple_lite = (93, 84, 120)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Matchie Card-Matching')
clock = pygame.time.Clock()

# win = False
run = True
original = []

# initialize the position of all concealed images
for i in range(12):
    original.append(i)
    original.append(i)

shuffle(original)

concealed = list(original)
flipped = []
found = []
missed = 0
first_card = []
has_first = False
has_second = False
second_card = []
first_flip_time = 0
second_flip_time = 0
show_time = 1
game_start_time = 0
start_screen = True


def initialize():
    # Todo: remove global variabls
    global win, run, original, concealed, flipped, found, missed, first_card, has_first, has_second, second_card
    global first_flip_time, second_flip_time, show_time, game_start_time, start_screen
    win = False
    run = True
    original = []

    # initialize the position of all concealed images
    for i in range(12):
        original.append(i)
        original.append(i)

    shuffle(original)

    concealed = list(original)
    flipped = []
    found = []
    missed = 0
    first_card = []
    has_first = False
    has_second = False
    second_card = []
    first_flip_time = 0
    second_flip_time = 0
    show_time = 1
    game_start_time = 0
    start_screen = True


def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()


def draw_start_screen(mouse):
    gameDisplay.fill(mmm_purple)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 200, "Matchie",
              (display_width / 2), 120)  # my code
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 58,
              "CARD-MATCHING BY AHMED MUSA", (display_width / 2), 165)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 35,
              "Instructions", (display_width / 2) + 26, 265)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "The game starts with all cards facing down.", (display_width / 2) + 26, 300)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "Click a card to flip it.", (display_width / 2) + 26, 320)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "If two consecutive cards that you flipped are the same, ", (display_width / 2) + 26, 340)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "these two cards will permanently face up.", (display_width / 2) + 26, 360)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "The game will end when all cards face up.", (display_width / 2) + 26, 380)
    draw_text(mmm_cream, "fonts/ARCADE.TTF", 24,
              "You can then choose to play again or exit the game.", (display_width / 2) + 26, 400)

    start = draw_interactive_button(
        mouse, 300, 50, 485, mmm_orange, mmm_orange_lite, "START", False)

    return start


def draw_win_screen(mouse):
    gameDisplay.fill(mmm_purple)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 150,
              "Congrats!", (display_width / 2), 200)
    draw_text(mmm_yellow, "fonts/ARCADE.TTF", 58,
              "You found all the pieces", (display_width / 2), 270)
    restart = draw_interactive_button(
        mouse, 300, 50, 485, mmm_orange, mmm_orange_lite, "PLAY AGAIN", True)
    return restart


def draw_text(colour, font, size, content, center_x, center_y):
    text = pygame.font.Font(font, size)
    text_surf, text_rect = text_objects(content, text, colour)
    text_rect.center = (center_x, center_y)
    gameDisplay.blit(text_surf, text_rect)


def draw_interactive_button(mouse, w, h, y, colour, secondary_colour, text, restart):
    stay_on_start_screen = True
    x = display_width / 2 - w / 2
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, secondary_colour, (x, y, w, h))
        if click[0] == 1:
            stay_on_start_screen = False
            if restart:
                initialize()
    else:
        pygame.draw.rect(gameDisplay, colour, (x, y, w, h))

    draw_text(mmm_cream, "fonts/ARCADE.TTF", 50,
              text, display_width / 2, y + 32)
    return stay_on_start_screen


def load_card_face(image_id):
    card = "./bundle1/img%s.JPG" % image_id
    img = pygame.image.load(card)
    return img


def load_card_back():
    card = "./cardback/card_back1.JPG"
    img = pygame.image.load(card)
    return img


def calculate_coord(index):
    y = int(index / 6)
    x = index - y * 6
    return [x, y]


def load_images():
    for n, j in enumerate(concealed):
        card_coord = calculate_coord(n)
        if (j == 's') or (j == 'f'):
            img = load_card_face(original[n])
        else:
            img = load_card_back()
        gameDisplay.blit(
            img, (card_coord[0] * image_width, card_coord[1] * image_height))


def identify_card(position_pressed):
    x_coord = int(position_pressed[0] / image_width)
    y_coord = int(position_pressed[1] / image_height)
    card = [x_coord, y_coord]
    return card


def calculate_index(card_pos):
    return card_pos[1] * 6 + card_pos[0]


def show_card(card_pos):
    if card_pos:
        concealed[calculate_index(card_pos)] = 's'


def flip_card(card_pos):
    if card_pos:
        concealed[calculate_index(card_pos)] = 'f'


def hide_card(card_pos):
    if card_pos:
        ind = calculate_index(card_pos)
        if concealed[ind] == 's':
            concealed[ind] = original[ind]


def check_same(card1, card2):
    if card1 and card2:
        return original[calculate_index(card1)] == original[calculate_index(card2)]


def check_win():
    is_win = True
    for item in concealed:
        if isinstance(item, int):
            is_win = False
    return is_win


# Main game loop
while run:
    ev = pygame.event.get()
    key = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            card_flipped = identify_card(pygame.mouse.get_pos())
            card_index = calculate_index(card_flipped)
            if concealed[card_index] != 's' and concealed[card_index] != 'f' and not start_screen:
                if not has_first:
                    first_flip_time = time.time()
                    first_card = card_flipped
                    show_card(card_flipped)
                    is_first_flip = False
                    has_first = True
                elif not has_second:
                    second_flip_time = time.time()
                    second_card = card_flipped
                    show_card(card_flipped)
                    has_second = True

    if has_first and has_second and check_same(first_card, second_card):
        flip_card(first_card)
        flip_card(second_card)
    if has_second and (time.time() - second_flip_time > show_time):
        hide_card(second_card)
        hide_card(first_card)
        has_first = has_second = False

    win = check_win()

    mouse = pygame.mouse.get_pos()
    if start_screen:
        start_screen = draw_start_screen(mouse)
    elif not win:
        load_images()
    else:
        restart = draw_win_screen(mouse)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
