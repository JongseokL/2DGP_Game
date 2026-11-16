from pathlib import Path
import random

from pico2d import load_image, get_canvas_width, get_canvas_height


# Filename, forward frame, oncoming frame.
CIVILIAN_FRAMES = [('civilian_car_01_bidirectional_sheet_v1.png', (108, 1104, 162, 329), (108, 379, 162, 330)), ('civilian_compact_black_bidirectional_v1.png', (94, 1107, 175, 302), (94, 391, 174, 301)), ('civilian_compact_blue_bidirectional_v1.png', (99, 1096, 179, 290), (100, 406, 179, 290)), ('civilian_compact_red_bidirectional_v1.png', (104, 1122, 157, 266), (102, 401, 159, 277)), ('civilian_compact_white_bidirectional_v1.png', (105, 1111, 169, 293), (105, 401, 169, 296)), ('civilian_compact_yellow_bidirectional_v1.png', (103, 1113, 166, 296), (102, 396, 167, 293)), ('civilian_sedan_black_bidirectional_v1.png', (107, 1102, 164, 334), (106, 376, 165, 334)), ('civilian_sedan_blue_bidirectional_v1.png', (108, 1103, 161, 331), (106, 378, 166, 330)), ('civilian_sedan_red_bidirectional_v1.png', (109, 1103, 161, 331), (106, 378, 165, 331)), ('civilian_sedan_white_bidirectional_v1.png', (106, 1104, 164, 332), (107, 377, 164, 332)), ('civilian_sedan_yellow_bidirectional_v1.png', (107, 1103, 161, 330), (107, 379, 162, 329)), ('civilian_suv_black_bidirectional_v1.png', (100, 1101, 171, 338), (94, 373, 178, 339)), ('civilian_suv_white_bidirectional_v1.png', (106, 1107, 157, 324), (105, 382, 163, 326)), ('civilian_truck_blue_bidirectional_v1.png', (106, 1098, 154, 329), (106, 379, 158, 328)), ('civilian_truck_red_bidirectional_v1.png', (107, 1106, 155, 318), (108, 388, 155, 316))]


class CivilianCar:
    def __init__(self, image, clip, lane, direction, y=0):
        self.image, self.clip = image, clip
        self.lane, self.direction = lane, direction
        centers = (856, 981, 1113, 1247) if direction == 1 else (201, 336, 468, 592)
        self.x = centers[lane] * get_canvas_width() / 1448
        self.y = y
        self.speed = 180.0 if direction == 1 else 210.0
        scale = min(62 / clip[2], 138 / clip[3])
        self.width, self.height = clip[2] * scale, clip[3] * scale

    def update(self, frame_time, road_distance):
        self.y += self.direction * self.speed * frame_time - road_distance

    def draw(self):
        self.image.clip_draw(*self.clip, self.x, self.y, self.width, self.height)


class CivilianTraffic:
    def __init__(self):
        root = Path(__file__).resolve().parent / 'assets' / 'images' / 'vehicles'
        self.assets = [(load_image(str(root / name)), forward, oncoming)
                       for name, forward, oncoming in CIVILIAN_FRAMES]
        self.cars = []
        self.spawn_timers = {-1: 0.0, 1: 0.0}

    def update(self, frame_time, road_distance):
        if frame_time <= 0:
            return
        height = get_canvas_height()
        for car in self.cars:
            car.update(frame_time, road_distance)
        self.cars = [car for car in self.cars
                     if car.y + car.height / 2 >= -2
                     and car.y - car.height / 2 <= height + 2]
        player_speed = road_distance / frame_time
        for direction in (-1, 1):
            self.spawn_timers[direction] -= frame_time
            if self.spawn_timers[direction] > 0:
                continue
            relative_speed = direction * (180 if direction == 1 else 210) - player_speed
            # Avoid accumulating off-screen cars at matching speeds.
            if abs(relative_speed) < 10:
                continue
            from_top = relative_speed < 0
            lanes = []
            for lane in range(4):
                same_lane = [c for c in self.cars
                             if c.direction == direction and c.lane == lane]
                if from_top:
                    free = all(c.y + c.height / 2 < height - 60 for c in same_lane)
                else:
                    free = all(c.y - c.height / 2 > 60 for c in same_lane)
                if free:
                    lanes.append(lane)
            if not lanes:
                self.spawn_timers[direction] = 0.1
                continue
            image, forward, oncoming = random.choice(self.assets)
            clip = forward if direction == 1 else oncoming
            car = CivilianCar(image, clip, random.choice(lanes), direction)
            car.y = height + car.height / 2 if from_top else -car.height / 2
            self.cars.append(car)
            self.spawn_timers[direction] = random.uniform(0.65, 1.25)

    def draw(self):
        for car in self.cars:
            car.draw()
