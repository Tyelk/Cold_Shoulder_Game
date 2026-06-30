import pygame
import common
import os


# most basic sprite possible
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect



# sprite with shadow options
class Image(Sprite):
    def __init__(self, image, rect, name, layer, 
                 shadow_offset=(0,0), shadow_colour=(0,0,0,0), shadow_scale=(0,0)):
        super().__init__(image, rect)
        self.name = name
        self._layer = layer

        # if offset or scale given then create a shadow
        if shadow_offset != (0,0) or shadow_scale != (0,0):
            self.has_shadow = True
            self.shadow = Shadow(self.image, self.rect.center, shadow_offset, 
                                 shadow_colour, shadow_scale, layer)
        else:
            self.has_shadow = False
            self.shadow = None
            


# create shadow behind sprite
class Shadow(pygame.sprite.Sprite):
    def __init__(self, image, pos, offset, colour, scale, layer):
        super().__init__()
        self._layer = layer - 1 # should always be one below its element

        # scale image
        self.image = pygame.transform.scale(image, (image.get_width() + scale[0], 
                                                    image.get_height() + scale[1]))

        # create mask and set outline to transparent
        self.image = pygame.mask.from_surface(self.image).to_surface(setcolor = colour, unsetcolor = (0,0,0,0))
        self.rect = self.image.get_frect(center = (pos[0] + offset[0], pos[1] + offset[1]))



