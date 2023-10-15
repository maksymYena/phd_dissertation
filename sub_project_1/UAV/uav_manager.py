from sub_project_1.UAV.uav import UAV


class UAVManager:
    def __init__(self, num_uavs=10):
        self.uavs = [UAV() for _ in range(num_uavs)]

    def move_uavs(self, other_aircraft=None):
        for uav in self.uavs:
            uav.move(time_step=1, other_aircraft=other_aircraft)  # Pass the other_aircraft parameter if needed

    def update_weather(self):
        for uav in self.uavs:
            uav.weather_model.update_weather()