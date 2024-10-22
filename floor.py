import random

import numpy as np


class Floor:
    def __init__(self, env, floor_id, frequency, probability_matrix):
        self.env = env
        self.floor_id = floor_id
        self.frequency = frequency
        self.probability_matrix = probability_matrix
        self.requests = {'up': [], 'down': []}  # Очереди пассажиров для каждого направления
        self.env.process(self.generate_passengers())
        self.total_passengers = 0

    def generate_passengers(self):
        """Генерация пассажиров на этаже"""
        while True:
            yield self.env.timeout(random.expovariate(1 / self.frequency))
            target_floor = np.random.choice(range(9), p=self.probability_matrix[self.floor_id])
            direction = 'up' if target_floor > self.floor_id else 'down'            
            # Пассажир добавляется в общую очередь на этаже
            self.requests[direction].append(target_floor)
            self.total_passengers = self.total_passengers + 1;            
            print(f"Пассажир стоит в очереди на {self.floor_id + 1} этаже, намеревается ехать на {target_floor + 1} этаж в момент времени {self.env.now}")