# custom button
class Button(pygame.sprite.Sprite):
    def __init__(self, text, font_size, name, layer, text_padding, button_depth, 
                 border_thickness, 
                 font_colour = common.COLOUR_WHITE, 
                 main_colour = common.COLOUR_LIGHT_BLACK, 
                 secondary_colour = common.COLOUR_DARK_GRAY, 
                 border_colour = common.COLOUR_BLACK, 
                 hover_font_colour = common.COLOUR_LIGHT_BLACK, 
                 hover_main_colour = common.COLOUR_DARK_OFF_WHITE, 
                 hover_secondary_colour = common.COLOUR_DARK_GRAY):
        super().__init__()
        self.script_dir = os.path.dirname(__file__)
        # general attributes
        self.text = text
        self.name = name
        self._layer = layer

        # sizing
        self.font_size = font_size
        self.text_padding = text_padding
        self.button_depth = button_depth
        self.current_depth = button_depth
        self.border_thickness = border_thickness

        # colours
        self.font_colour = font_colour
        self.main_colour = main_colour
        self.secondary_colour = secondary_colour
        self.hover_font_colour = hover_font_colour
        self.hover_main_colour = hover_main_colour
        self.hover_secondary_colour = hover_secondary_colour
        self.border_colour = border_colour
        # original colours
        self.original_font_colour = self.font_colour
        self.original_main_colour = self.main_colour
        self.original_secondary_colour = self.secondary_colour

        # hover/click bools
        self.is_active = True
        self.hovered = False
        self.click_down = False
        self.click_up = False
        self.clicked = False

        # create button
        self.create()

        # sounds
        click_down_sfx_path = os.path.join(self.script_dir, "../audio", "click_down.mp3")
        click_up_sfx_path = os.path.join(self.script_dir, "../audio", "click_up.mp3")
        hover_sfx_path = os.path.join(self.script_dir, "../audio", "hover.mp3")
        self.click_down_sfx = pygame.mixer.Sound(click_down_sfx_path)
        self.click_up_sfx = pygame.mixer.Sound(click_up_sfx_path)
        self.hover_sfx = pygame.mixer.Sound(hover_sfx_path)
        common.all_sound_effects.append(self.click_down_sfx)
        common.all_sound_effects.append(self.click_up_sfx)
        common.all_sound_effects.append(self.hover_sfx)
     

    def create(self):
        # font
        font_path = os.path.join(self.script_dir, "../fonts", "boldpixels.boldpixels.ttf")
        self.font = pygame.font.Font(font_path, self.font_size)
        self.font_surf = self.font.render(self.text, False, self.font_colour)
        self.font_rect = self.font_surf.get_frect()

        # main
        main_width = self.font_surf.get_width() + self.text_padding[0]
        main_height = self.font_surf.get_height() + self.text_padding[1]
        self.main_surf = pygame.Surface((main_width, main_height))
        self.main_rect = self.main_surf.get_frect()

        # secondary
        second_width = main_width
        second_height = main_height + self.current_depth
        self.secondary_surf = pygame.Surface((second_width, second_height))
        self.secondary_rect = self.secondary_surf.get_frect()

        # border
        border_width = second_width + (self.border_thickness) * 2
        border_height = main_height + self.border_thickness
        self.border_surf = pygame.Surface((border_width, border_height))
        self.border_rect = self.border_surf.get_frect()

        # button canvas
        button_width = border_width
        button_height = main_height + self.button_depth + self.border_thickness
        self.button_surf = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        self.button_rect = self.button_surf.get_frect()

        # colour
        self.main_surf.fill(self.main_colour)
        self.secondary_surf.fill(self.secondary_colour)
        self.border_surf.fill(self.border_colour)
        self.button_surf.fill((0,0,0,0))

        # relative positioning
        self.border_rect.midbottom = (button_width/2, button_height)
        self.secondary_rect.midbottom = (button_width/2, button_height - self.border_thickness)
        self.main_rect.midbottom = (button_width/2, 
                                    button_height - (self.current_depth + self.border_thickness))
        self.font_rect.center = (main_width/2, main_height/2)

        # draw surfaces
        self.draw_surfaces()

        # assigning values for sprite display
        self.image = self.button_surf
        self.rect = self.button_rect


    def draw_surfaces(self):
        # draw surfaces in correct order to create the buttons look
        self.main_surf.blit(self.font_surf, self.font_rect)
        self.button_surf.blit(self.border_surf, self.border_rect)
        self.button_surf.blit(self.secondary_surf, self.secondary_rect)
        self.button_surf.blit(self.main_surf, self.main_rect)


    def change_colour(self, f_colour, m_colour, s_colour):
        # change colours to stay consistent during clicks
        self.font_colour = f_colour
        self.main_colour = m_colour
        self.secondary_colour = s_colour

        # fill with new colours
        self.font_surf = self.font.render(self.text, False, self.font_colour)
        self.main_surf.fill(self.main_colour)
        self.secondary_surf.fill(self.secondary_colour)
        self.border_surf.fill(self.border_colour)

        # redrawing surfaces
        self.draw_surfaces()


    def hover(self):
        # change colours when hovered
        if not self.hovered:
            self.hovered = True

            # play audio
            self.hover_sfx.play()

            # change colour of button
            self.change_colour(self.hover_font_colour, self.hover_main_colour, 
                               self.hover_secondary_colour)


    def unhover(self):
        # revert colours when unhovered and click is released
        if self.hovered:
            self.hovered = False

            # change colours of button back to its original
            self.change_colour(self.original_font_colour, self.original_main_colour, 
                               self.original_secondary_colour)


    def check_hover(self):
        # if mouse is over button then it is hovering
        if self.rect.collidepoint(self.mouse_pos.x, self.mouse_pos.y):
            self.hover() # if over button (highlight button)
        else:
            self.unhover()  # if NOT over button


    def check_click(self):
        # left click while mouse is over the button
        if pygame.mouse.get_pressed()[0] and self.hovered and not self.click_down:
            self.click_down = True
            self.click_up = False

            # play audio
            self.click_down_sfx.play()

            # animate button press
            self.current_depth = self.button_depth * 0.5
            self.pos = self.rect.center
            self.create()
            self.rect.center = self.pos

        # release left click after clicking on button
        elif not pygame.mouse.get_pressed()[0] and self.click_down and not self.click_up:
            self.click_up = True
            self.click_down = False

            # play audio
            self.click_up_sfx.play()

            # animate button release
            self.current_depth = self.button_depth
            self.pos = self.rect.center
            self.create()
            self.rect.center = self.pos

            # set button as clicked
            self.clicked = True


    def calculate_mouse_pos(self):
        # calculate scal difference between screens
        scale_x = common.screen_size.x / common.main_canvas_size.x
        scale_y = common.screen_size.y / common.main_canvas_size.y

        # offset the mouse position by the screens position
        corrected_pos = (pygame.mouse.get_pos()[0] - common.screen_pos.x, 
                         pygame.mouse.get_pos()[1] - common.screen_pos.y)

        # scale the mouse position to the screens size
        self.mouse_pos = pygame.math.Vector2(corrected_pos[0] / scale_x, 
                                             corrected_pos[1] / scale_y)


    def check_state(self):
        # only change if active
        if self.is_active:
            self.calculate_mouse_pos()

            # only change button hover if left click is currently not pressed
            if not pygame.mouse.get_pressed()[0]:
                self.check_hover()

            # check for button click
            self.check_click()



