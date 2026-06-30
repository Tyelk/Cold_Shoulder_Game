import pygame
import common
from game import Game
from main_menu import MainMenu
from transition import Transition
from end_screen import EndScreen
from fail_screen import FailScreen


def main():
    pygame.init()
    pygame.mixer.init()

    # setup screen
    common.monitor_dimensions = pygame.math.Vector2(pygame.display.Info().current_w, 
                                                    pygame.display.Info().current_w)
    transition = Transition()
    transition.display_default()
    common.scale_screen(common.screen)
    pygame.display.update()

    # load game states
    main_menu = MainMenu()
    game = Game()
    end_screen = EndScreen()
    fail_screen = FailScreen()

    # default results
    results = {"opposite": False, "path": False, "signal": False, "curb": False, 
               "reverse": False}
    
    # start loop
    current_state = "main_menu"
    while True:
        match current_state:
            case "main_menu":
                current_state = main_menu.display_menu()
            case "play_game":
                current_state, results = game.play_game()
            case "end_screen":
                current_state = end_screen.display_screen(results)
            case "fail":
                current_state = fail_screen.display_screen()
            case _:  # default (quit)
                print(current_state)
                break
    pygame.quit()


# call main (start of program)
if __name__ == "__main__":
    main()

