import pygame
import common
from element import Sprite, Button
from transition import Transition


class FailScreen():
    def __init__(self):
        self.transition = Transition()
        self.all_elements = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.shroud_value = 255
        self.previous_time = 0
        self.finished_updating = False
        self.create_screen()


    def create_button_element(self, text, pos):
        # button settings
        end_button_font_size = 40
        end_button_layer = 10
        end_button_text_padding = (50, 5)
        end_button_depth = 10
        end_button_border_thickness = 10

        # create button
        button = Button(text, end_button_font_size, text, end_button_layer,
                        end_button_text_padding, end_button_depth, end_button_border_thickness)
        button.rect.center = pos

        # add to list
        self.all_buttons.add(button)


    def create_screen(self):
        # create background
        background_img = pygame.image.load("../graphics/bloody_ice_cream.png").convert_alpha()
        scaled_background_img = pygame.transform.scale(background_img, common.main_canvas_size)
        background_rect = scaled_background_img.get_frect(center = common.main_canvas_size / 2)
        background = Sprite(scaled_background_img, background_rect)

        # font attributes
        font_path = "../fonts/boldpixels.boldpixels.ttf"
        title_font_size = 120
        subtitle_font_size = 50
        font_antialias = False
        title_font_text = "BLOODY IDIOT"
        subtitle_font_text = "RESPECT CYCLISTS ON THE ROAD"
        font_colour = common.COLOUR_DARK_OFF_WHITE
        title_text_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.y * 0.15)
        subtitle_text_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.y * 0.25)

        # create font and create sprite
        title_font = pygame.font.Font(font_path, title_font_size)
        title_font.align = pygame.FONT_CENTER
        title_font_surf = title_font.render(title_font_text, font_antialias, font_colour)
        title_font_rect = title_font_surf.get_frect(center = title_text_pos)
        title_text = Sprite(title_font_surf, title_font_rect)

        # create font and create sprite
        subtitle_font = pygame.font.Font(font_path, subtitle_font_size)
        subtitle_font.align = pygame.FONT_CENTER
        subtitle_font_surf = subtitle_font.render(subtitle_font_text, font_antialias, 
                                                  font_colour)
        subtitle_font_rect = subtitle_font_surf.get_frect(center = subtitle_text_pos)
        subtitle_text = Sprite(subtitle_font_surf, subtitle_font_rect)

        # create shroud
        shroud_surf = pygame.Surface(common.main_canvas_size)
        shroud_surf.fill(common.COLOUR_BLACK) 
        shroud_surf.set_alpha(self.shroud_value)
        shroud_rect = shroud_surf.get_frect(center = common.main_canvas_size / 2)
        shroud = Sprite(shroud_surf, shroud_rect)

        # add all elements to group
        self.all_elements.add(background, title_text, subtitle_text, shroud)

        # end screen buttons
        replay_button_text = "REPLAY"
        quit_button_text = "MENU"
        replay_button_pos = (common.main_canvas_size.x * 0.33, common.main_canvas_size.y * 0.90)
        quit_button_pos = (common.main_canvas_size.x * 0.66, common.main_canvas_size.y * 0.90)

        # create buttons
        self.create_button_element(replay_button_text, replay_button_pos)
        self.create_button_element(quit_button_text, quit_button_pos)


    def handle_buttons(self):
        # check all buttons states
        for button in self.all_buttons:
            button.check_state()
            if button.clicked:
                button.clicked = False
                # leave screen when button selected
                if button.name == "REPLAY":
                    self.return_value = "play_game"
                elif button.name == "MENU":
                    self.return_value = "main_menu"
                self.transition.turn_on_leave_transition()
                self.end = True
                pygame.mixer.music.fadeout(1000)

        # display all buttons
        self.all_buttons.draw(common.screen)


    def update_shroud(self):
        # get last item in group (the shroud) and update its alpha level
        list(self.all_elements)[-1].image.set_alpha(self.shroud_value)


    def update_display(self):
        # start music after 1 sec delay & start removing shroud after 2 seconds
        current_start_time_diff = pygame.time.get_ticks() - self.start_time
        start_music_delay = 1000
        start_unveil_delay = 2000
        if current_start_time_diff <= start_music_delay:
            pygame.mixer.music.play(-1)
        if current_start_time_diff <= start_unveil_delay:
            return

        current_time_diff = pygame.time.get_ticks() - self.previous_time
        delay = 50

        if current_time_diff >= delay:
            # update shroud then decrease its value
            self.update_shroud()
            self.shroud_value -= 3
            self.previous_time = pygame.time.get_ticks()
            # once shroud is fully unveiled finish updating
            if self.shroud_value <= 0:
                self.finished_updating = True


    def reset_display(self):
        # resets elements to defautl values
        self.shroud_value = 255
        self.previous_time = 0
        self.finished_updating = False
        self.update_shroud()


    def display_screen(self):
        self.reset_display()

        self.fail_music = pygame.mixer.music.load("../audio/fail_song.mp3")
        self.start_time = pygame.time.get_ticks()

        # loop variables
        self.return_value = "quit"
        self.end = False
        running = True
        while running:
            common.handle_events()
            if common.quit:
                return "quit"
            common.calculate_delta_time()
                    
            # clear window and screen
            common.window.fill(common.COLOUR_BLACK)
            common.screen.fill(common.COLOUR_BLACK)

            # draw elements to screen 
            self.all_elements.draw(common.screen)

            # only update if not active transition
            if not self.transition.active_transition:
                if not self.finished_updating:
                    self.update_display()
                else:
                    self.handle_buttons()
            else:
                self.transition.display_transition()
                if not self.transition.active_transition and self.end:
                    # only ends when transition is done
                    running = False

            # display screen
            common.scale_screen(common.screen)
            pygame.display.update()
        return self.return_value