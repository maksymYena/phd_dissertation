from sub_project_1.Simulations.simulation import Simulation
from whether.whether import WeatherModel

if __name__ == "__main__":
    weather_model = WeatherModel()  # Створюємо модель погоди
    simulation = Simulation()
    simulation.run_simulation()

    # Запустити сценарій уникнення перешкод
    simulation.run_avoidance_scenario()

    # Запустити сценарій зміни цілей в реальному часі
    simulation.run_dynamic_targets_scenario()

    simulation.run_interactive_visualization()

    simulation.run_simulation_with_weather()
