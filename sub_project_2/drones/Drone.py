from random import uniform, choice

import pygame

from sub_project_2.configs.config import WIDTH, HEIGHT


class Drone:
    def __init__(self, x, y, color, engine_power, max_battery):
        self.x = x
        self.y = y
        self.color = color
        self.observation = 0
        self.max_speed = 5
        self.battery_capacity = max_battery
        self.battery_level = self.battery_capacity
        self.has_control_system = False
        self.is_hauling = False
        self.rescue_time = None
        self.engine_power = engine_power
        self.weight = 10  # Вага дрона
        self.carrying_capacity = 5  # Максимальна вага, яку дрон може перевозити
        self.payload_weight = 0  # Вага перевезеного вантажу

    def select_optimal_route(self, other_drone):
        if self.battery_level >= 50:
            print(f"Дрон {self} вибирає оптимальний маршрут для доставки до дрона {other_drone}.")
            return True
        else:
            print(f"Дрон {self} не має достатньо заряду для доставки до дрона {other_drone}.")
            return False

    def calculate_speed(self):
        # Розрахунок швидкості на основі ваги та ваги перевезеного вантажу
        total_weight = self.weight + self.payload_weight
        self.max_speed = self.engine_power / total_weight

    def load_payload(self, weight):
        if self.payload_weight + weight <= self.carrying_capacity:
            self.payload_weight += weight
        else:
            print(f"Дрон {self} не може перевезти більше вантажу, максимальна вага вантажу досягнута.")

    def unload_payload(self):
        self.payload_weight = 0

    def haul_control_system(self):
        if self.has_control_system:
            self.is_hauling = True
            self.has_control_system = False

    def release_control_system(self):
        self.is_hauling = False

    def move(self):
        dx = uniform(-self.max_speed, self.max_speed)
        dy = uniform(-self.max_speed, self.max_speed)
        self.x += dx
        self.y += dy
        self.battery_level -= abs(dx) + abs(dy)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)

    def detect_emergency(self):
        return choice([True, False])

    def process_optical_data(self):
        self.observation += 1

    def receive_control_system(self):
        self.has_control_system = True

    def perform_emergency_rescue(self, step):
        if self.detect_emergency():
            print("Аварія виявлена! Дрон вирушає на місце аварії.")
            # Симуляція точної локації збросу
            rescue_x = uniform(0, WIDTH)
            rescue_y = uniform(0, HEIGHT)
            self.rescue_time = step
            self.x = rescue_x
            self.y = rescue_y

    def exchange_information(self, other_drone):
        if self.battery_level >= 20 and other_drone.battery_level >= 20:
            print(f"Дрон {self} відправляє дані дрону {other_drone}.")
            print(f"Дрон {self} отримує дані від дрону {other_drone}.")
