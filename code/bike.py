import pygame
import common
import math
import os

class Bike(pygame.sprite.Sprite):
    def __init__(self, scale, layer):
        super().__init__()
        self._layer = layer

        # frames
        self.cycle_frames = []
        self.indicate_frames = []
        self.load_bike(scale)

        # attributes
        self.speed = 50
        self.rotate_speed = 2
        self.start_location = pygame.math.Vector2((common.main_canvas_size.x * 0.90, common.main_canvas_size.y * 0.58))
        self.reset()

        # waypoints
        self.way_points = []
        self.indicate_points = []
        self.map_path()


    def load_frames(self, path, scale, frames_list):
        # for each frame scale and add it to the list
        for frame in os.listdir(path):
            frame_path = os.path.join(path, frame)
            image = pygame.image.load(frame_path).convert_alpha()
            scaled_image = pygame.transform.scale(image, scale)
            frames_list.append(scaled_image)


    def load_bike(self, scale):
        # load animations
        bike_cycle_path = "../animations/bike_cycle"
        bike_indicate_path = "../animations/bike_indicate_left"
        self.load_frames(bike_cycle_path, scale, self.cycle_frames)
        self.load_frames(bike_indicate_path, scale, self.indicate_frames)


    def position_bike(self):
        # rotate image and center on new position
        self.image = pygame.transform.rotate(self.current_image, self.rotate_angle)
        self.rect = self.image.get_frect(center = self.current_location)


    def add_waypoint(self, new_waypoint):
        # add new waypoints and prevent new redundant waypoints from being added

        # if list is empty add new waypoint
        if len(self.way_points) < 1:
            self.way_points.append(new_waypoint)
        else:
            # if there are waypoints get the latest waypoint in the list
            latest_wp = pygame.math.Vector2(self.way_points[-1])
            new_waypoint = pygame.math.Vector2(new_waypoint)

            # if the distance between the waypoints is greater than 2 then add the waypoint
            distance = latest_wp.distance_to(new_waypoint)
            if distance > 2:
                self.way_points.append(new_waypoint)


    def create_transition_waypoints(self, start, end, control_point_a, control_point_b):
        # creates waypoints following a beizer curve to have a smooth transition
        # between entering and exiting the roundabout

        # creates 9 points along the curve
        num_of_points = 9
        for num in range(num_of_points + 1):
            point = num / num_of_points

            # create x and y coordinates
            x = (1 - point)**3 * start[0] + 3 * (1 - point)**2 * point * control_point_a[0] + 3 * (1 - point) * point**2 * control_point_b[0] + point**3 * end[0]
            y = (1 - point)**3 * start[1] + 3 * (1 - point)**2 * point * control_point_a[1] + 3 * (1 - point) * point**2 * control_point_b[1] + point**3 * end[1]

            # add waypoint
            self.add_waypoint((x, y))


    def create_turn_waypoints(self):
        # creates turn around roundabout
        start_point = pygame.math.Vector2(common.main_canvas_size.x * 0.5, 
                                    common.main_canvas_size.y * 0.6)
        center_point = pygame.math.Vector2(common.main_canvas_size.x * 0.5, 
                                    common.main_canvas_size.y * 0.5)

        # creates 9 evenly spaced waypoints around the roundabout in a 90 degree turn
        degrees = 90
        num_of_points = 10
        translated_point = start_point - center_point
        degree_change = degrees / num_of_points
        for n in range(num_of_points):
            # rotate vector and create new waypoint
            rotated_translated = translated_point.rotate(degree_change * (n + 1))
            new_point = rotated_translated + center_point

            # add waypoint
            self.add_waypoint(new_point)


    def map_path(self):
        # entry curve
        entry = (common.main_canvas_size.x * 0.66, common.main_canvas_size.y * 0.58)
        end = (common.main_canvas_size.x * 0.5, common.main_canvas_size.y * 0.6)
        entry_control_point = (common.main_canvas_size.x * 0.6, common.main_canvas_size.y * 0.58)
        end_control_point = (common.main_canvas_size.x * 0.55, common.main_canvas_size.y * 0.6)
        self.create_transition_waypoints(entry, end, entry_control_point, end_control_point)

        # roundabout curve
        self.create_turn_waypoints()

        # exit curve
        start = (common.main_canvas_size.x * 0.4, common.main_canvas_size.y * 0.5)
        exit = (common.main_canvas_size.x * 0.42, common.main_canvas_size.y * 0.34)
        start_control_point = (common.main_canvas_size.x * 0.4, common.main_canvas_size.y * 0.45)
        exit_control_point = (common.main_canvas_size.x * 0.42, common.main_canvas_size.y * 0.40)
        self.create_transition_waypoints(start, exit, start_control_point, exit_control_point)

        # final waypoint
        self.way_points.append((common.main_canvas_size.x * 0.42, common.main_canvas_size.y * -0.10))

        # indicate waypoints
        right_indicate_pos = (common.main_canvas_size .x* 0.70, common.main_canvas_size.y * 0.55)
        left_indicate_pos = (common.main_canvas_size.x * 0.4, common.main_canvas_size.y * 0.5)
        end_indicate_pos = (common.main_canvas_size.x * 0.45, common.main_canvas_size.y * 0.30)
        indicate_right = (right_indicate_pos, "R") # indicate right
        indicate_left = (left_indicate_pos, "L") # indicate left
        indicate_end = (end_indicate_pos, "N") # indicate nothing/neutral 
        self.indicate_points = [indicate_right, indicate_left, indicate_end]


    def rotate(self):
        # calculates the angle between the next waypoint and the previous waypoint
        if self.way_point_index < 1: # first angle
            ahead_wp = pygame.math.Vector2(self.way_points[self.way_point_index])
            behind_wp = self.start_location
        elif self.way_point_index + 1 < len(self.way_points): # between angles
            ahead_wp = pygame.math.Vector2(self.way_points[self.way_point_index + 1])
            behind_wp = pygame.math.Vector2(self.way_points[self.way_point_index])
        else:   # last angle
            ahead_wp = pygame.math.Vector2(self.way_points[self.way_point_index])
            behind_wp = pygame.math.Vector2(self.way_points[self.way_point_index - 1])

        # gets the angle of the next waypoints 
        angle = math.atan2(-(ahead_wp.y-behind_wp.y), ahead_wp.x-behind_wp.x)
        degrees = math.degrees(angle)
        
        # finds the difference between the current angle and the new angle 
        new_angle = (degrees - 90) % 360    #(offset by 90 to appear sideways)
        angle_diff = new_angle - self.rotate_angle

        # if the difference is to great or ot low invert the angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360

        # rotate bike by a portion of the angle difference (depending on the delta time)
        self.rotate_angle = (self.rotate_angle + (angle_diff * self.rotate_speed * common.delta_time)) % 360


    def move(self):
        if self.way_point_index < len(self.way_points):
            # get the current waypoint, save the distance, and move to the new point
            current_wp = pygame.math.Vector2(self.way_points[self.way_point_index])
            distance = current_wp.distance_to(self.current_location)
            self.current_location.move_towards_ip(current_wp, self.speed * common.delta_time)

            # rotate the image
            self.rotate()

            # if within 1 unit then change to next waypoint
            if distance < 1:
                self.way_point_index += 1


    def update_indicate(self):
        # compares indicate states and checks index is not out of bounds
        same_indicate_states = self.new_indicate == self.current_indicate
        counter_below_max = self.indicate_frame_counter < len(self.indicate_frames) - 1

        # if the states are different and counter at 0 set current state to new
        # if the states are different and counter is not 0 decrease the counter
        # if the current state is NOT N and counter is below max increase counter
        if not same_indicate_states and self.indicate_frame_counter == 0:
            self.current_indicate = self.new_indicate
        elif not same_indicate_states and self.indicate_frame_counter > 0:
            self.indicate_frame_counter -= 1
        elif self.current_indicate != "N" and counter_below_max:
            self.indicate_frame_counter += 1


    def animate(self):
        frame_delay = 200

        # only change frame if enough time has passed
        if pygame.time.get_ticks() - self.last_frame_time >= frame_delay:

            # increment counter and reset if to large
            self.cycle_frame_counter += 1
            if self.cycle_frame_counter >= len(self.cycle_frames):
                self.cycle_frame_counter = 0

            # update indicate counter
            self.update_indicate()

            # get latest cycle frame and overlay new arm frame
            cycle_frame = self.cycle_frames[self.cycle_frame_counter].copy()
            arm_frame = self.indicate_frames[self.indicate_frame_counter].copy()
            if self.current_indicate == "R":    # flip arms if indicating to the right
                arm_frame = pygame.transform.flip(arm_frame, True, False)
            cycle_frame.blit(arm_frame, (0,0))

            # update new image nad save new time
            self.current_image = cycle_frame
            self.last_frame_time = pygame.time.get_ticks()
        

    def check_indicate_points(self):
        # get current indicate waypoint and the distance between it and the bike
        current_point = self.indicate_points[self.indicate_point_index]
        wp_pos = pygame.math.Vector2(current_point[0])
        distance = self.current_location.distance_to(wp_pos)

        # if the bike is within 50 units of the current waypoint set new indicate
        if distance <= 50:
            self.new_indicate = current_point[1]
            # increment point if less than list max
            if self.indicate_point_index + 1 < len(self.indicate_points):
                self.indicate_point_index += 1


    def update_bike(self):
        self.check_indicate_points()
        self.move()
        self.animate()
        self.position_bike()


    def reset(self):
        # frames
        self.last_frame_time = 0
        self.cycle_frame_counter = 0
        self.indicate_frame_counter = 0
        self.current_indicate = "N"
        self.new_indicate = "N"

        # attributes
        self.rotate_angle = 90
        self.current_location = self.start_location.copy()
        self.current_image = self.cycle_frames[0]
        self.way_point_index = 0
        self.indicate_point_index = 0

        self.position_bike()

