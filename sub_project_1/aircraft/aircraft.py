import numpy as np


class Aircraft:
    def __init__(self, max_speed=10):
        self.x = np.random.rand() * 100
        self.y = np.random.rand() * 100
        self.speed = np.random.rand() * max_speed
        self.direction = np.random.rand() * 2 * np.pi

    def move(self, time_step=0.1):
        # Обчисліть нові координати на основі швидкості та напрямку
        self.x += self.speed * np.cos(self.direction) * time_step
        self.y += self.speed * np.sin(self.direction) * time_step
        self.x = np.clip(self.x, 0, 100)
        self.y = np.clip(self.y, 0, 100)
