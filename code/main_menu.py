import pygame
import common
from element import Image, Shadow, Button, VolumeSlider, Sprite, ToggleTutorialButton
from transition import Transition
from pygame.sprite import LayeredUpdates


class MainMenu():
    def __init__(self):
        # create groups
        self.all_elements = LayeredUpdates()
        self.all_main_buttons = pygame.sprite.Group()
        self.settings_menu_buttons = pygame.sprite.Group()
        self.settings_menu_sliders = pygame.sprite.Group()
        self.transition = Transition()
        
        # load elements
        self.load_main_menu()
        self.load_settings_menu()


    def load_main_menu(self):
        # main menu elements
        background_img_path = "../graphics/road_tracks_background.png"
        title_img_path = "../graphics/title.png"
        background_size = common.main_canvas_size
        title_size = (common.main_canvas_size.x * 0.75, common.main_canvas_size.y * 0.23)
        background_pos = common.main_canvas_size / 2
        title_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.x * 0.10)
        background_name = "background"
        title_name = "title"
        background_layer = 0
        title_layer = 1
        title_shadow_offset = (-25, 25)

        # background
        background_img = pygame.image.load(background_img_path).convert_alpha()
        scaled_background_img = pygame.transform.scale(background_img, background_size)
        background_img_rect = scaled_background_img.get_frect(center = background_pos)
        background = Image(scaled_background_img, background_img_rect, background_name, 
                           background_layer)

        # title
        title_img = pygame.image.load(title_img_path).convert_alpha()
        scaled_title_img = pygame.transform.scale(title_img, title_size)
        title_img_rect = scaled_title_img.get_frect(midtop = title_pos)
        title = Image(scaled_title_img, title_img_rect, title_name, title_layer, 
                      title_shadow_offset, common.COLOUR_SHADOW)

        # buttons
        play_button_text = "PLAY"
        quit_button_text = "QUIT"
        set_button_text = "SETTINGS"
        button_font_size = 60
        button_layer = 2
        button_padding = (50, 5)
        button_depth = 10
        button_border = 10
        play_button_pos = common.main_canvas_size / 2
        settings_button_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.y * 0.65)
        quit_button_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.y * 0.8)
        shadow_offset = (-25, 25)
        shadow_colour = common.COLOUR_SHADOW
        shadow_scale = (0, 0)
        shadow_layer = 1

        # play button
        play = Button(play_button_text, button_font_size, play_button_text, button_layer, 
                      button_padding, button_depth, button_border)
        play.rect.center = play_button_pos
        play_shadow = Shadow(play.border_surf, play.rect.center, shadow_offset, shadow_colour,
                             shadow_scale, shadow_layer)
        
        # settings button
        settings = Button(set_button_text, button_font_size, set_button_text, button_layer,
                          button_padding, button_depth, button_border)
        settings.rect.center = settings_button_pos
        settings_shadow = Shadow(settings.border_surf, settings.rect.center, shadow_offset,
                                 shadow_colour, shadow_scale, shadow_layer)

        # quit button
        quit = Button(quit_button_text, button_font_size, quit_button_text, button_layer, 
                      button_padding, button_depth, button_border)
        quit.rect.center = quit_button_pos
        quit_shadow = Shadow(quit.border_surf, quit.rect.center, shadow_offset, shadow_colour,
                             shadow_scale, shadow_layer)

        # add to groups
        self.all_elements.add(background, title, title.shadow, play, play_shadow,
                        quit, quit_shadow, settings, settings_shadow)
        self.all_main_buttons.add(play, settings, quit)


    def load_settings_menu(self):
        # settings menu
        menu_img_path = "../graphics/clipboard_background_small.png"
        background_size = common.main_canvas_size
        menu_size = (common.main_canvas_size.x * 0.6, common.main_canvas_size.x * 0.8)
        screen_center = common.main_canvas_size / 2
        
        menu_background = pygame.Surface(background_size, pygame.SRCALPHA)
        menu_background.fill(common.COLOUR_DARK_MIST)
        menu_background_rect = menu_background.get_frect()

        menu_img = pygame.image.load(menu_img_path).convert_alpha()
        menu_img_scaled = pygame.transform.scale(menu_img, menu_size)
        menu_rect = menu_img_scaled.get_frect()

        # text
        font_path = "../fonts/boldpixels.boldpixels.ttf"
        menu_title_font_size = 60
        contents_fonts_size = 40
        menu_title_font_text = "SETTINGS"
        music_font_text = "MUSIC"
        effects_font_text = "EFFECTS"
        toggle_font_text = "SHOW TUTORIAL"
        font_antialias = False
        font_colour = common.COLOUR_LIGHT_BLACK
        title_pos = (menu_rect.midtop[0],  menu_rect.midtop[1] + menu_rect.height * 0.16)
        music_text_pos = (menu_rect.midtop[0], menu_rect.midtop[1] + menu_rect.height * 0.27)
        effects_text_pos = (menu_rect.midtop[0], menu_rect.midtop[1] + menu_rect.height * 0.47)
        toggle_text_pos = (menu_rect.center[0] - menu_rect.width * 0.3, 
                           menu_rect.center[1] + menu_rect.height * 0.24)

        title_font = pygame.font.Font(font_path, menu_title_font_size)
        title_font.align = pygame.FONT_CENTER
        title_font_surf = title_font.render(menu_title_font_text, font_antialias, font_colour)
        title_font_rect = title_font_surf.get_frect(midtop = title_pos)

        music_font = pygame.font.Font(font_path, contents_fonts_size)
        music_font.align = pygame.FONT_CENTER
        music_font_surf = music_font.render(music_font_text, font_antialias, font_colour)
        music_font_rect = music_font_surf.get_frect(center = music_text_pos)

        effects_font = pygame.font.Font(font_path, contents_fonts_size)
        effects_font.align = pygame.FONT_CENTER
        effects_font_surf = effects_font.render(effects_font_text, font_antialias, font_colour)
        effects_font_rect = effects_font_surf.get_frect(center = effects_text_pos)

        toggle_font = pygame.font.Font(font_path, contents_fonts_size)
        toggle_font.align = pygame.FONT_CENTER
        toggle_font_surf = toggle_font.render(toggle_font_text, font_antialias, font_colour)
        toggle_font_rect = toggle_font_surf.get_frect(midleft = toggle_text_pos)

        # place contents onto menu
        menu_img_scaled.blit(title_font_surf, title_font_rect)
        menu_img_scaled.blit(music_font_surf, music_font_rect)
        menu_img_scaled.blit(effects_font_surf, effects_font_rect)
        menu_img_scaled.blit(toggle_font_surf, toggle_font_rect)

        menu_rect.center = screen_center
        menu_background.blit(menu_img_scaled, menu_rect)
        self.settings_menu = Sprite(menu_background, menu_background_rect)

        # settings buttons
        close_button_text = "CLOSE"
        button_font_size = 40
        button_layer = 10
        button_text_padding = (50, 5)
        button_depth = 10
        button_border_thickness = 10
        close_button_pos = (screen_center[0], screen_center[1] + menu_rect.height * 0.45)
        
        close_button = Button(close_button_text, button_font_size, close_button_text,
                                button_layer, button_text_padding, button_depth, 
                                button_border_thickness)
        close_button.rect.midbottom = close_button_pos

        self.settings_menu_buttons.add(close_button)

        # toggle tutorial button
        toggle_size = common.main_canvas_size * 0.07
        toggle_depth = 5
        toggle_pos = (screen_center[0] + menu_rect.width * 0.28, 
                      screen_center[1] + menu_rect.height * 0.23)

        self.toggle_button = ToggleTutorialButton(toggle_pos, toggle_size, toggle_depth)

        # volume sliders
        slider_length = menu_rect.width * 0.6
        music_slider_pos = (screen_center[0], screen_center[1] - menu_rect.height * 0.15)
        effects_slider_pos = (screen_center[0], screen_center[1] + menu_rect.height * 0.05)

        music_slider = VolumeSlider(slider_length, music_slider_pos, music_font_text)
        effects_slider = VolumeSlider(slider_length, effects_slider_pos, effects_font_text)

        self.settings_menu_sliders.add(music_slider, effects_slider)


    def display_settings_menu(self):
        # display all settings menu options/buttons
        common.screen.blit(self.settings_menu.image, self.settings_menu.rect)
        self.settings_menu_buttons.draw(common.screen)
        for slider in self.settings_menu_sliders:
            slider.display()
        common.screen.blit(self.toggle_button.image, self.toggle_button.rect)


    def handle_settings_key(self, esc_key):
        if esc_key:
            # toggle settings menu if ESC key selected
            self.settings_menu_active = not self.settings_menu_active


    def handle_settings_menu_buttons(self):
        # check buttons
        for button in self.settings_menu_buttons:
            button.check_state()
            if button.clicked:
                button.clicked = False
                if button.name == "CLOSE": # close menu
                    self.settings_menu_active = False

        # check sliders
        for slider in self.settings_menu_sliders:
            slider.check_state()

        # check tutorial button
        self.toggle_button.check_state()


    def leave_menu(self, value):
        # leave main menu
        self.return_value = value
        self.transition.turn_on_leave_transition()
        self.end = True
        pygame.mixer.music.fadeout(1000)


    def handle_main_menu_buttons(self):
        # transition to play, quit, or open settings menu
        for button in self.all_main_buttons:
            button.check_state()
            if button.clicked:
                button.clicked = False
                match button.name:
                    case "PLAY":
                        self.leave_menu("play_game")
                    case "QUIT":
                        self.leave_menu("quit")
                    case "SETTINGS":
                        self.settings_menu_active = True
                    case _:
                        self.return_value = "unknown"
                

    def reset_menu(self):
        # reset variables
        self.transition.turn_on_arrive_transition()
        self.settings_menu_active = False
        self.return_value = "quit"
        self.end = False

        # update settings menu options
        for slider in self.settings_menu_sliders:
            slider.set_button_level()

        self.toggle_button.update_image()


    def display_menu(self):
        self.reset_menu()

        # play menu music
        self.menu_music = pygame.mixer.music.load("../audio/menu_song.mp3")
        pygame.mixer.music.play(-1)
        
        # menu loop
        running = True
        while running:
            esc_key = common.handle_events()
            if common.quit:
                return "quit"
            common.calculate_delta_time()
                    
            # clear window and screen
            common.window.fill(common.COLOUR_BLACK)
            common.screen.fill(common.COLOUR_DARK_GRAY)

            # draw elements to screen 
            self.all_elements.draw(common.screen)

            # settings menu
            if self.settings_menu_active:
                self.display_settings_menu()

            if not self.transition.active_transition:
                # only checks buttons inputs if no transition
                self.handle_settings_key(esc_key)
                if self.settings_menu_active:
                    self.handle_settings_menu_buttons()
                else:
                    self.handle_main_menu_buttons()
            else:
                self.transition.display_transition()
                if not self.transition.active_transition and self.end:
                    # only ends when transition is done
                    running = False

            # display screen
            common.scale_screen(common.screen)
            pygame.display.update()
        return self.return_value

