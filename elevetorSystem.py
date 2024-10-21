from elevator import Elevator
from floor import Floor


class ElevatorSystem:
    def __init__(self, env, num_elevators, capacities, travel_time, load_time, floor_frequency, probability_matrix):
        self.env = env
        self.elevators = [Elevator(env, i, capacities[i], travel_time, load_time) for i in range(num_elevators)]
        self.floors = [Floor(env, i, floor_frequency[i], probability_matrix) for i in range(9)]
    
    def add_request(self, floor, direction):
        """Добавление запроса на вызов лифта"""
        for elevator in self.elevators:
            elevator.requests[floor][direction].append(1)  # добавляем пассажира в очередь