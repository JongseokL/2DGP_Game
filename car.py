from pathlib import Path

from pico2d import (load_image, get_canvas_width, get_canvas_height,
                    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT,
                    SDLK_UP, SDLK_DOWN)


class Car:
    def __init__(self):
        image_path = (Path(__file__).resolve().parent / 'assets' / 'images'
                      / 'player' / 'player_basic_car.png')
        self.image = load_image(str(image_path))
        self.x = 1163 * 1100 / 1350
        self.y = 130 * 880 / 1080
        self.width = 80 * 1100 / 1350
        self.height = 180 * 880 / 1080
        self.pressed_keys = set()
        self.speed = 0.0
        self.travel_distance = 0.0
        self.max_speed = 320.0
        self.acceleration = 240.0
        self.braking = 640.0
        self.coasting = 100.0
        self.steer_speed = 260.0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP:
            self.pressed_keys.discard(event.key)

    def update(self, frame_time):
        # Speeds are pixels per second; braking has priority over acceleration.
        if SDLK_DOWN in self.pressed_keys:
            acceleration = -self.braking
        elif SDLK_UP in self.pressed_keys:
            acceleration = self.acceleration
        else:
            acceleration = -self.coasting
        previous_speed = self.speed
        self.speed = max(0.0, min(self.max_speed,
                                self.speed + acceleration * frame_time))
        self.travel_distance = (previous_speed + self.speed) * 0.5 * frame_time
        direction = (int(SDLK_RIGHT in self.pressed_keys)
                     - int(SDLK_LEFT in self.pressed_keys))
        self.x += direction * self.steer_speed * frame_time

        # Keep the full sprite inside the canvas, including its transparent margin.
        half_width, half_height = self.width / 2, self.height / 2
        self.x = max(half_width, min(get_canvas_width() - half_width, self.x))
        self.y = max(half_height, min(get_canvas_height() - half_height, self.y))

    def draw(self):
        self.image.clip_draw(95, 667, 253, 552,
                             self.x, self.y, self.width, self.height)