# simple sprite that moves
class AnimatedSprite(Sprite):
    def __init__(self, image, rect, layer, 
                 right_distance, left_distance, down_distance, up_distance, speed):
        super().__init__(image, rect)
        self._layer = layer

        # sets point that bob animation is centered around
        self.original_location = self.rect.topleft

        # movement variables
        self.right_distance = right_distance
        self.left_distance = left_distance
        self.down_distance = down_distance
        self.up_distance = up_distance
        self.speed = speed
        
        # direction booleans (start animation moving in the largest direction)
        self.right = right_distance > left_distance
        self.down = down_distance > up_distance

        # check for any movement
        self.x_movement = bool(right_distance or left_distance)
        self.y_movement = bool(down_distance or up_distance)


    def animate_x(self):
        # check x location
        if self.original_location[0] - self.rect.x <= -self.right_distance:
            self.right = False
        if self.original_location[0] - self.rect.x >= self.left_distance:
            self.right = True

        # change x location
        if self.right:
            self.rect.x += self.speed * common.delta_time
        else:
            self.rect.x -= self.speed * common.delta_time

        
    def animate_y(self):
        # check y location
        if self.original_location[1] - self.rect.y <= -self.down_distance:
            self.down = False
        if self.original_location[1] - self.rect.y >= self.up_distance:
            self.down = True

        # change y location
        if self.down:
            self.rect.y += self.speed * common.delta_time
        else:
            self.rect.y -= self.speed * common.delta_time


    def update(self):
        # only animate if there is movement
        if self.x_movement:
            self.animate_x()
        if self.y_movement:
            self.animate_y()



# constantly looping animation
class Animation(pygame.sprite.Sprite):
    def __init__(self, path, scale):
        super().__init__()
        self.frames = []
        self.load_images(path, scale)
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_frect()
        self.frame_speed = 50
        self.last_frame_time = 0


    def load_images(self, path, scale):
        # for each image in the file create surface, scale, and then add to list of frames
        for frame in os.listdir(path):
            frame_path = os.path.join(path, frame)

            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(image, scale)
            self.frames.append(scaled_image)


    def update(self):
        # only get the new frame once enouch time has passed
        current_ticks = pygame.time.get_ticks()
        last_time = self.last_frame_time
        frame_speed = self.frame_speed

        if current_ticks - last_time >= frame_speed:

            # increment frame count
            self.current_frame += 1

            # if frame count exceeds the amount of frames reset the count
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

            # make the current image the frame
            self.image = self.frames[self.current_frame]

            # reset last frame time
            self.last_frame_time = pygame.time.get_ticks()



