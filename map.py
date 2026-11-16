from pathlib import Path

from pico2d import load_image


class Map:
    def __init__(self):
        image_path = (
            Path(__file__).resolve().parent
            / 'assets' / 'images' / 'maps'
            / 'road_two_way_8lane_ground_detail_v2.png'
        )
        self.image = load_image(str(image_path))

    def draw(self):
        self.image.draw(675, 540, 1350, 1080)
