from sub_project_1.UAV.uav_manager import UAVManager

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from sub_project_1.aircraft.aircraft import Aircraft
from sub_project_1.whether.whether import WeatherModel


class Simulation:
    def __init__(self):
        self.uav_manager = UAVManager()
        self.aircraft_manager = [Aircraft() for _ in range(5)]  # П'ять повітряних об'єктів
        self.max_time_steps = 100
        self.weather_model = WeatherModel()  # Ініціалізуйте об'єкт WeatherModel

    def run_simulation(self):
        # Зберігайте метрики
        average_speeds = []
        average_direction_deviation = []
        average_distance_deviation = []
        weather_impact_on_speed = []  # Метрика впливу погоди на швидкість
        uav_positions = []

        # Зберігайте метрики для кожної погодної умови
        weather_metrics = {condition: [] for condition in self.weather_model.weather_conditions}

        for _ in range(self.max_time_steps):
            self.uav_manager.move_uavs(other_aircraft=self.aircraft_manager)

            # Збережіть середню швидкість
            average_speed = np.mean([uav.speed for uav in self.uav_manager.uavs])
            average_speeds.append(average_speed)

            # Збережіть середнє відхилення напрямку
            deviation = np.std([uav.direction for uav in self.uav_manager.uavs])
            average_direction_deviation.append(deviation)

            # Обчисліть середнє відхилення від цільових координат
            distance_deviation = np.mean(
                [np.sqrt((uav.x - 50) ** 2 + (uav.y - 50) ** 2) for uav in self.uav_manager.uavs])
            average_distance_deviation.append(distance_deviation)

            # Збережіть позиції БПЛА
            uav_positions.append([(uav.x, uav.y) for uav in self.uav_manager.uavs])

        # Побудуйте графіки
        plt.figure(figsize=(18, 10))

        plt.subplot(2, 2, 1)
        plt.plot(range(self.max_time_steps), average_speeds, label='Середня швидкість')
        plt.xlabel('Час')
        plt.ylabel('Швидкість')
        plt.title('Динаміка середньої швидкості БПЛА')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(range(self.max_time_steps), average_direction_deviation, label='Середнє відхилення напрямку')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення напрямку руху БПЛА')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(range(self.max_time_steps), average_distance_deviation, label='Середнє відхилення від цілі')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення від цільових координат')
        plt.legend()

        plt.subplot(2, 2, 4)
        for i in range(len(uav_positions[0])):
            x_vals = [pos[i][0] for pos in uav_positions]
            y_vals = [pos[i][1] for pos in uav_positions]
            plt.plot(x_vals, y_vals, label=f'БПЛА {i + 1}')
        plt.xlabel('X-координата')
        plt.ylabel('Y-координата')
        plt.title('Траєкторії БПЛА')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def run_avoidance_scenario(self):
        # Збережіть метрики для сценарію уникнення перешкод
        avoidance_average_speeds = []
        avoidance_average_direction_deviation = []
        avoidance_average_distance_deviation = []
        avoidance_uav_positions = []

        for _ in range(self.max_time_steps):
            self.uav_manager.move_uavs(other_aircraft=self.aircraft_manager)

            # Збережіть середню швидкість
            average_speed = np.mean([uav.speed for uav in self.uav_manager.uavs])
            avoidance_average_speeds.append(average_speed)

            # Збережіть середнє відхилення напрямку
            deviation = np.std([uav.direction for uav in self.uav_manager.uavs])
            avoidance_average_direction_deviation.append(deviation)

            # Обчисліть середнє відхилення від цільових координат
            distance_deviation = np.mean(
                [np.sqrt((uav.x - 50) ** 2 + (uav.y - 50) ** 2) for uav in self.uav_manager.uavs])
            avoidance_average_distance_deviation.append(distance_deviation)

            # Збережіть позиції БПЛА
            avoidance_uav_positions.append([(uav.x, uav.y) for uav in self.uav_manager.uavs])

        # Побудуйте графіки для сценарію уникнення перешкод
        plt.figure(figsize=(18, 10))

        plt.subplot(2, 2, 1)
        plt.plot(range(self.max_time_steps), avoidance_average_speeds, label='Середня швидкість')
        plt.xlabel('Час')
        plt.ylabel('Швидкість')
        plt.title('Динаміка середньої швидкості БПЛА (Уникнення перешкод)')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(range(self.max_time_steps), avoidance_average_direction_deviation, label='Середнє відхилення напрямку')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення напрямку руху БПЛА (Уникнення перешкод)')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(range(self.max_time_steps), avoidance_average_distance_deviation, label='Середнє відхилення від цілі')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення від цільових координат (Уникнення перешкод)')
        plt.legend()

        plt.subplot(2, 2, 4)
        for i in range(len(avoidance_uav_positions[0])):
            x_vals = [pos[i][0] for pos in avoidance_uav_positions]
            y_vals = [pos[i][1] for pos in avoidance_uav_positions]
            plt.plot(x_vals, y_vals, label=f'БПЛА {i + 1}')
        plt.xlabel('X-координата')
        plt.ylabel('Y-координата')
        plt.title('Траєкторії БПЛА (Уникнення перешкод)')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def exponential_moving_average(data, alpha=0.1):
        ema = [data[0]]  # Початкове значення EMA
        for i in range(1, len(data)):
            ema_value = alpha * data[i] + (1 - alpha) * ema[-1]
            ema.append(ema_value)
        return ema

    def run_dynamic_targets_scenario(self):
        # Створіть об'єкти для сценарію зміни цілей в реальному часі
        dynamic_targets_aircraft = [Aircraft() for _ in range(2)]  # Два повітряних об'єкти для сценарію зміни цілей
        max_time_steps_dynamic_targets = 75  # Максимальна кількість кроків для сценарію зміни цілей

        # Зберігайте метрики для сценарію зміни цілей в реальному часі
        dynamic_targets_average_speeds = []
        dynamic_targets_average_direction_deviation = []
        dynamic_targets_average_distance_deviation = []
        dynamic_targets_uav_positions = []

        for _ in range(max_time_steps_dynamic_targets):
            self.uav_manager.move_uavs(other_aircraft=dynamic_targets_aircraft)

            # Збережіть середню швидкість
            average_speed = np.mean([uav.speed for uav in self.uav_manager.uavs])
            dynamic_targets_average_speeds.append(average_speed)

            # Збережіть середнє відхилення напрямку
            deviation = np.std([uav.direction for uav in self.uav_manager.uavs])
            dynamic_targets_average_direction_deviation.append(deviation)

            # Обчисліть середнє відхилення від цільових координат
            distance_deviation = np.mean([np.sqrt((uav.x - 30) ** 2 + (uav.y - 70) ** 2) for uav in self.uav_manager.uavs])
            dynamic_targets_average_distance_deviation.append(distance_deviation)

            # Збережіть позиції БПЛА
            dynamic_targets_uav_positions.append([(uav.x, uav.y) for uav in self.uav_manager.uavs])

        # Відображення метрик для сценарію зміни цілей в реальному часі
        plt.figure(figsize=(18, 10))

        plt.subplot(2, 2, 1)
        plt.plot(range(max_time_steps_dynamic_targets), dynamic_targets_average_speeds, label='Середня швидкість')
        plt.xlabel('Час')
        plt.ylabel('Швидкість')
        plt.title('Динаміка середньої швидкості БПЛА для сценарію зміни цілей')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(range(max_time_steps_dynamic_targets), dynamic_targets_average_direction_deviation, label='Середнє відхилення напрямку')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення напрямку руху БПЛА для сценарію зміни цілей')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(range(max_time_steps_dynamic_targets), dynamic_targets_average_distance_deviation, label='Середнє відхилення від цілі')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення від цільових координат для сценарію зміни цілей')
        plt.legend()

        plt.subplot(2, 2, 4)
        for i in range(len(dynamic_targets_uav_positions[0])):
            x_vals = [pos[i][0] for pos in dynamic_targets_uav_positions]
            y_vals = [pos[i][1] for pos in dynamic_targets_uav_positions]
            plt.plot(x_vals, y_vals, label=f'БПЛА {i + 1}')
        plt.xlabel('X-координата')
        plt.ylabel('Y-координата')
        plt.title('Траєкторії БПЛА для сценарію зміни цілей')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def run_interactive_visualization(self):
        # Create an empty figure
        fig = go.Figure()

        # Initialize traces for each UAV
        traces = [go.Scatter(x=[0], y=[0], mode='lines', name=f'UAV {i + 1}') for i in
                  range(len(self.uav_manager.uavs))]

        # Add the traces to the figure
        for trace in traces:
            fig.add_trace(trace)

        animation_settings = {
            'frame': {
                'duration': 100,  # Duration between frames in milliseconds
                'redraw': True
            },
            'fromcurrent': True,
        }

        # Define layout settings
        fig.update_layout(
            title='Анімація траєкторій БПЛА',
            xaxis=dict(title='X-координата'),
            yaxis=dict(title='Y-координата'),
            showlegend=True,
            updatemenus=[
                {
                    'buttons': [
                        {
                            'args': [
                                None,
                                {
                                    'frame': {
                                        'duration': 100,  # Duration between frames in milliseconds
                                        'redraw': True
                                    },
                                    'fromcurrent': True,
                                },
                            ],
                            'label': 'Програвати',
                            'method': 'animate',
                        },
                        {
                            'args': [
                                [None],
                                {
                                    'frame': {
                                        'duration': 0,  # Duration between frames in milliseconds
                                        'redraw': True
                                    },
                                    'mode': 'immediate',
                                },
                            ],
                            'label': 'Зупинити',
                            'method': 'animate',
                        },
                    ],
                    'direction': 'left',
                    'pad': {'r': 10, 't': 87},
                    'showactive': False,
                    'type': 'buttons',
                    'x': 0.1,
                    'xanchor': 'right',
                    'y': 0,
                    'yanchor': 'top',
                }
            ],

        )

        frames = []

        # Iterate through time steps
        for step in range(self.max_time_steps):
            uav_positions = []  # Збереження позицій БПЛА на даному кроці

            # Move UAVs and store their positions
            self.uav_manager.move_uavs(other_aircraft=self.aircraft_manager)
            for uav in self.uav_manager.uavs:
                uav_positions.append((uav.x, uav.y))

            # Update individual traces for each UAV
            for i, trace in enumerate(traces):
                trace.x = [pos[0] for pos in uav_positions[:i + 1]]
                trace.y = [pos[1] for pos in uav_positions[:i + 1]]

            # Create a frame for the current step
            frame = go.Frame(
                data=traces,
                name=f'Frame {step}'
            )

            frames.append(frame)

        # Add frames to the figure
        fig.frames = frames

        # Ваш наступний код для анімації

        # Відображення анімованого графіку
        fig.show()

    def run_simulation_with_weather(self):
        # Зберігайте метрики
        average_speeds = []
        average_direction_deviation = [0.0]  # Додайте початкове значення
        average_distance_deviation = []
        weather_impact_on_speed = []  # Метрика впливу погоди на швидкість
        uav_positions = []

        # Зберігайте метрики для кожної погодної умови
        weather_metrics = {condition: [] for condition in self.weather_model.weather_conditions}

        # Параметри для згладжування експоненційним методом
        alpha = 0.1  # Параметр згладжування
        ema_direction_deviation = average_direction_deviation[0]

        for _ in range(self.max_time_steps):
            # Оновіть погодні умови
            self.weather_model.update_weather()

            self.uav_manager.move_uavs()

            # Збережіть середню швидкість
            average_speed = np.mean([uav.speed for uav in self.uav_manager.uavs])
            average_speeds.append(average_speed)

            # Збережіть середнє відхилення напрямку
            deviation = np.std([uav.direction for uav in self.uav_manager.uavs])
            average_direction_deviation.append(deviation)

            # Обчисліть середнє відхилення від цільових координат
            distance_deviation = np.mean(
                [np.sqrt((uav.x - 50) ** 2 + (uav.y - 50) ** 2) for uav in self.uav_manager.uavs])
            average_distance_deviation.append(distance_deviation)

            # Збережіть вплив погодних умов на швидкість (сума впливів всіх БПЛА)
            weather_impact = sum([uav.weather_model.get_weather_effect()[1] for uav in self.uav_manager.uavs])
            weather_impact_on_speed.append(weather_impact)

            # Збережіть позиції БПЛА
            uav_positions.append([(uav.x, uav.y) for uav in self.uav_manager.uavs])

            # Збережіть метрики для кожної погодної умови
            for condition in self.weather_model.weather_conditions:
                weather_effect_on_speed, _ = self.weather_model.get_weather_effect()
                average_speed_condition = np.mean(
                    [uav.speed + weather_effect_on_speed for uav in self.uav_manager.uavs if
                     self.weather_model.current_weather == condition])
                weather_metrics[condition].append(average_speed_condition)

            # Згладжування експоненційним методом для відхилення напрямку
            ema_direction_deviation = alpha * deviation + (1 - alpha) * average_direction_deviation[-1]
            average_direction_deviation.append(ema_direction_deviation)

        # Виправлено помилку тут: змінено range(self.max_time_steps) на range(self.max_time_steps + 1)
        plt.subplots(3, 2, figsize=(18, 12))

        plt.subplot(3, 2, 1)
        plt.plot(range(self.max_time_steps), average_speeds, label='Середня швидкість')
        plt.xlabel('Час')
        plt.ylabel('Швидкість')
        plt.title('Динаміка середньої швидкості БПЛА')
        plt.legend()

        plt.subplot(3, 2, 2)
        # Змінено range(self.max_time_steps + 1) для x і y
        plt.plot(range(self.max_time_steps + 1), [ema_direction_deviation] * (self.max_time_steps + 1),
                 label='Згладжене відхилення напрямку')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка згладженого відхилення напрямку руху БПЛА')
        plt.legend()

        plt.subplot(3, 2, 3)
        plt.plot(range(self.max_time_steps), average_distance_deviation, label='Середнє відхилення від цілі')
        plt.xlabel('Час')
        plt.ylabel('Відхилення')
        plt.title('Динаміка середнього відхилення від цільових координат')
        plt.legend()

        plt.subplot(3, 2, 4)
        plt.plot(range(self.max_time_steps), weather_impact_on_speed, label='Вплив погоди на швидкість')
        plt.xlabel('Час')
        plt.ylabel('Вплив погоди')
        plt.title('Динаміка впливу погодних умов на швидкість БПЛА')
        plt.legend()

        plt.subplot(3, 2, 5)
        for condition in self.weather_model.weather_conditions:
            plt.plot(range(self.max_time_steps), weather_metrics[condition],
                     label=f'Середня швидкість при {condition}')
            plt.xlabel('Час')
            plt.ylabel('Швидкість')
            plt.title(f'Динаміка середньої швидкості БПЛА при погодній умові: {condition}')
            plt.legend()

        plt.tight_layout()
        plt.show()

    def exponential_moving_average(self, data, alpha):
        ema = [data[0]]  # Початкове значення EMA
        for value in data[1:]:
            ema.append(alpha * value + (1 - alpha) * ema[-1])
        return ema