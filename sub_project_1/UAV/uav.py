import numpy as np
from sub_project_1.whether.whether import WeatherModel  # Make sure to adjust the import path as needed

class UAV:
    def __init__(self, max_speed=10, simulation_area_width=100, simulation_area_height=100):
        self.x = np.random.rand() * simulation_area_width
        self.y = np.random.rand() * simulation_area_height
        self.speed = np.random.rand() * max_speed
        self.direction = np.random.rand() * 2 * np.pi
        self.weather_model = WeatherModel()
        self.simulation_area_width = simulation_area_width
        self.simulation_area_height = simulation_area_height

    def move(self, time_step, other_uavs=None, other_aircraft=None):
        weather_effect = self.weather_model.get_weather_effect()
        weather_effect_on_speed, _ = weather_effect  # We only need the speed effect

        new_speed = self.speed + weather_effect_on_speed
        new_direction = self.direction

        # Calculate the new position based on speed and direction
        new_x = self.x + new_speed * np.cos(new_direction) * time_step
        new_y = self.y + new_speed * np.sin(new_direction) * time_step

        # Update the position
        self.x = new_x
        self.y = new_y

        self.check_boundary()

    def check_boundary(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.simulation_area_width:
            self.x = self.simulation_area_width

        if self.y < 0:
            self.y = 0
        elif self.y > self.simulation_area_height:
            self.y = self.simulation_area_height
