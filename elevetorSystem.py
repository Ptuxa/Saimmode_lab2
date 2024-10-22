from elevator import Elevator
from floor import Floor


class ElevatorSystem:
    def __init__(self, env, num_elevators, capacities, travel_time, load_time, floor_frequency, probability_matrix):
        self.env = env
        self.floors = [Floor(env, i, floor_frequency[i], probability_matrix) for i in range(9)]
        self.elevators = [Elevator(env, i, capacities[i], travel_time, load_time, self.floors) for i in range(num_elevators)]

    def report_statistics(self, total_waiting_time):
        total_passengers = 0
        total_trips = 0 
        for i in range(len(self.floors)):
            total_passengers = total_passengers + self.floors[i].total_passengers  
            
        for i in range(len(self.elevators)):
            total_trips = total_trips + self.elevators[i].total_trips  
            
        avg_waiting_time = total_waiting_time / total_passengers if total_passengers > 0 else 0
        print(f"Среднее время ожидания: {avg_waiting_time:.2f}")
        print(f"Общее количество поездок: {total_trips}")
        print(f"Общее количество пассажиров: {total_passengers}")