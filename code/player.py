import os
import pygame
import math
import common

class Player(pygame.sprite.Sprite):
    def __init__(self, start_location, player_scale, layer):
        super().__init__()
        self.script_dir = os.path.dirname(__file__)
        self.start_location = start_location.copy()
        self._layer = layer

        # load images
        self.image_dict = {}
        self.load_images(player_scale)

        # audio 
        indicator_on_sfx_path = os.path.join(self.script_dir, "../audio", "indicator_on.mp3")
        indicator_off_sfx_path = os.path.join(self.script_dir, "../audio", "indicator_off.mp3")
        reverse_sfx_path = os.path.join(self.script_dir, "../audio", "reverse.mp3")
        self.indicator_on_sfx = pygame.mixer.Sound(indicator_on_sfx_path)
        self.indicator_off_sfx = pygame.mixer.Sound(indicator_off_sfx_path)
        self.reverse_sfx = pygame.mixer.Sound(reverse_sfx_path)
        common.all_sound_effects.append(self.indicator_on_sfx)
        common.all_sound_effects.append(self.indicator_off_sfx)
        common.all_sound_effects.append(self.reverse_sfx)

        # set start
        self.reset()
      

    def load_images(self, player_scale):
        # images are saved to the dictionary depending on booleans used to determine
        # scenarios they will be used for
        # BOOLEAN (left indication, right indication, braking, reversing)
        default_path = os.path.join(self.script_dir, "../graphics", "car.png")
        default = pygame.image.load(default_path).convert_alpha()
        self.image_dict[(False, False, False, False)] = pygame.transform.scale(default, player_scale)
        left_path = os.path.join(self.script_dir, "../graphics", "car_ind_left.png")
        left = pygame.image.load(left_path).convert_alpha()
        self.image_dict[(True, False, False, False)] = pygame.transform.scale(left, player_scale)
        right_path = os.path.join(self.script_dir, "../graphics", "car_ind_right.png")
        right = pygame.image.load(right_path).convert_alpha()
        self.image_dict[(False, True, False, False)] = pygame.transform.scale(right, player_scale)
        brake_path = os.path.join(self.script_dir, "../graphics", "car_brake.png")
        brake = pygame.image.load(brake_path).convert_alpha()
        self.image_dict[(False, False, True, False)] = pygame.transform.scale(brake, player_scale)
        brake_left_path = os.path.join(self.script_dir, "../graphics", "car_brake_ind_left.png")
        brake_left = pygame.image.load(brake_left_path).convert_alpha()
        self.image_dict[(True, False, True, False)] = pygame.transform.scale(brake_left, player_scale)
        brake_right_path = os.path.join(self.script_dir, "../graphics", "car_brake_ind_right.png")
        brake_right = pygame.image.load(brake_right_path).convert_alpha()
        self.image_dict[(False, True, True, False)] = pygame.transform.scale(brake_right, player_scale)
        
        reverse_path = os.path.join(self.script_dir, "../graphics", "car_reverse.png")
        reverse = pygame.image.load(reverse_path).convert_alpha()
        self.image_dict[(False, False, False, True)] = pygame.transform.scale(reverse, player_scale)
        reverse_brake_path = os.path.join(self.script_dir, "../graphics", "car_reverse_brake.png")
        reverse_brake = pygame.image.load(reverse_brake_path).convert_alpha()
        self.image_dict[(False, False, True, True)] = pygame.transform.scale(reverse_brake, player_scale)
        rev_brake_left_path = os.path.join(self.script_dir, "../graphics", "car_reverse_brake_ind_left.png")
        rev_brake_left = pygame.image.load(rev_brake_left_path).convert_alpha()
        self.image_dict[(True, False, True, True)] = pygame.transform.scale(rev_brake_left, player_scale)
        rev_brake_right_path = os.path.join(self.script_dir, "../graphics", "car_reverse_brake_ind_right.png")
        rev_brake_right = pygame.image.load(rev_brake_right_path).convert_alpha()
        self.image_dict[(False, True, True, True)] = pygame.transform.scale(rev_brake_right, player_scale)
        rev_left_path = os.path.join(self.script_dir, "../graphics", "car_reverse_ind_left.png")
        rev_left = pygame.image.load(rev_left_path).convert_alpha()
        self.image_dict[(True, False, False, True)] = pygame.transform.scale(rev_left, player_scale)
        rev_right_path = os.path.join(self.script_dir, "../graphics", "car_reverse_ind_right.png")
        rev_right = pygame.image.load(rev_right_path).convert_alpha()
        self.image_dict[(False, True, False, True)] = pygame.transform.scale(rev_right, player_scale)
    

    def reset(self):
        # set starting image
        self.current_image = self.image_dict[(False, False, False, False)]
        self.image = self.current_image
        self.rect = self.image.get_frect(center = self.start_location)

        # movement variables
        self.car_location = self.start_location.copy()
        self.car_acceleration = 50
        self.car_speed = 0
        self.rotate_angle = 0
        self.turn_radius = 1.5

        # inidcator variables
        self.reversing = False
        self.left_indicator = False
        self.right_indicator = False
        self.indicator_toggle_time = 0
        self.indicator_on = False
        self.indicator_active_time = 0

        self.reversed = False


    def input_check(self):
        # player input
        self.input()

        # move car
        self.move()

        # check location
        self.boundary_check()


    def input(self):
        # gets player input
        keys = pygame.key.get_pressed()

        # Car speed
        forward_pedal = int(keys[pygame.K_w])
        back_pedal = int(keys[pygame.K_s])
        self.momentum_calculation(forward_pedal, back_pedal)

        # rotation of player car
        turn_direction = int(keys[pygame.K_a]) - int(keys[pygame.K_d])
        self.rotation_calculation(turn_direction)

        # indicators
        indicators = int(keys[pygame.K_q]) - int(keys[pygame.K_e])
        self.toggle_indicators(indicators)

        # player car lights
        self.update_car_lights(forward_pedal, back_pedal)
        

    def momentum_calculation(self, forward_pedal, back_pedal):
        # rounded to 2 decimals to keep movement consistent
        self.car_speed = round(self.car_speed, 2)

        velocity = self.car_acceleration * common.delta_time

        # if the pedal of the opposite direction of the players movement is pressed then
        # the speed is reduced by a greater amount
        if back_pedal and self.car_speed > 1:
            self.car_speed -= velocity * 4
        elif forward_pedal and self.car_speed < -1:
            self.car_speed += velocity * 3
        elif forward_pedal:
            self.car_speed += velocity
        elif back_pedal:
            self.car_speed -= velocity * 0.5
        elif self.car_speed > 1:  # slowly reduce speed if no pedal is pressed
            self.car_speed -= velocity * 0.1
        elif self.car_speed < -1:
            self.car_speed += velocity * 0.5
        else:   # set speed to zero if slow enough to remove any slight movements
            self.car_speed = 0

        # calculate the location of the player car depending on their turn angle and speed
        self.car_location.x += self.car_speed * math.cos(math.radians(self.rotate_angle + 90)) * common.delta_time
        self.car_location.y -= self.car_speed * math.sin(math.radians(self.rotate_angle + 90)) * common.delta_time


    def rotation_calculation(self, turn_direction):
        # rotation is determined by the direction, acceleration, turn radius, and the delta time
        # if the vehicle is not moving it cannot turn
        self.rotate_angle += turn_direction * (self.car_speed / 2) * common.delta_time * self.turn_radius

        # resets angle to prevent scaling infinitely (in either direction)
        self.rotate_angle = self.rotate_angle % 360


    def toggle_indicators(self, indicators):
        no_toggle_value = 0

        # if no indicator change then return
        if indicators == no_toggle_value:
            return
        
        # can toggle only if after toggle delay (prevent spamming indicator)
        toggle_delay = 400
        if pygame.time.get_ticks() - self.indicator_toggle_time >= toggle_delay:

            # toggles indicator on/off and turns off opposite indicator
            if indicators > no_toggle_value:
                self.left_indicator = not self.left_indicator
                self.right_indicator = False
            else:
                self.right_indicator = not self.right_indicator
                self.left_indicator = False

            # sets new toggle time
            self.indicator_toggle_time = pygame.time.get_ticks()
            

    def update_car_lights(self, forward_pedal, back_pedal):
        indicator_flicker_delay = 500   # indicator flicker delay time

        # reversing if noticeable negative acceleration
        reversing_speed = -10
        self.reversing = bool(self.car_speed < reversing_speed)
        if self.reversing:
            self.reverse_sfx.play()
            self.reversed = True

        # braking if pressing button in opposite direction of acceleration
        braking = bool((not self.reversing and back_pedal) or (self.reversing and forward_pedal))
        
        # boolean to hold if the inidcators can flicker or not
        toggle_flicker = pygame.time.get_ticks() - self.indicator_active_time >= indicator_flicker_delay

        # if either indicator is on and can be flickered
        if (self.left_indicator or self.right_indicator) and toggle_flicker:
            # toggle indicator
            self.indicator_on = not self.indicator_on

            # only changes indicator (visually) when flickered
            self.right_ind_active = self.right_indicator
            self.left_ind_active = self.left_indicator

            # indicator audio
            if self.indicator_on:
                self.indicator_on_sfx.play()
            else:
                self.indicator_off_sfx.play()

            # sets new time
            self.indicator_active_time = pygame.time.get_ticks()

        elif not self.left_indicator and not self.right_indicator:
            # if neither indicator is on then turn them off without waiting for the delay
            self.right_ind_active = False
            self.left_ind_active = False
            self.indicator_on = False
            
        # the player image is determined by the combination of left/right indicating, braking
        # and reversing
        # the combination is used to get the appropriate image from the dictionary
        left_ind = self.left_ind_active and self.indicator_on
        right_ind = self.right_ind_active and self.indicator_on
        self.current_image = self.image_dict[(left_ind, right_ind, braking, self.reversing)]


    def move(self):
        # set car center to new locaiton
        self.rect.center = (self.car_location.x, self.car_location.y)

        # set player sprite rotation and location
        self.image = pygame.transform.rotate(self.current_image, self.rotate_angle)
        self.rect = self.image.get_frect(center = self.rect.center)


    def boundary_check(self):
        # Screen boundaries prevent car leaving play area
        if self.rect.top < 0:
            self.rect.top = 0
            self.car_speed = 0
            self.car_location.y += 1

        if self.rect.bottom > common.main_canvas_size.y:
            self.rect.bottom = common.main_canvas_size.y
            self.car_speed = 0
            self.car_location.y -= 1

        if self.rect.left < 0:
            self.rect.left = 0
            self.car_speed = 0
            self.car_location.x += 1

        if self.rect.right > common.main_canvas_size.x:
            self.rect.right = common.main_canvas_size.x
            self.car_speed = 0
            self.car_location.x -= 1