# clickable image button
class ImageButton(Image):
    def __init__(self, default_image, hover_image, rect, name, layer, click_depth,
                 shadow_offset=(0,0), shadow_colour=(0,0,0,0), shadow_scale=(0,0)):
        super().__init__(default_image, rect, name, layer, 
                         shadow_offset, shadow_colour, shadow_scale)
        self.script_dir = os.path.dirname(__file__)
        self.image = default_image
        self.default_image = default_image
        self.hover_image = hover_image
        self.rect = rect
        self.name = name
        self._layer = layer
        self.click_depth = click_depth

        # hover/click bools
        self.is_active = True
        self.hovered = False
        self.click_down = False
        self.click_up = False
        self.clicked = False

        # sounds
        click_down_sfx_path = os.path.join(self.script_dir, "../audio", "click_down.mp3")
        click_up_sfx_path = os.path.join(self.script_dir, "../audio", "click_up.mp3")
        hover_sfx_path = os.path.join(self.script_dir, "../audio", "hover.mp3")
        self.click_down_sfx = pygame.mixer.Sound(click_down_sfx_path)
        self.click_up_sfx = pygame.mixer.Sound(click_up_sfx_path)
        self.hover_sfx = pygame.mixer.Sound(hover_sfx_path)
        common.all_sound_effects.append(self.click_down_sfx)
        common.all_sound_effects.append(self.click_up_sfx)
        common.all_sound_effects.append(self.hover_sfx)


    def hover(self):
        if not self.hovered:
            self.hovered = True
            # change image
            self.image = self.hover_image

            # play audio
            self.hover_sfx.play()


    def unhover(self):
        if self.hovered:
            self.hovered = False
            # change image
            self.image = self.default_image


    def check_hover(self):
        # if mouse is over button then it is hovering
        if self.rect.collidepoint(self.mouse_pos.x, self.mouse_pos.y):
            self.hover() # if over button (highlight button)
        else:
            self.unhover()  # if NOT over button


    def check_click(self):
        # left click while mouse is over the button
        if pygame.mouse.get_pressed()[0] and self.hovered and not self.click_down:
            self.click_down = True
            self.click_up = False

            # play audio
            self.click_down_sfx.play()

            # animate button press
            self.original_pos = self.rect.center
            self.rect.center = (self.original_pos[0], self.original_pos[1] + self.click_depth)

        # release left click after clicking on button
        elif not pygame.mouse.get_pressed()[0] and self.click_down and not self.click_up:
            self.click_up = True
            self.click_down = False

            # play audio
            self.click_up_sfx.play()

            # animate button release
            self.rect.center = self.original_pos

            # set button as clicked
            self.clicked = True


    def calculate_mouse_pos(self):
        # calculate scal difference between screens
        scale_x = common.screen_size.x / common.main_canvas_size.x
        scale_y = common.screen_size.y / common.main_canvas_size.y

        # offset the mouse position by the screens position
        corrected_pos = (pygame.mouse.get_pos()[0] - common.screen_pos.x, 
                         pygame.mouse.get_pos()[1] - common.screen_pos.y)

        # scale the mouse position to the screens size
        self.mouse_pos = pygame.math.Vector2(corrected_pos[0] / scale_x, 
                                             corrected_pos[1] / scale_y)


    def check_state(self):
        # only change if active
        if self.is_active:
            self.calculate_mouse_pos()

            # only change button hover if left click is currently not pressed
            if not pygame.mouse.get_pressed()[0]:
                self.check_hover()

            # check for button click
            self.check_click()



# image that can be toggled
class ToggleImage(Image):
    def __init__(self, blank_image, true_image, false_image, rect, name, layer):
        super().__init__(blank_image, rect, name, layer)
        self.blank_image = blank_image
        self.true_image = true_image
        self.false_image = false_image

    def toggle_blank(self):
        self.image = self.blank_image

    def toggle_true(self):
        self.image = self.true_image

    def toggle_false(self):
        self.image = self.false_image



