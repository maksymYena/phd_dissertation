import matplotlib.pyplot as plt
import pandas as pd
import pygame
from scipy.signal import find_peaks

from sub_project_2.configs.config import RED, YELLOW, WHITE, BLUE, screen, metrics_df
from sub_project_2.drones.Drone import Drone
from sub_project_2.drowning_person.drowning_person import DrowningPerson


# Клас симуляції
class Simulation:
    def __init__(self):
        self.optical_drone = Drone(100, 100, RED, engine_power=200, max_battery=200)
        self.ftp_drone = Drone(200, 200, YELLOW, engine_power=200, max_battery=200)
        self.drowning_person = DrowningPerson()
        self.time_steps = []
        self.optical_drone_observation = []
        self.emergency_detected = []
        self.optical_drone_battery = []
        self.ftp_drone_battery = []
        self.distance_between_drones = []
        self.optical_drone_speed = []
        self.ftp_drone_speed = []
        self.rescue_time = []
        self.drop_accuracy = []

    def run(self, simulation_duration):
        global metrics_df  # Declare metrics_df as a global variable to access it in the run method.
        running = True
        clock = pygame.time.Clock()

        for step in range(simulation_duration):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.optical_drone.calculate_speed()
            self.optical_drone.move()

            self.ftp_drone.move()

            if self.optical_drone.battery_level <= 0 or self.ftp_drone.battery_level <= 0:
                running = False

            self.optical_drone.process_optical_data()

            distance = ((self.optical_drone.x - self.ftp_drone.x) ** 2 + (self.optical_drone.y - self.ftp_drone.y) ** 2) ** 0.5
            self.distance_between_drones.append(distance)

            self.optical_drone_speed.append(self.optical_drone.max_speed)
            self.ftp_drone_speed.append(self.ftp_drone.max_speed)

            self.optical_drone.perform_emergency_rescue(step)  # Pass 'step' as an argument.
            self.ftp_drone.exchange_information(self.optical_drone)
            self.optical_drone.exchange_information(self.ftp_drone)

            if self.optical_drone.detect_emergency() and not self.optical_drone.has_control_system:
                if self.ftp_drone.select_optimal_route(self.optical_drone):
                    self.optical_drone.haul_control_system()
                    # Розрахунок точності визначення координат збросу
                    self.drop_accuracy.append(distance)
                else:
                    self.drop_accuracy.append(None)
                    self.optical_drone.release_control_system()
            else:
                self.drop_accuracy.append(None)

            new_row = {
                'Time Step': step,
                'Optical Drone Observation': self.optical_drone.observation,
                'Emergency Detected': int(self.optical_drone.detect_emergency()),
                'Optical Drone Battery': self.optical_drone.battery_level,
                'FTP Drone Battery': self.ftp_drone.battery_level,
                'Distance Between Drones': distance,
                'Optical Drone Speed': self.optical_drone.max_speed,
                'FTP Drone Speed': self.ftp_drone.max_speed,
                'Rescue Time': self.optical_drone.rescue_time,
                'Drop Accuracy': self.drop_accuracy[-1]
            }

            metrics_df = pd.concat([metrics_df, pd.DataFrame([new_row])], ignore_index=True)

            screen.fill(WHITE)

            self.optical_drone.draw(screen)
            self.ftp_drone.draw(screen)

            pygame.draw.circle(screen, BLUE, (int(self.drowning_person.x), int(self.drowning_person.y)), 10)

            pygame.display.flip()

            clock.tick(60)

            self.time_steps.append(step)
            self.optical_drone_observation.append(self.optical_drone.observation)
            self.emergency_detected.append(self.optical_drone.detect_emergency())
            self.optical_drone_battery.append(self.optical_drone.battery_level)
            self.ftp_drone_battery.append(self.ftp_drone.battery_level)

            if self.optical_drone.rescue_time is not None:
                self.rescue_time.append(self.optical_drone.rescue_time)
            else:
                self.rescue_time.append(None)

        pygame.quit()

    # Метод для відобразження графіків
    def display_metrics(self):
        plt.figure(figsize=(12, 10))

        plt.subplot(3, 2, 1)
        plt.plot(self.time_steps, self.optical_drone_observation, label='Спостереження оптичного дрону')
        plt.xlabel('Час')
        plt.ylabel('Кількість спостережень')
        plt.legend()

        plt.subplot(3, 2, 2)
        plt.plot(self.time_steps, self.emergency_detected, label='Виявлення аварії')
        plt.xlabel('Час')
        plt.ylabel('Аварія (1 - так, 0 - ні)')
        plt.legend()

        plt.subplot(3, 2, 3)
        plt.plot(self.time_steps, self.optical_drone_battery, label='Заряд оптичного дрону')
        plt.plot(self.time_steps, self.ftp_drone_battery, label='Заряд FTP дрону')
        plt.xlabel('Час')
        plt.ylabel('Заряд')
        plt.legend()

        plt.subplot(3, 2, 4)
        plt.plot(self.time_steps, self.distance_between_drones, label ='Відстань між дронами')  # Fix here, add ':' after 'label'
        plt.xlabel('Час')
        plt.ylabel('Відстань')
        plt.legend()

        plt.subplot(3, 2, 5)
        plt.plot(self.time_steps, self.optical_drone_speed, label='Швидкість оптичного дрону')
        plt.plot(self.time_steps, self.ftp_drone_speed, label='Швидкість FTP дрону')
        plt.xlabel('Час')
        plt.ylabel('Швидкість')
        plt.legend()

        plt.subplot(3, 2, 6)
        plt.plot(self.time_steps, self.rescue_time, label='Час на рятувальну операцію')
        plt.xlabel('Час')
        plt.ylabel('Час (кроки)')
        plt.legend()

        # Фільтруємо дані, залишаючи тільки числові значення (не None)
        filtered_drop_accuracy = [x for x in self.drop_accuracy if x is not None]

        # Графік для точності визначення координат збросу на основі фільтрованих даних
        plt.figure(figsize=(12, 6))
        plt.plot(self.time_steps[:len(filtered_drop_accuracy)], filtered_drop_accuracy, label='Точність визначення координат збросу')
        plt.xlabel('Час')
        plt.ylabel('Відстань між дронами (точність)')
        plt.legend()

        # Фільтруємо дані, залишаючи тільки числові значення (не None)
        filtered_drop_accuracy = [x if x is not None else float('inf') for x in self.drop_accuracy]

        # Графік для точності визначення координат збросу на основі фільтрованих даних
        plt.figure(figsize=(12, 6))
        plt.plot(self.time_steps[:len(filtered_drop_accuracy)], filtered_drop_accuracy, label='Точність визначення координат збросу')
        plt.xlabel('Час')
        plt.ylabel('Відстань між дронами (точність)')
        plt.legend()

        # Знаходження піків та мінімумів у фільтрованих даних
        peak_indices, _ = find_peaks(filtered_drop_accuracy, height=50)
        min_indices, _ = find_peaks([-x for x in filtered_drop_accuracy], height=50)

        peak_values = [filtered_drop_accuracy[i] for i in peak_indices]
        min_values = [filtered_drop_accuracy[i] for i in min_indices]

        # Додаємо анотації тексту для піків та мінімумів
        for value, index in zip(peak_values, peak_indices):
            plt.annotate(f'Пік: {value:.2f}', xy=(self.time_steps[index], value), xytext=(self.time_steps[index] + 10, value + 10),
                         arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=12, color='red')

        for value, index in zip(min_values, min_indices):
            plt.annotate(f'Мінімум: {value:.2f}', xy=(self.time_steps[index], value), xytext=(self.time_steps[index] + 10, value + 10),
                         arrowprops=dict(facecolor='blue', arrowstyle='->'), fontsize=12, color='blue')

        # Додаємо підписи для піков та мінімумів
        for value, index in zip(peak_values, peak_indices):
            plt.text(self.time_steps[index] + 10, value + 30, f'Пік: {value:.2f}', fontsize=12, color='red')

        for value, index in zip(min_values, min_indices):
            plt.text(self.time_steps[index] + 10, value - 50, f'Мінімум: {value:.2f}', fontsize=12, color='blue')

        plt.tight_layout()
        plt.show()

        # Збереження DataFrame у файл CSV для подальшого аналізу
        metrics_df.to_csv('simulation_metrics.csv', index=False)

# ... (other code)

# Define and execute your main function or run the Simulation class here.
