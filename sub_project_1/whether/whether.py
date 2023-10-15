import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


class WeatherModel:
    def __init__(self):
        self.weather_conditions = ['Вітер', 'Дощ', 'Сніг', 'Сонце']
        self.current_weather = None

    def update_weather(self):
        # Вибираємо випадкову погодну умову
        self.current_weather = np.random.choice(self.weather_conditions)

    def get_weather_effect(self):
        # Повертаємо вплив погоди на швидкість та видимість
        weather_effect = {
            'Вітер': (-0.2, -0.1),  # Increased speed impact for Вітер
            'Дощ': (-0.3, -0.2),  # Increased speed impact for Дощ
            'Сніг': (-0.4, -0.3),  # Highest speed impact for Сніг
            'Сонце': (0.1, 0.2)  # Lowest speed impact for Сонце
        }
        return weather_effect.get(self.current_weather, (0, 0))






