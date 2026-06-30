import pygame

# global attributes
quit = False
fullscreen = False
monitor_dimensions = None
screen_size = pygame.math.Vector2(1000, 1000)
main_canvas_size = pygame.math.Vector2(1000, 1000)
screen_pos = pygame.math.Vector2(0, 0)
window = pygame.display.set_mode(main_canvas_size, pygame.RESIZABLE)
screen = pygame.Surface(main_canvas_size)
clock = pygame.time.Clock()
delta_time = 0
music_volume = 1
effects_volume = 1
all_sound_effects = []
tutorial_active = True

# colours
COLOUR_WHITE = (255,255,255)
COLOUR_OFF_WHITE = (252,247,245)
COLOUR_DARK_OFF_WHITE = (242,240,239)
COLOUR_LIGHT_GRAY = (150,150,150)
COLOUR_DARK_GRAY = (50,50,50)
COLOUR_BLACK = (0,0,0)
COLOUR_LIGHT_BLACK = (20,20,20)
COLOUR_RED = (183,11,11)
COLOUR_ORANGE = (255,189,54)
COLOUR_GREEN = (132,249,54)
COLOUR_PINK = (166, 17, 189)
COLOUR_SHADOW = (0,0,0,128)
COLOUR_DARK_MIST = (0,0,0,240)


def update_screen_size(new_size):
    global screen_size

    # make screen scale the smallest of the windows measurements
    smallest_dimension = new_size[0] if new_size[0] < new_size[1] else new_size[1]

    # set global variable 
    screen_size = pygame.math.Vector2(smallest_dimension, smallest_dimension)


def handle_events():
    global quit
    global window
    global fullscreen

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit entire game
            quit = True
        if event.type == pygame.VIDEORESIZE:
            # update screen when resized
            update_screen_size(event.size)
        if event.type == pygame.KEYDOWN:
            # full screen
            if event.key == pygame.K_F11:
                if fullscreen:
                    window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
                else:
                    window = pygame.display.set_mode(monitor_dimensions, pygame.FULLSCREEN)
                fullscreen = not fullscreen
            if event.key == pygame.K_ESCAPE:
                return True
            else:
                return False


def scale_screen(new_screen):
    global screen_pos

    # scale screen and place in center of window
    scaled_screen = pygame.transform.scale(new_screen, screen_size)
    scaled_rect = scaled_screen.get_frect(center = (window.get_width()/2, window.get_height()/2))

    # set screen position 
    screen_pos = pygame.Vector2(scaled_rect.topleft)

    # print screen onto window
    window.blit(scaled_screen, scaled_rect)


def calculate_delta_time():
    # calculate delta time depending on the frame rate
    global delta_time
    delta_time = clock.tick() / 1000    # uncapped frame rate


def change_music_volume(volume):
    # set and save music volume across pages
    global music_volume
    music_volume = volume
    pygame.mixer.music.set_volume(volume)

def change_effects_volume(volume):
    # set and save effects volume across pages
    global effects_volume
    effects_volume = volume
    for effect in all_sound_effects:
        effect.set_volume(volume)