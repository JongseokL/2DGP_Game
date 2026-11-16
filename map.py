from pathlib import Path

from pico2d import load_image, get_canvas_width, get_canvas_height


class Map:
    def __init__(self):
        image_path = (Path(__file__).resolve().parent / 'assets' / 'images'
                      / 'maps' / 'road_two_way_8lane_ground_detail_v2.png')
        self.image = load_image(str(image_path))
        self.scroll = 0.0

    def update(self, distance):
        self.scroll = (self.scroll + distance) % get_canvas_height()

    def draw(self):
        width, height = get_canvas_width(), get_canvas_height()
        # Adjacent copies cover the canvas throughout every scroll cycle.
        bottom = -self.scroll
        self.image.draw(width / 2, bottom + height / 2, width, height)
        self.image.draw(width / 2, bottom + height * 1.5, width, height)
