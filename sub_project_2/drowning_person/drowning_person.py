import random

from sub_project_2.configs.config import WIDTH, HEIGHT


class DrowningPerson:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
