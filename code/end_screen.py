import os
import pygame
import common
from element import Sprite, ToggleImage, Button
from transition import Transition

class EndScreen():
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.finished_updating = False

        # setup visuals
        self.all_elements = pygame.sprite.Group()
        self.all_result_text = pygame.sprite.Group()
        self.all_tickboxes = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        self.all_grade_elements = pygame.sprite.Group()
        self.transition = Transition()
        self.create_end_screen()

        # setup audio
        success_sfx_path = os.path.join(self.script_dir, "../audio", "success.mp3")
        fail_sfx_path = os.path.join(self.script_dir, "../audio", "fail.mp3")
        bad_grade_sfx_path = os.path.join(self.script_dir, "../audio", "bad_score.mp3")
        ok_grade_sfx_path = os.path.join(self.script_dir, "../audio", "ok_score.mp3")
        great_grade_sfx_path = os.path.join(self.script_dir, "../audio", "great_score.mp3")
        self.success_sfx = pygame.mixer.Sound(success_sfx_path)
        self.fail_sfx = pygame.mixer.Sound(fail_sfx_path)
        self.bad_grade_sfx = pygame.mixer.Sound(bad_grade_sfx_path)
        self.ok_grade_sfx = pygame.mixer.Sound(ok_grade_sfx_path)
        self.great_grade_sfx = pygame.mixer.Sound(great_grade_sfx_path)
        common.all_sound_effects.append(self.success_sfx)
        common.all_sound_effects.append(self.fail_sfx)
        common.all_sound_effects.append(self.bad_grade_sfx)
        common.all_sound_effects.append(self.ok_grade_sfx)
        common.all_sound_effects.append(self.great_grade_sfx)


    def create_text_element(self, font_size, font_text, font_colour, text_pos, pos_left=True, 
                            grade=False):
        font_path = os.path.join(self.script_dir, "../fonts", "boldpixels.boldpixels.ttf")
        font_antialias = False

        # create font and create sprite
        font = pygame.font.Font(font_path, font_size)
        font.align = pygame.FONT_CENTER
        font_surf = font.render(font_text, font_antialias, font_colour)
        if pos_left:    # align text to the left
            font_rect = font_surf.get_frect(midleft = text_pos)
        else:
            font_rect = font_surf.get_frect(center = text_pos)
        text = Sprite(font_surf, font_rect)

        # add to lists
        self.all_result_text.add(text)
        if grade:
            self.all_grade_elements.add(text)


    def create_tickbox_element(self, empty_tb, success_tb, fail_tb, tb_pos, name, layer):
        # create sprite
        rect = empty_tb.get_frect(center = tb_pos)
        tickbox = ToggleImage(empty_tb, success_tb, fail_tb, rect, name, layer)

        # add to list
        self.all_tickboxes.add(tickbox)


    def create_button_element(self, text, pos):
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


    def create_end_screen(self):
        # end screen
        end_screen_size = common.main_canvas_size
        end_screen_background = pygame.Surface(end_screen_size, pygame.SRCALPHA)
        end_screen_background.fill(common.COLOUR_BLACK)
        end_screen_background_rect = end_screen_background.get_frect()
        end_screen = Sprite(end_screen_background, end_screen_background_rect)
        self.all_elements.add(end_screen)

        # end screen buttons
        replay_button_text = "REPLAY"
        quit_button_text = "MENU"
        replay_button_pos = (common.main_canvas_size.x * 0.33, common.main_canvas_size.y * 0.90)
        quit_button_pos = (common.main_canvas_size.x * 0.66, common.main_canvas_size.y * 0.90)
        
        # create buttons
        self.create_button_element(replay_button_text, replay_button_pos)
        self.create_button_element(quit_button_text, quit_button_pos)

        # font values
        body_text_size = 35
        font_colour = common.COLOUR_DARK_OFF_WHITE
        gave_way_font_text = "GAVE WAY TO THE BIKE"
        spacing_font_text = "GAVE APPROPRIATE SPACING"
        opposite_font_text = "STAYED IN THE CORRECT LANES"
        path_font_text = "TOOK THE OPTIMAL PATH"
        signal_font_text = "CORRECT PATH AND SIGNALING"
        curb_font_text = "DID NOT HIT A CURB"
        reverse_font_text = "DID NOT REVERSE"
        
        gave_way_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.25)
        spacing_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.3)
        opposite_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.35)
        path_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.40)
        signal_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.45)
        curb_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.50)
        reverse_text_pos = (common.main_canvas_size.x * 0.1, common.main_canvas_size.y * 0.55)
        
        # creating text
        self.create_text_element(body_text_size, gave_way_font_text, font_colour, 
                                 gave_way_text_pos)
        self.create_text_element(body_text_size, spacing_font_text, font_colour, spacing_text_pos)
        self.create_text_element(body_text_size, opposite_font_text, font_colour, 
                                 opposite_text_pos)
        self.create_text_element(body_text_size, path_font_text, font_colour, path_text_pos)
        self.create_text_element(body_text_size, signal_font_text, font_colour, signal_text_pos)
        self.create_text_element(body_text_size, curb_font_text, font_colour, curb_text_pos)
        self.create_text_element(body_text_size, reverse_font_text, font_colour, reverse_text_pos)

        # tickbox
        empty_tickbox_path = os.path.join(self.script_dir, "../graphics", "empty_tickbox.png")
        success_tickbox_path = os.path.join(self.script_dir, "../graphics", "success_tickbox.png")
        failure_tickbox_path = os.path.join(self.script_dir, "../graphics", "failure_tickbox.png")
        tickbox_size = common.main_canvas_size * 0.05
        gw_tb_name = "gave_way"
        space_tb_name = "spacing"
        opp_tb_name = "opposite"
        path_tb_name = "path"
        signal_tb_name = "signal"
        curb_tb_name = "curb"
        rev_tb_name = "reverse"
        layer = 2

        gw_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.25)
        space_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.3)
        opp_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.35)
        path_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.4)
        signal_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.45)
        curb_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.50)
        rev_tickbox_pos = (common.main_canvas_size.x * 0.8, common.main_canvas_size.y * 0.55)

        empty_tickbox = pygame.image.load(empty_tickbox_path).convert_alpha()
        empty_tickbox_scaled = pygame.transform.scale(empty_tickbox, tickbox_size)
        success_tickbox = pygame.image.load(success_tickbox_path).convert_alpha()
        success_tickbox_scaled = pygame.transform.scale(success_tickbox, tickbox_size)
        failure_tickbox = pygame.image.load(failure_tickbox_path).convert_alpha()
        failure_tickbox_scaled = pygame.transform.scale(failure_tickbox, tickbox_size)

        # create tickboxes
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, gw_tickbox_pos, gw_tb_name, 
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, space_tickbox_pos, space_tb_name, 
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, opp_tickbox_pos, opp_tb_name, 
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, path_tickbox_pos, path_tb_name, 
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, signal_tickbox_pos, signal_tb_name,
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, curb_tickbox_pos, curb_tb_name, 
                                       layer)
        self.create_tickbox_element(empty_tickbox_scaled, success_tickbox_scaled, 
                                       failure_tickbox_scaled, rev_tickbox_pos, rev_tb_name, 
                                       layer)


    def create_grade(self, grade, message):
        # create grade label
        grade_label_font_size = 50
        grade_label_text = "GRADE:"
        align_left = False
        grade_element = True
        grade_label_font_colour = common.COLOUR_DARK_OFF_WHITE
        grade_label_pos = (common.main_canvas_size.x * 0.45, common.main_canvas_size.y * 0.7)
        self.create_text_element(grade_label_font_size, grade_label_text,
                                 grade_label_font_colour, grade_label_pos, align_left, 
                                 grade_element)
        
        # create grade
        label_font_size = 60
        if grade.startswith(("A", "B")):
            grade_font_colour = common.COLOUR_GREEN
            self.grade_level = "great"
        elif grade.startswith("C"):
            grade_font_colour = common.COLOUR_ORANGE
            self.grade_level = "ok"
        else:
            grade_font_colour = common.COLOUR_RED
            self.grade_level = "bad"
        grade_pos = (common.main_canvas_size.x * 0.6, common.main_canvas_size.y * 0.7)
        self.create_text_element(label_font_size, grade, grade_font_colour, grade_pos,
                                 align_left, grade_element)

        # create title message
        if grade == "A+":
            title_font_colour = common.COLOUR_PINK
        else:
            title_font_colour = common.COLOUR_DARK_OFF_WHITE
        title_font_size = 100
        title_text_pos = (common.main_canvas_size.x / 2, common.main_canvas_size.y * 0.1)
        self.create_text_element(title_font_size, message, title_font_colour, title_text_pos, 
                                 align_left, grade_element)


    def calculate_results(self):
        # count trues
        total_passed = 0
        total_results = len(self.results)
        for value in self.results.values():
            if value:
                total_passed += 1
        
        # calcualte percentage
        percentage = (total_passed / total_results) * 100

        # grade result
        grade = ""
        message = ""
        if percentage >= 90:
            grade = "A+"
            message = "NICE CREAM"
        elif percentage >= 85:
            grade = "A"
            message = "NICE"
        elif percentage >= 80:
            grade = "A-"
            message = "NICE"
        elif percentage >= 75:
            grade = "B+"
            message = "GOOD JOB"
        elif percentage >= 70:
            grade = "B"
            message = "GOOD JOB"
        elif percentage >= 65:
            grade = "B-"
            message = "GOOD JOB"
        elif percentage >= 60:
            grade = "C+"
            message = "THATS ROUGH BUDDY"
        elif percentage >= 55:
            grade = "C"
            message = "THATS ROUGH BUDDY"
        elif percentage >= 50:
            grade = "C-"
            message = "THATS ROUGH BUDDY"
        elif percentage >= 40:
            grade = "D"
            message = "YIKES"
        else:
            grade = "E"
            message = "PLEASE DONT DRIVE"

        # create grade elements
        self.create_grade(grade, message)


    def handle_buttons(self):
        # check all buttons
        for button in self.all_buttons:
            # activate all buttons and check their state
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

        # display all buttons
        self.all_buttons.draw(common.screen)
                

    def play_grade_sound(self):
        # play different sounds for different grades
        match self.grade_level:
            case "great":
                self.great_grade_sfx.play()
            case "ok":
                self.ok_grade_sfx.play()
            case "bad":
                self.bad_grade_sfx.play()
            case _:  # default
                self.ok_grade_sfx.play()


    def update_tickbox(self):
        tickboxes = list(self.all_tickboxes)
        # checks results of most recenlty shown tickbox and displays result
        if self.results[tickboxes[self.row_counter].name]:
            tickboxes[self.row_counter].toggle_true()
            self.success_sfx.play()
        else:
            tickboxes[self.row_counter].toggle_false()
            self.fail_sfx.play()


    def update_display(self):
        num_of_result_rows = len(self.all_tickboxes)
        current_time_diff = pygame.time.get_ticks() - self.previous_time
        time_delay = 400

        # only update if enough time has past
        if current_time_diff >= time_delay:

            # if counter is less than number of results then add or update result
            if self.row_counter < num_of_result_rows or self.added_row:
                if self.added_row:
                    self.update_tickbox()
                    self.added_row = False
                    self.row_counter += 1
                else:
                    self.all_elements.add(list(self.all_result_text)[self.row_counter])
                    self.all_elements.add(list(self.all_tickboxes)[self.row_counter])
                    self.added_row = True
            else:
                # else display other elements
                self.all_elements.add(list(self.all_result_text)[self.row_counter])

                # plays sound when grade is displayed (2nd to last element in text group)
                if self.row_counter == len(self.all_result_text) - 2:
                    self.play_grade_sound()

                self.row_counter += 1

                # finish updating when all elements have been shown
                if self.row_counter >= len(self.all_result_text):
                    self.finished_updating = True

            self.previous_time = pygame.time.get_ticks()


    def reset_display(self):
        # if previously run delete the past results
        for element in self.all_grade_elements:
            element.kill()

        # reset varaibles
        self.finished_updating = False
        self.added_row = False
        self.row_counter = 0
        self.previous_time = 0

        # remove and reset elements
        for text in self.all_result_text:
            self.all_elements.remove(text)

        for tickbox in self.all_tickboxes:
            self.all_elements.remove(tickbox)

        for box in self.all_tickboxes:
            box.toggle_blank()


    def display_screen(self, results):
        self.reset_display()
        self.results = results
        self.calculate_results()
        self.transition.turn_on_arrive_transition()

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
            common.screen.fill(common.COLOUR_DARK_GRAY)

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


