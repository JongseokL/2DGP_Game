from pathlib import Path

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_i


class MineWeapon:
    def __init__(self):
        path = (Path(__file__).resolve().parent / 'assets' / 'images'
                / 'weapons' / 'mine_v1.png')
        self.image = load_image(str(path))
        self.mines = []
        self.key_down = False
        self.width = 23
        self.height = 23.5

    def handle_event(self, event, car):
        # Beta: one mine per press, ignoring keyboard auto-repeat.
        if event.type == SDL_KEYDOWN and event.key == SDLK_i:
            if not self.key_down:
                y = car.y - car.height / 2 - self.height / 2 - 4
                self.mines.append([car.x, y, 0.0])
                self.key_down = True
        elif event.type == SDL_KEYUP and event.key == SDLK_i:
            self.key_down = False

    def update(self, frame_time, road_distance):
        for mine in self.mines:
            mine[1] -= road_distance
            mine[2] += frame_time
        self.mines = [mine for mine in self.mines
                      if mine[1] + self.height / 2 > 0 and mine[2] < 12.0]

    def draw(self):
        for x, y, age in self.mines:
            self.image.clip_draw(128, 117, 985, 1008,
                                 x, y, self.width, self.height)
