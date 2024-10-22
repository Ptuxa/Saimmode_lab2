import numpy as np

class Floor:
    def __init__(self, env, floor_id, frequency, probability_matrix, time_limit):
        self.env = env
        self.floor_id = floor_id
        self.frequency = frequency
        self.probability_matrix = probability_matrix
        self.requests = {'up': [], 'down': []}  # Очереди пассажиров для каждого направления
        self.total_passengers = 0
        self.timer_counter = 0
        self.time_limit = time_limit

    def generate_passengers(self):
        """Генерация пассажиров на этаже"""
        if self.timer_counter < self.time_limit:            
            for i in range(1):
                target_floor = np.random.choice(range(9), p=self.probability_matrix[self.floor_id])
                direction = 'up' if target_floor > self.floor_id else 'down'            
                # Пассажир добавляется в общую очередь на этаже
                self.requests[direction].append((target_floor, self.timer_counter))
                self.total_passengers = self.total_passengers + 1;            
                print(f"Пассажир стоит в очереди на {self.floor_id + 1} этаже, намеревается ехать на {target_floor + 1} этаж в момент времени {self.timer_counter}")
            
    def take_requests_before_time(self, current_timer_counter):
        new_requests = {'up': [], 'down': []}
        
        for direction, request in self.requests.items():                                    
            for target_floor, timer_counter in request:
                if timer_counter <= current_timer_counter:
                    new_requests[direction].append((target_floor, timer_counter))
                    
        return new_requests                