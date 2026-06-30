import os
import pygame
import common
from tutorial import Tutorial
from player import Player
from bike import Bike
from element import Image, AnimatedSprite, VolumeSlider, Button, ImageButton, Sprite, ToggleTutorialButton
from transition import Transition
from pygame.sprite import LayeredUpdates

class Game():
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.transition = Transition()
        self.game_loaded = False
        self.game_end = False

        # create groups
        self.all_sprites = LayeredUpdates()
        self.environment_sprites = pygame.sprite.Group()
        self.section_sprites = pygame.sprite.Group()
        self.bike_group = pygame.sprite.Group()
        self.pause_menu_buttons = pygame.sprite.Group()
        self.pause_menu_sliders = pygame.sprite.Group()

        # vars
        self.results = {}
        self.tutorial_active = True
        self.tutorial_page_num = 0

        # incidents
        self.curb_hit = False
        self.gave_way = False
        self.invalid_spacing = False

        # path
        self.last_check = 0
        self.correct_path = [('6',), ('6', 'd'), ('d',), ('a', 'd'), 
                        ('a',), ('a', 'b'), ('b',), ('3', 'b'), ('3',)]
        self.taken_path = []

        # signal
        self.correct_signal_map = [(('6',), 'N'), (('6',), 'R'), (('6', 'd'), 'R'), 
                            (('d',), 'R'), (('a', 'd'), 'R'), (('a',), 'R'), 
                            (('a', 'b'), 'R'), (('a', 'b'), 'L'), (('b',), 'L'), 
                            (('3', 'b'), 'L'), (('3',), 'L'), (('3',), 'N')]
        self.taken_signal_map = []

        # opposite lanes (opposite if contains 5, 6 or 8 2 4 at all)
        self.opposite_lanes = [('5','6'), ('8',), ('2',), ('4',)]

        # load game
        self.load_game_elements()
        self.load_detection_sections()
        self.load_player()
        self.load_goal()
        self.load_bike()
        self.load_pause_menu()
        self.tutorial = Tutorial(self.player.rect, self.goal.rect)

        # audio
        goal_reached_sfx_path = os.path.join(self.script_dir, "../audio", "goal_reached.mp3")
        crash_sfx_path = os.path.join(self.script_dir, "../audio", "crash.mp3")
        self.goal_reached_sfx = pygame.mixer.Sound(goal_reached_sfx_path)
        self.crash_sfx = pygame.mixer.Sound(crash_sfx_path)
        common.all_sound_effects.append(self.goal_reached_sfx)
        common.all_sound_effects.append(self.crash_sfx)
        


    def load_game_elements(self):
        # road
        road_img_path = os.path.join(self.script_dir, "../graphics", "road.png")
        road_img = pygame.image.load(road_img_path).convert_alpha()
        road_img_scaled = pygame.transform.scale(road_img, (common.main_canvas_size))
        road_rect = road_img_scaled.get_frect(center = common.main_canvas_size / 2)
        road = Image(road_img_scaled, road_rect, "road", 0)

        # roundabout
        roundabout_img_path = os.path.join(self.script_dir, "../graphics", "roundabout.png")
        roundabout_img = pygame.image.load(roundabout_img_path).convert_alpha()
        roundabout_img_scaled = pygame.transform.scale(roundabout_img, ((common.main_canvas_size) * 0.10))
        roundabout_rect = roundabout_img_scaled.get_frect(center = common.main_canvas_size / 2)
        roundabout = Image(roundabout_img_scaled, roundabout_rect, "roundabout", 1)

        # grass sections
        top_left_grass_img_path = os.path.join(self.script_dir, "../graphics", "top_left_grass.png")
        top_left_grass_img = pygame.image.load(top_left_grass_img_path).convert_alpha()
        top_left_grass_scaled = pygame.transform.scale(top_left_grass_img, ((common.main_canvas_size) * 0.40))
        top_left_grass_rect = top_left_grass_scaled.get_frect(topleft = (0,0))
        top_left_grass = Image(top_left_grass_scaled, top_left_grass_rect, "top_left_grass", 1)

        top_right_grass_img_path = os.path.join(self.script_dir, "../graphics", "top_right_grass.png")
        top_right_grass_img = pygame.image.load(top_right_grass_img_path).convert_alpha()
        top_right_grass_scaled = pygame.transform.scale(top_right_grass_img, ((common.main_canvas_size) * 0.40))
        top_right_grass_rect = top_right_grass_scaled.get_frect(topright = (common.main_canvas_size.x, 0))
        top_right_grass = Image(top_right_grass_scaled, top_right_grass_rect, "top_right_grass", 1)

        bot_left_grass_img_path = os.path.join(self.script_dir, "../graphics", "bot_left_grass.png")
        bot_left_grass_img = pygame.image.load(bot_left_grass_img_path).convert_alpha()
        bot_left_grass_scaled = pygame.transform.scale(bot_left_grass_img, ((common.main_canvas_size) * 0.40))
        bot_left_grass_rect = bot_left_grass_scaled.get_frect(bottomleft = (0, common.main_canvas_size.x))
        bot_left_grass = Image(bot_left_grass_scaled, bot_left_grass_rect, "bot_left_grass", 1)

        bot_right_grass_img_path = os.path.join(self.script_dir, "../graphics", "bot_right_grass.png")
        bot_right_grass_img = pygame.image.load(bot_right_grass_img_path).convert_alpha()
        bot_right_grass_scaled = pygame.transform.scale(bot_right_grass_img, ((common.main_canvas_size) * 0.40))
        bot_right_grass_rect = bot_right_grass_scaled.get_frect(bottomright = common.main_canvas_size)
        bot_right_grass = Image(bot_right_grass_scaled, bot_right_grass_rect, "bot_right_grass", 1)

        # road markings
        # create surface to place all markings onto
        mark_surf = pygame.Surface((common.main_canvas_size.x * 0.20, common.main_canvas_size.y * 0.34), pygame.SRCALPHA)
        mark_surf.fill((0,0,0,0))
        
        # place markings onto surface
        marking_width = 10
        pygame.draw.rect(mark_surf, common.COLOUR_WHITE, (5, 0, (mark_surf.get_width()/2) - marking_width /2, marking_width))
        pygame.draw.rect(mark_surf, common.COLOUR_WHITE, (mark_surf.get_width()/2 - marking_width / 2, 0, marking_width, mark_surf.get_height()))

        # bottom markings
        bot_mark_rect = mark_surf.get_frect(midbottom = (common.main_canvas_size.x/2, common.main_canvas_size.y))
        bot_mark = Image(mark_surf, bot_mark_rect, "bot_mark", 1)

        #rotate markings surface to match road
        left_mark_surf = pygame.transform.rotate(mark_surf, 270)
        left_mark_rect = left_mark_surf.get_frect(midleft = (0, common.main_canvas_size.y/2))
        left_mark = Image(left_mark_surf, left_mark_rect, "left_mark", 1)

        right_mark_surf = pygame.transform.rotate(mark_surf, 90)
        right_mark_rect = right_mark_surf.get_frect(midright = (common.main_canvas_size.x, common.main_canvas_size.y/2))
        right_mark = Image(right_mark_surf, right_mark_rect, "right_mark", 1)

        top_mark_surf = pygame.transform.rotate(mark_surf, 180)
        top_mark_rect = top_mark_surf.get_frect(midtop = (common.main_canvas_size.x/2, 0))
        top_mark = Image(top_mark_surf, top_mark_rect, "top_mark", 1)

        #add elements to groups
        self.all_sprites.add(road, roundabout, top_left_grass, top_right_grass, 
                             bot_left_grass, bot_right_grass, right_mark, bot_mark, 
                             left_mark, top_mark)
        self.environment_sprites.add(roundabout, top_left_grass, top_right_grass, 
                                     bot_left_grass, bot_right_grass)


    def load_detection_sections(self):
        # surface dimensions
        vert_road_surf = pygame.Surface((common.main_canvas_size.x * 0.10, common.main_canvas_size.y * 0.34))
        hori_road_surf = pygame.Surface((common.main_canvas_size.x * 0.34, common.main_canvas_size.y * 0.10))
        roundabout_road_surf = pygame.Surface((common.main_canvas_size.x * 0.16, common.main_canvas_size.y * 0.16))

        # hide surfaces
        vert_road_surf.fill('blue')
        hori_road_surf.fill('green')
        roundabout_road_surf.fill('yellow')
        vert_road_surf.set_alpha(0)
        hori_road_surf.set_alpha(0)
        roundabout_road_surf.set_alpha(0)

        # roads
        road_one_rect = vert_road_surf.get_frect(topright = (common.main_canvas_size.x / 2, 0))
        road_one = Image(vert_road_surf, road_one_rect, "1", 3)

        road_two_rect = vert_road_surf.get_frect(topleft = (common.main_canvas_size.x / 2, 0))
        road_two = Image(vert_road_surf, road_two_rect, "2", 3)

        road_three_rect = hori_road_surf.get_frect(bottomright = (common.main_canvas_size.x, common.main_canvas_size.y / 2))
        road_three = Image(hori_road_surf, road_three_rect, "3", 3)

        road_four_rect = hori_road_surf.get_frect(topright = (common.main_canvas_size.x, common.main_canvas_size.y / 2))
        road_four = Image(hori_road_surf, road_four_rect, "4", 3)

        road_five_rect = vert_road_surf.get_frect(bottomleft = (common.main_canvas_size.x / 2, common.main_canvas_size.y))
        road_five = Image(vert_road_surf, road_five_rect, "5", 3)

        road_six_rect = vert_road_surf.get_frect(bottomright = (common.main_canvas_size.x / 2, common.main_canvas_size.y))
        road_six = Image(vert_road_surf, road_six_rect, "6", 3)

        road_seven_rect = hori_road_surf.get_frect(topleft = (0, common.main_canvas_size.y / 2))
        road_seven = Image(hori_road_surf, road_seven_rect, "7", 3)

        road_eight_rect = hori_road_surf.get_frect(bottomleft = (0, common.main_canvas_size.y / 2))
        road_eight = Image(hori_road_surf, road_eight_rect, "8", 3)

        # roundabouts
        roundabout_a_rect= roundabout_road_surf.get_frect(bottomright = common.main_canvas_size / 2)
        roundabout_a = Image(roundabout_road_surf, roundabout_a_rect, "a", 3)

        roundabout_b_rect= roundabout_road_surf.get_frect(bottomleft = common.main_canvas_size / 2)
        roundabout_b = Image(roundabout_road_surf, roundabout_b_rect, "b", 3)

        roundabout_c_rect= roundabout_road_surf.get_frect(topleft = common.main_canvas_size / 2)
        roundabout_c = Image(roundabout_road_surf, roundabout_c_rect, "c", 3)

        roundabout_d_rect= roundabout_road_surf.get_frect(topright = common.main_canvas_size / 2)
        roundabout_d = Image(roundabout_road_surf, roundabout_d_rect, "d", 3)

        # add to group
        self.all_sprites.add(road_one, road_two, road_three, road_four, road_five, road_six, road_seven, road_eight, roundabout_a, roundabout_b, roundabout_c, roundabout_d)
        self.section_sprites.add(road_one, road_two, road_three, road_four, road_five, road_six, road_seven, road_eight, roundabout_a, roundabout_b, roundabout_c, roundabout_d)


    def load_player(self):
        # create player sprite
        start_location = pygame.math.Vector2((common.main_canvas_size.x * 0.45, 
                                              common.main_canvas_size.y * 0.90))
        player_scale = pygame.math.Vector2((common.main_canvas_size.x * 0.05, 
                                            common.main_canvas_size.y * 0.08))
        self.player = Player(start_location, player_scale, 3)
        self.all_sprites.add(self.player)


    def load_goal(self):
        # create goal sprite
        goal_img_path = os.path.join(self.script_dir, "../graphics", "ice_cream.png")
        goal_img = pygame.image.load(goal_img_path).convert_alpha()
        goal_img = pygame.transform.scale(goal_img, (common.main_canvas_size.x * 0.04, 
                                                     common.main_canvas_size.y * 0.07))
        goal_rect = goal_img.get_frect(center = (common.main_canvas_size.x * 0.95, 
                                                 common.main_canvas_size.y * 0.44))
        self.goal = AnimatedSprite(goal_img, goal_rect, 2, 0, 0, 
                                    common.main_canvas_size.y * 0.01,
                                    common.main_canvas_size.y * 0.01, 5)
        self.all_sprites.add(self.goal)

    
    def load_bike(self):
        # create bike sprite
        bike_scale = (common.main_canvas_size.x * 0.055, common.main_canvas_size.y * 0.06)
        self.bike = Bike(bike_scale, 5)
        self.all_sprites.add(self.bike)
        self.bike_group.add(self.bike)


    def load_pause_menu(self):
        # pause button
        pause_img_path = os.path.join(self.script_dir, "../graphics", "small_gear.png")
        pause_img_alt_path = os.path.join(self.script_dir, "../graphics", "small_gear_hover.png")
        pause_button_size = common.main_canvas_size * 0.05
        pause_button_pos = (common.main_canvas_size.x * 0.99, 
                               common.main_canvas_size.y * 0.01)
        pause_button_layer = 2
        pause_button_depth = 5
        pause_button_name = "pause"

        pause_img = pygame.image.load(pause_img_path).convert_alpha()
        pause_img_scaled = pygame.transform.scale(pause_img, pause_button_size)
        pause_hover_img = pygame.image.load(pause_img_alt_path).convert_alpha()
        pause_hover_img_scaled = pygame.transform.scale(pause_hover_img, 
                                                           pause_button_size)
        pause_img_rect = pause_img_scaled.get_frect(topright = pause_button_pos)
        self.pause_button = ImageButton(pause_img_scaled, pause_hover_img_scaled, 
                                       pause_img_rect, pause_button_name, pause_button_layer, pause_button_depth)

        # pause menu
        background_size = common.main_canvas_size
        menu_size = (common.main_canvas_size.x * 0.7, common.main_canvas_size.x * 0.9)
        screen_center = common.main_canvas_size / 2
        
        menu_background = pygame.Surface(background_size, pygame.SRCALPHA)
        menu_background.fill(common.COLOUR_DARK_MIST)
        menu_background_rect = menu_background.get_frect()

        menu_img_path = os.path.join(self.script_dir, "../graphics", "clipboard_background_small.png")
        menu_img = pygame.image.load(menu_img_path).convert_alpha()
        menu_img_scaled = pygame.transform.scale(menu_img, menu_size)
        menu_rect = menu_img_scaled.get_frect()

        # text
        font_path = os.path.join(self.script_dir, "../fonts", "boldpixels.boldpixels.ttf")
        menu_title_font_size = 60
        contents_fonts_size = 40
        menu_title_font_text = "PAUSED"
        music_font_text = "MUSIC"
        effects_font_text = "EFFECTS"
        toggle_font_text = "SHOW TUTORIAL"
        font_antialias = False
        font_colour = common.COLOUR_LIGHT_BLACK
        title_pos = (menu_rect.midtop[0],  menu_rect.midtop[1] + menu_rect.height * 0.16)
        music_text_pos = (menu_rect.center[0], menu_rect.center[1] - menu_rect.height * 0.1)
        effects_text_pos = (menu_rect.center[0], menu_rect.center[1] + menu_rect.height * 0.1)
        toggle_text_pos = (menu_rect.center[0] - menu_rect.width * 0.25, 
                           menu_rect.center[1] + menu_rect.height * 0.3)

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
        self.pause_menu = Sprite(menu_background, menu_background_rect)

        # settings buttons
        resume_button_text = "RESUME"
        reset_button_text = "RESET"
        menu_button_text = "MENU"
        button_font_size = 40
        button_layer = 10
        button_text_padding = (50, 5)
        button_depth = 10
        button_border_thickness = 10
        resume_button_pos = (screen_center[0], screen_center[1] - (menu_rect.height * 0.24))
        reset_button_pos = (screen_center[0] - (menu_rect.width * 0.35), 
                            screen_center[1] + (menu_rect.height * 0.45))
        menu_button_pos = (screen_center[0] + (menu_rect.width * 0.35), 
                           screen_center[1] + (menu_rect.height * 0.45))
        
        resume_button = Button(resume_button_text, button_font_size, resume_button_text,
                                button_layer, button_text_padding, button_depth, 
                                button_border_thickness)
        resume_button.rect.midtop = resume_button_pos
        reset_button = Button(reset_button_text, button_font_size, reset_button_text,
                                button_layer, button_text_padding, button_depth, 
                                button_border_thickness)
        reset_button.rect.bottomleft = reset_button_pos
        menu_button = Button(menu_button_text, button_font_size, menu_button_text,
                                button_layer, button_text_padding, button_depth, 
                                button_border_thickness)
        menu_button.rect.bottomright = menu_button_pos

        self.pause_menu_buttons.add(resume_button, reset_button, menu_button)

        # toggle tutorial button
        toggle_size = common.main_canvas_size * 0.07
        toggle_depth = 5
        toggle_pos = (screen_center[0] + menu_rect.width * 0.25, 
                      screen_center[1] + menu_rect.height * 0.3)

        self.toggle_button = ToggleTutorialButton(toggle_pos, toggle_size, toggle_depth)

        # volume sliders
        music_slider_type = "MUSIC"
        effects_slider_type = "EFFECTS"
        slider_length = menu_rect.width * 0.5
        music_slider_pos = (screen_center[0], screen_center[1] - menu_rect.height * 0.04)
        effects_slider_pos = (screen_center[0], screen_center[1] + menu_rect.height * 0.16)

        music_slider = VolumeSlider(slider_length, music_slider_pos, music_slider_type)
        effects_slider = VolumeSlider(slider_length, effects_slider_pos, effects_slider_type)

        self.pause_menu_sliders.add(music_slider, effects_slider)


    def track_path(self):
        # if less than 200 ms since last track check return without checking
        # (done to allow for buffer to prevent false positives)
        if pygame.time.get_ticks() - self.last_check >= 200:

            # checks sections car is currently in
            current_sections = pygame.sprite.spritecollide(self.player, self.section_sprites, 
                                                           False, pygame.sprite.collide_mask)

            # gets name of each section (can be in multiple sections)
            current_path = []
            for sect in current_sections:
                current_path.append(sect.name)

            # if no sections in list OR current sections are different add to list
            if len(self.taken_path) == 0 or self.taken_path[-1] != tuple(current_path):
                self.taken_path.append(tuple(current_path))

            # return a new check time
            self.last_check = pygame.time.get_ticks()


    def track_signals(self):
        # gets the players current signaling (L = left, R = right, N = no indication)
        current_indication = "L" if self.player.left_indicator \
                                else ("R" if self.player.right_indicator else "N")

        # combines current section and indication
        location_signal = (self.taken_path[-1], current_indication)

        # if no items in list or current combination is different add to list
        if len(self.taken_signal_map) == 0 or self.taken_signal_map[-1] != location_signal:
            self.taken_signal_map.append(location_signal)


    def check_for_curb_collision(self):
        if self.curb_hit:
            return
        # only check for curb hit if no curb is currently hit
        self.curb_hit = bool(pygame.sprite.spritecollide(self.player, 
                                                            self.environment_sprites, False, 
                                                            pygame.sprite.collide_mask))


    def check_give_way(self):
        if self.gave_way:
            return
        
        # check distance between bike and waypoint
        give_way_point = pygame.math.Vector2(common.main_canvas_size.x * 0.45, 
                                             common.main_canvas_size.y * 0.55)
        current_location = self.bike.current_location
        distance_diff = current_location.distance_to(give_way_point)

        # if player has not left starting road and bike reaches waypoint then giveway is true
        hit_distance = 40
        correct_point = self.taken_path[0] == self.correct_path[0]
        correct_length = len(self.taken_path) == 1
        if distance_diff <= hit_distance and correct_point and correct_length:
            self.gave_way = True


    def check_spacing(self):
        if self.invalid_spacing:
            return

        # gets distance between the bike and player
        player_pos = pygame.math.Vector2(self.player.car_location)
        distance_diff = self.bike.current_location.distance_to(player_pos)

        # if the distance is at or below the threshold the spacing is invalid
        hit_distance = 80
        if distance_diff <= hit_distance:
            self.invalid_spacing = True

    
    def check_bike_hit(self):
        self.bike_hit = bool(pygame.sprite.spritecollide(self.player, self.bike_group, False,
                                                         pygame.sprite.collide_mask))
        
        if self.bike_hit: # hard fail if hit (no transition)
            self.crash_sfx.play()
            self.return_value = "fail"
            self.running = False


    def check_goal_reached(self):
        if self.player.rect.colliderect(self.goal.rect):
            # if player reaches the goal play activate end delay and set results
            self.goal_reached = True
            self.goal_reached_sfx.play()
            self.goal_reached_time = pygame.time.get_ticks()
            self.calculate_result()


    def calculate_result(self):
        # checks how the player did
        self.results["gave_way"] = self.gave_way
        self.results["spacing"] = not self.invalid_spacing
        self.results["opposite"] = bool(not any(pos in self.taken_path 
                                            for pos in self.opposite_lanes))    # checks path taken does not inclue opposite lanes
        self.results["path"] = bool(self.taken_path == self.correct_path)
        self.results["signal"] = bool(self.taken_signal_map == self.correct_signal_map)
        self.results["curb"] = not self.curb_hit
        self.results["reverse"] = not self.player.reversed


    def handle_pause_buttons(self, esc_key):
        self.pause_button.check_state()
        if self.pause_button.clicked or esc_key:
            # toggle pause menu if ESC key or pause button selected
            self.pause_button.clicked = False
            self.pause_menu_active = not self.pause_menu_active


    def display_pause_menu(self):
        # display pause menu and buttons
        common.screen.blit(self.pause_menu.image, self.pause_menu.rect)
        self.pause_menu_buttons.draw(common.screen)
        for slider in self.pause_menu_sliders:
            slider.display()
        common.screen.blit(self.toggle_button.image, self.toggle_button.rect)
                

    def handle_pause_menu_buttons(self):
        # check buttons
        for button in self.pause_menu_buttons:
            button.check_state()
            if button.clicked:
                button.clicked = False
                if button.name == "RESUME": # resumes game
                    self.pause_menu_active = False
                elif button.name == "RESET":    # resets game
                    self.end_game("play_game")
                elif button.name == "MENU": # goes to main menu
                    self.end_game("main_menu")
        
        # check sliders
        for slider in self.pause_menu_sliders:
            slider.check_state()

        # check tutorial button
        self.toggle_button.check_state()


    def end_game(self, value):
        # sets values to end the game in the game loop
        self.return_value = value
        self.transition.turn_on_leave_transition()
        self.end = True


    def delay_end(self):
        current_time_delay = pygame.time.get_ticks() - self.goal_reached_time
        target_delay = 700

        # wait delay then end game
        if current_time_delay >= target_delay:
            self.goal_reached = False
            self.end_game("end_screen")


    def reset_game(self):
        # reset variables
        self.transition.turn_on_arrive_transition()
        self.pause_menu_active = False
        self.return_value = "quit"
        self.goal_reached = False
        self.end = False
        self.player.reset()
        self.bike.reset()
        self.taken_path = []
        self.taken_signal_map = []

        self.bike_hit = False
        self.curb_hit = False
        self.gave_way = False
        self.invalid_spacing = False

        # update pause menu options
        for slider in self.pause_menu_sliders:
            slider.set_button_level()

        self.toggle_button.update_image()

        # only display tutorial if still activated in menu
        self.tutorial.active = common.tutorial_active
        self.tutorial.current_page = 0


    def run_game_logic(self):
        # move elements and check and track the player
        self.player.input_check()
        self.bike.update_bike()
        self.track_path()
        self.track_signals()
        self.check_for_curb_collision()
        self.check_give_way()
        self.check_spacing()
        self.check_goal_reached()
        self.check_bike_hit()


    def play_game(self):
        self.reset_game()

        # play game music
        menu_music_path = os.path.join(self.script_dir, "../audio", "play_song.mp3")
        self.menu_music = pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.play(-1)

        # game loop
        self.running = True
        while self.running:
            esc_key = common.handle_events()
            if common.quit:
                return "quit", self.results
            common.calculate_delta_time()

            # clear screen
            common.window.fill(common.COLOUR_BLACK)
            common.screen.fill(common.COLOUR_DARK_GRAY)

            # update sprites
            self.all_sprites.update()

            # draw elements to screen
            self.all_sprites.draw(common.screen)

            # tutorial
            if self.tutorial.active:
                self.tutorial.display_tutorial()

            # pause menu
            if self.pause_menu_active:
                self.display_pause_menu()

            # draw pause button ontop of any other menu
            common.screen.blit(self.pause_button.image, self.pause_button.rect)

            # delay end
            if self.goal_reached:
                self.delay_end()
            elif not self.transition.active_transition: # NO current transition
                self.handle_pause_buttons(esc_key)
                if self.pause_menu_active:  # game paused
                    self.handle_pause_menu_buttons()
                elif self.tutorial.active: # tutorial and game unpaused
                    self.tutorial.handle_tutorial_buttons()
                else:  # unpaused and not tutorial
                    self.run_game_logic()
            else:   # active transition
                self.transition.display_transition()
                if not self.transition.active_transition and self.end:
                    # only ends when transition is done
                    self.running = False

            # display screen
            common.scale_screen(common.screen)
            pygame.display.update()

        return self.return_value, self.results


