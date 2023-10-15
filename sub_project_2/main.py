from sub_project_2.GUI.GUI import GUI
from sub_project_2.Simulation.simulation import Simulation


# Основна функція
def main():
    simulation_duration = 1_500  # Тривалість симуляції (кількість кроків)
    sim = Simulation()
    sim.run(simulation_duration)
    sim.display_metrics()

    # Запуск машинного навчання та відображення результатів у графічному інтерфейсі
    gui = GUI()
    gui.run()


if __name__ == "__main__":
    main()
