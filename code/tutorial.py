import pygame
import common
from element import AnimatedSprite, Button, Animation, Sprite


# page class to hold all contents relevant to each page
class Page():
    def __init__(self, contents, animation=None):
        self.contents = contents
        self.animation = animation
        self.has_animation = False if animation is None else True


class Tutorial(pygame.sprite.Sprite):
    def __init__(self, player_rect, goal_rect):
        super().__init__()
        self.active = True

        # page contents
        self.current_page = 0
        self.page_text = {}
        self.pages = []
        self.first_page_button_names = []
        self.last_page_button_names = []
        self.other_page_button_names =[]
        self.tutorial_buttons = pygame.sprite.Group()

        # create pages
        self.create_text()
        self.create_common_elements()
        self.create_page_one(player_rect)
        self.create_page_two(goal_rect)

        # create plain pages
        for num in range(3, 6):
            self.create_plain_text_page(num)

        # create animated pages
        self.create_animated_page("../animations/drive_forward", 6)
        self.create_animated_page("../animations/reverse", 7)
        self.create_animated_page("../animations/brake", 8)
        self.create_animated_page("../animations/turn_left", 9)
        self.create_animated_page("../animations/turn_right", 10)
        self.create_animated_page("../animations/indicate_left", 11)
        self.create_animated_page("../animations/indicate_right", 12)


    def create_text(self):
        # tutorial page text
        self.page_text[1] = "THIS IS YOU"
        self.page_text[2] = "THIS IS A DELICIOUS SWEET TREAT"
        self.page_text[3] = "YOUR GOAL IS SIMPLE.\nREACH THE SWEET TREAT"
        self.page_text[4] = "BUT THERE IS ONE CATCH..."
        self.page_text[5] = "YOU MUST OBEY THE ROAD RULES"

        self.page_text[6] = "HOLD W TO DRIVE FORWARD"
        self.page_text[7] = "HOLD S TO REVERSE"
        self.page_text[8] = "HOLD THE OPOSITE KEY OF THE CARS MOMENTUM TO BRAKE"
        self.page_text[9] = "HOLD A TO TURN LEFT"
        self.page_text[10] = "HOLD D TO TURN RIGHT"
        self.page_text[11] = "PRESS Q TO TOGGLE THE LEFT INDICATOR"
        self.page_text[12] = "PRESS E TO TOGGLE THE RIGHT INDICATOR"

    
    def create_common_elements(self):
        # create base surface the size of the screen
        self.base_surf = pygame.Surface((common.main_canvas_size.x, 
                                    common.main_canvas_size.y), 
                                    pygame.SRCALPHA)
        self.base_rect = self.base_surf.get_frect()

        # create arrow
        arrow_img = pygame.image.load("../graphics/arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(arrow_img, (common.main_canvas_size.x * 0.20,
                                                      common.main_canvas_size.y * 0.12))
        
        # text box
        self.text_box_surf = pygame.Surface((common.main_canvas_size.x * 0.60, 
                                        common.main_canvas_size.y * 0.60), pygame.SRCALPHA)
        self.text_box_surf.fill((0,0,0,0))
        self.text_box_rect = self.text_box_surf.get_frect(
            center = (common.main_canvas_size.x / 2, common.main_canvas_size.y / 2))
        
        # font
        self.font = pygame.font.Font("../fonts/boldpixels.boldpixels.ttf", 50)
        self.font.align = pygame.FONT_CENTER

        # buttons
        width_buffer = self.text_box_rect.width * 0.02
        height_buffer = self.text_box_rect.height * 0.02
        back_button = Button("BACK", 40, "BACK", 10, (50,5), 10, 10)
        back_button.rect.bottomleft = (self.text_box_rect.bottomleft[0] + width_buffer, 
                                       self.text_box_rect.bottomleft[1] - height_buffer)
        
        next_button = Button("NEXT", 40, "NEXT", 10, (50,5), 10, 10)
        next_button.rect.bottomright = (self.text_box_rect.bottomright[0] - width_buffer, 
                                        self.text_box_rect.bottomright[1] - height_buffer)
        
        play_button = Button("PLAY", 40, "PLAY", 10, (50,5), 10, 10)
        play_button.rect.bottomright = (self.text_box_rect.bottomright[0] - width_buffer, 
                                        self.text_box_rect.bottomright[1] - height_buffer)
        
        skip_button = Button("SKIP", 30, "SKIP", 10, (50,5), 5, 10)
        skip_button.rect.midbottom = (self.text_box_rect.midbottom[0], 
                                    self.text_box_rect.midbottom[1] - height_buffer)
        
        # add button to groups and lists
        self.tutorial_buttons.add(back_button, next_button, play_button, skip_button)
        self.first_page_button_names = ["NEXT", "SKIP"]
        self.last_page_button_names = ["BACK", "PLAY", "SKIP"]
        self.other_page_button_names = ["BACK", "NEXT", "SKIP"]


    def create_page_one(self, player_rect):
        # create player cutout
        player_cutout_surf = pygame.Surface((player_rect.width 
                                      + (common.main_canvas_size.x * 0.05), 
                                      player_rect.height 
                                      + (common.main_canvas_size.y * 0.05)))
        player_cutout_rect = player_cutout_surf.get_frect(center = player_rect.center)

        # add cutout to the base
        base = self.base_surf.copy()
        base.blit(player_cutout_surf, player_cutout_rect)

        # convert base to a mask and make cutouts transparent
        base_mask = pygame.mask.from_surface(base).to_surface(setcolor = (0,0,0,0), 
                                                                unsetcolor = common.COLOUR_DARK_MIST)

        # text box
        text_box = self.text_box_surf.copy()
        
        # font
        font_surf = self.font.render(self.page_text[1], False, common.COLOUR_DARK_OFF_WHITE)
        font_rect = font_surf.get_frect(center = (text_box.width / 2, text_box.height / 2))

        # create page
        text_box.blit(font_surf, font_rect)
        base_mask.blit(text_box, self.text_box_rect)
        content = Sprite(base_mask, self.base_rect)

        # create arrow
        arrow_rect = self.arrow.get_frect(midright = (player_rect.midleft[0] 
                                                        - common.main_canvas_size.x * 0.05,
                                                        player_rect.midleft[1]))
        
        # create arrow pointing to player
        arrow = AnimatedSprite(self.arrow, arrow_rect, 10, 
                                common.main_canvas_size.x * 0.025, 
                                common.main_canvas_size.x * 0.025, 0, 0, 20)
        
        # add page to list
        self.pages.append(Page(content, arrow))


    def create_page_two(self, goal_rect):
        # create goal cutout
        goal_cutout_surf = pygame.Surface((goal_rect.width 
                                        + (common.main_canvas_size.x * 0.05), 
                                        goal_rect.height 
                                        + (common.main_canvas_size.y * 0.05)))
        goal_cutout_rect = goal_cutout_surf.get_frect(center = goal_rect.center)

        # add cutout to the base
        base = self.base_surf.copy()
        base.blit(goal_cutout_surf, goal_cutout_rect)

        # convert base to a mask and make cutouts transparent
        base_mask = pygame.mask.from_surface(base).to_surface(setcolor = (0,0,0,0), 
                                                              unsetcolor = common.COLOUR_DARK_MIST)

        # text box
        text_box = self.text_box_surf.copy()
        
        # font
        font_surf = self.font.render(self.page_text[2], False, 
                                     common.COLOUR_DARK_OFF_WHITE, 
                                     wraplength=text_box.width)
        font_rect = font_surf.get_frect(center = (text_box.width / 2, text_box.height / 2))

        # add to base
        text_box.blit(font_surf, font_rect)
        base_mask.blit(text_box, self.text_box_rect)
        content = Sprite(base_mask, self.base_rect)

        # create arrow
        arrow_img = pygame.transform.rotate(self.arrow, 270)
        arrow_rect = arrow_img.get_frect(midbottom = (goal_rect.midtop[0],
                                                      goal_rect.midtop[1] 
                                                      - common.main_canvas_size.y * 0.05))
        
        # create arrow pointing to goal
        arrow = AnimatedSprite(arrow_img, arrow_rect, 10, 0, 0, 
                                common.main_canvas_size.y * 0.025,
                                common.main_canvas_size.y * 0.025, 20)
        
        # add page to list
        self.pages.append(Page(content, arrow))


    def create_plain_text_page(self, page_num):
        # create base
        base = self.base_surf.copy()
        base.fill((common.COLOUR_DARK_MIST))

        # text box
        text_box = self.text_box_surf.copy()
        
        # font
        font_surf = self.font.render(self.page_text[page_num], False, common.COLOUR_DARK_OFF_WHITE, 
                                     wraplength=text_box.width)
        font_rect = font_surf.get_frect(center = (text_box.width / 2, text_box.height / 2))

        # add to base
        text_box.blit(font_surf, font_rect)
        base.blit(text_box, self.text_box_rect)
        content = Sprite(base, self.base_rect)
        
        # add page to list
        self.pages.append(Page(content))


    def create_animated_page(self, file_path, page_num):
        # create base
        base = self.base_surf.copy()
        base.fill((common.COLOUR_DARK_MIST))

        # text box
        text_box = self.text_box_surf.copy()
        
        # font
        font_surf = self.font.render(self.page_text[page_num], False, 
                                     common.COLOUR_DARK_OFF_WHITE,
                                     wraplength = text_box.width)
        font_rect = font_surf.get_frect(center = (self.text_box_rect.width / 2,
                                        self.text_box_rect.height * 0.70))

        # animation
        animation = Animation(file_path, (self.text_box_rect.width * 0.50, 
                                          self.text_box_rect.width * 0.50))
        animation.rect.midtop = self.text_box_rect.midtop
    
        # add to base
        text_box.blit(font_surf, font_rect)
        base.blit(text_box, self.text_box_rect)
        content = Sprite(base, self.base_rect)
        
        # add page to list
        self.pages.append(Page(content, animation))


    def display_tutorial(self):
        # display current page
        page = self.pages[self.current_page]
        common.screen.blit(page.contents.image, page.contents.rect)
        if page.has_animation:
            common.screen.blit(page.animation.image, page.animation.rect)
            page.animation.update()

        # check if currently on first/last/other page
        first_page = bool(self.current_page == 0)
        last_page = bool(self.current_page == len(self.pages) - 1)
        other_page = not first_page and not last_page

        # add correct buttons
        for button in self.tutorial_buttons:
            if first_page and button.name in self.first_page_button_names:
                common.screen.blit(button.image, button.rect)
                button.is_active = True
            elif last_page and button.name in self.last_page_button_names:
                common.screen.blit(button.image, button.rect)
                button.is_active = True
            elif other_page and button.name in self.other_page_button_names:
                common.screen.blit(button.image, button.rect)
                button.is_active = True
            else:
                button.is_active = False


    def handle_tutorial_buttons(self):
        # check if buttons are hovered/clicked
        for button in self.tutorial_buttons:
            button.check_state()
            if button.clicked:
                button.clicked = False
                if button.name == "NEXT":
                    self.current_page += 1
                elif button.name == "BACK":
                    self.current_page -= 1
                elif button.name == "SKIP" or button.name == "PLAY":
                    self.active = False    # turn off tutorial