# msuic/sound effects volume sliders
class VolumeSlider(pygame.sprite.Sprite):
    def __init__(self, slider_length, pos, type):
        super().__init__()
        self.script_dir = os.path.dirname(__file__)
        # setup
        self.pos = pos
        self.type = type
        self.load_elements(slider_length)

        # booleans
        self.is_active = True
        self.hovered = False
        self.drag = False
        self.click_down = False
        self.click_up = False


    def load_elements(self, length):
        button_height_scale_multiplier = 3

        # load images from file
        default_img_path = os.path.join(self.script_dir, "../graphics", "slider_button_default.png")
        hover_img_path = os.path.join(self.script_dir, "../graphics", "slider_button_hover.png")
        line_img_path = os.path.join(self.script_dir, "../graphics", "slider_line.png")
        default_img = pygame.image.load(default_img_path).convert_alpha()
        hover_img = pygame.image.load(hover_img_path).convert_alpha()
        line_img = pygame.image.load(line_img_path).convert_alpha()

        # scale line to given length
        line_width_to_height_ratio = line_img.get_width() / line_img.get_height()
        scaled_line = pygame.transform.scale(line_img, 
                                               (length, length / line_width_to_height_ratio))
        
        # scale button to stay correct scale to line
        button_width_to_height_ratio = default_img.get_width() / default_img.get_height()
        button_height = scaled_line.get_height() * button_height_scale_multiplier
        button_width = button_height * button_width_to_height_ratio
        scaled_default = pygame.transform.scale(default_img, (button_width, button_height))
        scaled_hover = pygame.transform.scale(hover_img, (button_width, button_height))

        # save different button looks
        self.default = scaled_default
        self.highlighted = scaled_hover

        # save elements surfs and rects
        self.line_image = scaled_line
        self.line_rect = self.line_image.get_frect(center = self.pos)
        self.button_image = self.default
        button_pos = (self.line_rect.right - (self.button_image.get_width() / 2), self.pos[1])
        self.button_rect = self.button_image.get_frect(center = button_pos)


    def hover(self):
        if not self.hovered:
            self.hovered = True
            # change image
            self.button_image = self.highlighted


    def unhover(self):
        if self.hovered:
            self.hovered = False
            # change image
            self.button_image = self.default


    def check_hover(self):
        # if mouse is over button then it is hovering
        if self.button_rect.collidepoint(self.mouse_pos.x, self.mouse_pos.y):
            self.hover() # if over button (highlight button)
        else:
            self.unhover()  # if NOT over button


    def check_click(self):
        # left click while mouse is over the button
        if pygame.mouse.get_pressed()[0] and self.hovered and not self.click_down:
            self.click_down = True
            self.click_up = False
            self.drag = True

        # release left click after clicking on button
        elif not pygame.mouse.get_pressed()[0] and self.click_down and not self.click_up:
            self.click_up = True
            self.click_down = False
            self.drag = False


    def calculate_mouse_pos(self):
        # calculate scale difference between screens
        scale_x = common.screen_size.x / common.main_canvas_size.x
        scale_y = common.screen_size.y / common.main_canvas_size.y

        # offset the mouse position by the screens position
        corrected_pos = (pygame.mouse.get_pos()[0] - common.screen_pos.x, 
                         pygame.mouse.get_pos()[1] - common.screen_pos.y)

        # scale the mouse position to the screens size
        self.mouse_pos = pygame.math.Vector2(corrected_pos[0] / scale_x, 
                                             corrected_pos[1] / scale_y)


    def calculate_value(self):
        # calculates the position of the button on the line as a percentage
        line_size = self.line_rect.width - self.button_rect.width
        button_pos = (self.button_rect.center[0] - self.line_rect.left) - (self.button_rect.width / 2)
        percentage = (button_pos / line_size)

        # call function depending on type the slider is assigned to
        if self.type == "MUSIC":
            common.change_music_volume(percentage)
        elif self.type == "EFFECTS":
            common.change_effects_volume(percentage)


    def set_button_level(self):
        # set button position to reflect volume level
        line_size = self.line_rect.width - self.button_rect.width

        # set level depending on what type the slider is assigned to
        if self.type == "MUSIC":
            button_pos = line_size * common.music_volume
        elif self.type == "EFFECTS":
            button_pos = line_size * common.effects_volume
        
        # sets position
        button_pos += self.line_rect.left + (self.button_rect.width / 2)
        self.button_rect.center = (button_pos, self.line_rect.center[1])


    def update_pos(self):
        # limits prevent button from leaving the slider
        left_limit = self.line_rect.left + (self.button_rect.width / 2)
        right_limit = self.line_rect.right - (self.button_rect.width / 2)

        # if button within length of slider then move it to the mouses position
        # if the mouse is past a limit move the button to that limit
        if self.mouse_pos.x >= left_limit and self.mouse_pos.x <= right_limit:
            x_pos = self.mouse_pos.x
        elif self.mouse_pos.x < left_limit:
            x_pos = left_limit
        elif self.mouse_pos.x > right_limit:
            x_pos = right_limit

        # set button pos
        new_pos = (x_pos, self.pos[1])
        self.button_rect.center = new_pos
        self.calculate_value()


    def check_state(self):
        # only change if active
        if self.is_active:
            self.calculate_mouse_pos()

            # only change button hover if left click is currently not pressed
            if not pygame.mouse.get_pressed()[0]:
                self.check_hover()

            # check for button click
            self.check_click()

            # move button if being dragged
            if self.drag:
                self.update_pos()


    def display(self):
        # displays slider components on screen
        common.screen.blit(self.line_image, self.line_rect)
        common.screen.blit(self.button_image, self.button_rect)



