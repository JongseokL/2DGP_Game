from pathlib import Path
import random

from pico2d import load_image, get_canvas_width, get_canvas_height


# Third row, first column: straight oncoming pose.
CIVILIAN_FRAMES = [('civilian_car_01_bidirectional_sheet_v1.png', (108, 379, 162, 330)), ('civilian_compact_black_bidirectional_v1.png', (94, 391, 174, 301)), ('civilian_compact_blue_bidirectional_v1.png', (100, 406, 179, 290)), ('civilian_compact_red_bidirectional_v1.png', (102, 401, 159, 277)), ('civilian_compact_white_bidirectional_v1.png', (105, 401, 169, 296)), ('civilian_compact_yellow_bidirectional_v1.png', (102, 396, 167, 293)), ('civilian_sedan_black_bidirectional_v1.png', (106, 376, 165, 334)), ('civilian_sedan_blue_bidirectional_v1.png', (106, 378, 166, 330)), ('civilian_sedan_red_bidirectional_v1.png', (106, 378, 165, 331)), ('civilian_sedan_white_bidirectional_v1.png', (107, 377, 164, 332)), ('civilian_sedan_yellow_bidirectional_v1.png', (107, 379, 162, 329)), ('civilian_suv_black_bidirectional_v1.png', (94, 373, 178, 339)), ('civilian_suv_white_bidirectional_v1.png', (105, 382, 163, 326)), ('civilian_truck_blue_bidirectional_v1.png', (106, 379, 158, 328)), ('civilian_truck_red_bidirectional_v1.png', (108, 388, 155, 316))]


class CivilianCar:
    def __init__(self, image, clip, lane, y):
        self.image = image
        self.clip = clip
        self.lane = lane
        self.x = (201, 336, 468, 592)[lane] * get_canvas_width() / 1448
        self.y = y
        scale = min(62 / clip[2], 138 / clip[3])
        self.width = clip[2] * scale
        self.height = clip[3] * scale

    def update(self, frame_time, road_distance):
        self.y -= 210 * frame_time + road_distance

    def draw(self):
        self.image.clip_draw(*self.clip, self.x, self.y, self.width, self.height)


class CivilianTraffic:
    def __init__(self):
        root = Path(__file__).resolve().parent / 'assets' / 'images' / 'vehicles'
        self.assets = [(load_image(str(root / name)), clip)
                       for name, clip in CIVILIAN_FRAMES]
        self.cars = []
        self.spawn_timer = 0.0

    def update(self, frame_time, road_distance):
        for car in self.cars:
            car.update(frame_time, road_distance)
        self.cars = [car for car in self.cars if car.y + car.height / 2 > 0]
        self.spawn_timer -= frame_time
        if self.spawn_timer <= 0:
            # Spawn spacing only; no gameplay collision detection or response.
            lanes = [lane for lane in range(4)
                     if all(car.lane != lane or
                            car.y + car.height / 2 < get_canvas_height() - 50
                            for car in self.cars)]
            if lanes:
                image, clip = random.choice(self.assets)
                car = CivilianCar(image, clip, random.choice(lanes), 0)
                car.y = get_canvas_height() + car.height / 2
                self.cars.append(car)
                self.spawn_timer = random.uniform(0.65, 1.25)
            else:
                self.spawn_timer = 0.1

    def draw(self):
        for car in self.cars:
            car.draw()
