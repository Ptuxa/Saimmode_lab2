import random

import numpy as np


class Floor:
    def __init__(self, env, floor_id, frequency, probability_matrix):
        self.env = env
        self.floor_id = floor_id
        self.frequency = frequency
        self.probability_matrix = probability_matrix
        self.env.process(self.generate_passengers())

    def generate_passengers(self, elevator_system):
        """Генерация пассажиров на этаже"""
        while True:
            yield self.env.timeout(random.expovariate(self.frequency))
            target_floor = np.random.choice(range(9), p=self.probability_matrix[self.floor_id])
            direction = 'up' if target_floor > self.floor_id else 'down'
            print(f"Пассажир на этаже {self.floor_id} ждёт лифт {direction} в {self.env.now}")
            # Пассажир добавляется в очередь на этаже
            elevator_system.add_request(self.floor_id, direction)
