# config.py
import pygame
import pandas as pd

# Ініціалізація Pygame
pygame.init()

# Константи для розмірів вікна
WIDTH, HEIGHT = 800, 600

# Колір
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Створення вікна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Моделювання руху та взаємодії дронів")

# Створення пустого DataFrame для збереження метрик
metrics_df = pd.DataFrame(columns=[
    'Time Step',
    'Optical Drone Observation',
    'Emergency Detected',
    'Optical Drone Battery',
    'FTP Drone Battery',
    'Distance Between Drones',
    'Optical Drone Speed',
    'FTP Drone Speed',
    'Rescue Time',
    'Drop Accuracy'
])
