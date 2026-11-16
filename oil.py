from pathlib import Path

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_o


class OilWeapon:
    def __init__(self):
        path = (Path(__file__).resolve().parent / 'assets' / 'images'
                / 'weapons' / 'oil_slick_v1.png')
        self.image = load_image(str(path))
        self.slicks = []
        self.key_down = False
        self.width = 46
        self.height = 100

    def handle_event(self, event, car):
        # Beta: one free deployment per key press, without key-repeat firing.
        if event.type == SDL_KEYDOWN and event.key == SDLK_o:
            if not self.key_down:
                self.slicks.append([car.x, car.y - car.height / 2, 0.0])
                self.key_down = True
        elif event.type == SDL_KEYUP and event.key == SDLK_o:
            self.key_down = False

    def update(self, frame_time, road_distance):
        for slick in self.slicks:
            slick[1] -= road_distance
            slick[2] += frame_time
        # Remove off-screen or expired oil, including while the player is stopped.
        self.slicks = [s for s in self.slicks
                       if s[1] + self.height / 2 > 0 and s[2] < 12.0]

    def draw(self):
        for x, y, age in self.slicks:
            self.image.clip_draw(369, 92, 499, 1061,
                                 x, y, self.width, self.height)
