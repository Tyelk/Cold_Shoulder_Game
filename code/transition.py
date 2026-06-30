import pygame
import common
from element import Image, Sprite, Shadow

class Transition():
    def __init__(self):
        # transition variables
        self.surfaces = []
        self.section_count = 10
        self.section_width = (common.main_canvas_size.x / self.section_count)
        self.current_count = 0
        self.last_section_time = 0
        self.section_delay = 1000 / self.section_count

        self.sections = []
        self.create_transition()

        # transition booleans
        self.active_transition = False
        self.leave_transition = False
        self.arrive_transition= False
        self.audio_playing = False

        # sounds
        self.leave_sfx = pygame.mixer.Sound("../audio/transition_leave.mp3")
        self.arrive_sfx = pygame.mixer.Sound("../audio/transition_arrive.mp3")
        common.all_sound_effects.append(self.leave_sfx)
        common.all_sound_effects.append(self.arrive_sfx)


    def create_transition(self):
        # create surface 
        load_img_path = "../graphics/load_screen.png"
        load_img_size = common.main_canvas_size

        load_img = pygame.image.load(load_img_path).convert_alpha()
        load_img_scaled = pygame.transform.scale(load_img, load_img_size)

        # loading text
        font_path = "../fonts/boldpixels.boldpixels.ttf"
        font_size = 70
        font_text = "LOADING"
        font_antialias = False
        font_colour = common.COLOUR_DARK_OFF_WHITE
        font_pos = common.main_canvas_size / 2

        font = pygame.font.Font(font_path, font_size)
        font_surf = font.render(font_text, font_antialias, font_colour)
        font_rect = font_surf.get_frect(center = font_pos)
        load_img_scaled.blit(font_surf, font_rect)

        # create default screen
        rect = load_img_scaled.get_frect()
        self.default = Sprite(load_img_scaled, rect)

        # create each section and add to list
        for num in range(self.section_count):
            section_rect = pygame.Rect(num * self.section_width, 0, 
                                    self.section_width, common.main_canvas_size.y)
            
            sect = load_img_scaled.subsurface(section_rect)
            sect_rect = sect.get_frect(topleft = (num * self.section_width, 0))
            section = Image(sect, sect_rect, "sect", 6)

            self.sections.append(section)

    
    def display_default(self):
        # default loading screen (static image)
        common.screen.blit(self.default.image, self.default.rect)

    
    def turn_on_arrive_transition(self):
        self.active_transition = True
        self.arrive_transition = True

    
    def turn_on_leave_transition(self):
        self.active_transition = True
        self.leave_transition = True


    def calculate_delay(self):
        # calcualte delay
        current_ticks = pygame.time.get_ticks()
        past_ticks = self.last_section_time
        delay = self.section_delay

        # only pass if delay has been long enough
        if current_ticks - past_ticks >= delay:
            # save tick and increment count
            self.last_section_time = pygame.time.get_ticks()
            self.current_count += 1


    def display_leave_transition(self):
        # hides screen slowly

        if not self.audio_playing:
            self.leave_sfx.play()
            self.audio_playing = True

        # display section
        for num in range(self.current_count + 1):
            sect = self.sections[num]
            common.screen.blit(sect.image, sect.rect)

        self.calculate_delay()

        # once all sections have been shown reset the variables
        if self.current_count >= self.section_count:
            self.last_section_time = 0
            self.current_count = 0
            self.leave_transition = False
            self.active_transition = False
            self.audio_playing = False
    

    def display_arrive_transition(self):
        # show screen slowly

        if not self.audio_playing:
            self.arrive_sfx.play()
            self.audio_playing = True

        # remove sections
        for num in range(len(self.sections) - 1,  self.current_count - 1, -1):
            sect = self.sections[num]
            common.screen.blit(sect.image, sect.rect)

        self.calculate_delay()

        # once all sections have been hidden reset the variables
        if self.current_count >= self.section_count - 1:
            self.last_section_time = 0
            self.current_count = 0
            self.arrive_transition = False
            self.active_transition = False
            self.audio_playing = False


    def display_transition(self):
        # shows transtion if either are turned on
        if self.leave_transition:
            self.display_leave_transition()
        elif self.arrive_transition:
            self.display_arrive_transition()

