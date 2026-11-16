from pathlib import Path

from pico2d import load_image


class Car:
    def __init__(self):
        image_path = (
            Path(__file__).resolve().parent
            / 'assets' / 'images' / 'player'
            / 'player_basic_car.png'
        )
        self.image = load_image(str(image_path))

        # 기본 도로의 가장 오른쪽 차선 중앙, 화면 하단에서 시작한다.
        self.x = 1163 * 1100 / 1350
        self.y = 130 * 880 / 1080
        self.width = 80 * 1100 / 1350
        self.height = 180 * 880 / 1080

    def draw(self):
        # 시트 좌측 상단의 직진 프레임을 사용한다. 원본 크기: 1254 x 1254.
        self.image.clip_draw(95, 667, 253, 552,
                             self.x, self.y, self.width, self.height)