# togglable button
class ToggleTutorialButton(pygame.sprite.Sprite):
    def __init__(self, pos, size, click_depth):
        super().__init__()
        self.script_dir = os.path.dirname(__file__)
        self.click_depth = click_depth
        self.original_pos = pos
        self.load_images(pos, size)
        self.update_image()

        # hover/click bools
        self.hovered = False
        self.click_down = False
        self.click_up = False

        # sounds
        click_down_sfx_path = os.path.join(self.script_dir , "../audio", "click_down.mp3")
        click_up_sfx_path = os.path.join(self.script_dir , "../audio", "click_up.mp3")
        hover_sfx_path = os.path.join(self.script_dir , "../audio", "hover.mp3")
        self.click_down_sfx = pygame.mixer.Sound(click_down_sfx_path)
        self.click_up_sfx = pygame.mixer.Sound(click_up_sfx_path)
        self.hover_sfx = pygame.mixer.Sound(hover_sfx_path)
        common.all_sound_effects.append(self.click_down_sfx)
        common.all_sound_effects.append(self.click_up_sfx)
        common.all_sound_effects.append(self.hover_sfx)

    
    def load_images(self, pos, size):
        # load images
        active_image_path = os.path.join(self.script_dir, "../graphics", "success_tickbox.png")
        inactive_image_path = os.path.join(self.script_dir, "../graphics", "failure_tickbox.png")
        active_img = pygame.image.load(active_image_path).convert_alpha()
        active_img_scaled = pygame.transform.scale(active_img, size)
        inactive_img = pygame.image.load(inactive_image_path).convert_alpha()
        inactive_img_scaled = pygame.transform.scale(inactive_img, size)
        self.rect = active_img_scaled.get_frect(center = pos)

        # set image states
        self.active_image = active_img_scaled
        self.inactive_image = inactive_img_scaled


    def update_image(self):
        # sets image depending if tutorial is active
        if common.tutorial_active :
            self.image = self.active_image
        else:
            self.image = self.inactive_image


    def hover(self):
        if not self.hovered:
            self.hovered = True
            # play audio
            self.hover_sfx.play()
            # animate hover
            self.rect.center = (self.original_pos[0], 
                                self.original_pos[1] + (self.click_depth / 2))


    def unhover(self):
        if self.hovered:
            # restore to defualt
            self.hovered = False
            self.rect.center = self.original_pos


    def check_hover(self):
        # if mouse is over button then it is hovering
        if self.rect.collidepoint(self.mouse_pos.x, self.mouse_pos.y):
            self.hover() # if over button (highlight button)
        else:
            self.unhover()  # if NOT over button


    def check_click(self):
        # left click while mouse is over the button
        if pygame.mouse.get_pressed()[0] and self.hovered and not self.click_down:
            self.click_down = True
            self.click_up = False

            # play audio
            self.click_down_sfx.play()

            # animate button press
            self.rect.center = (self.original_pos[0], self.original_pos[1] + self.click_depth)

        # release left click after clicking on button
        elif not pygame.mouse.get_pressed()[0] and self.click_down and not self.click_up:
            self.click_up = True
            self.click_down = False

            # play audio
            self.click_up_sfx.play()

            # animate button release
            self.rect.center = self.original_pos

            # change tutorial status
            common.tutorial_active = not common.tutorial_active
            self.update_image()


    def calculate_mouse_pos(self):
        # calculate scal difference between screens
        scale_x = common.screen_size.x / common.main_canvas_size.x
        scale_y = common.screen_size.y / common.main_canvas_size.y

        # offset the mouse position by the screens position
        corrected_pos = (pygame.mouse.get_pos()[0] - common.screen_pos.x, 
                         pygame.mouse.get_pos()[1] - common.screen_pos.y)

        # scale the mouse position to the screens size
        self.mouse_pos = pygame.math.Vector2(corrected_pos[0] / scale_x, 
                                             corrected_pos[1] / scale_y)


    def check_state(self):
        self.calculate_mouse_pos()

        # only change button hover if left click is currently not pressed
        if not pygame.mouse.get_pressed()[0]:
            self.check_hover()

        # check for button click
        self.check_click()

