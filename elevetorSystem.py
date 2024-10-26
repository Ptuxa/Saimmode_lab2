from elevator import Elevator
from floor import Floor


class ElevatorSystemRun:
    def __init__(self, num_elevators, capacities, travel_time, load_time, floor_frequency, probability_matrix, time_limit, number_of_runs):
        self.floors = [Floor(i, floor_frequency[i], probability_matrix, time_limit) for i in range(9)]
        self.elevators = [Elevator(i, capacities[i], travel_time, load_time, self.floors, time_limit) for i in range(num_elevators)]
        self.time_limit = time_limit
        self.number_of_runs = number_of_runs          
        
    def run_simulation(self):
        is_increase_time = False        
        is_stop_simulation = False
            
        while is_stop_simulation == False:                            
            is_stop_simulation = True
        
            min_time = float('inf')
            
            for j in range(len(self.floors)):
                if self.floors[j].timer_counter < self.time_limit: 
                    self.floors[j].generate_passengers()
                    self.floors[j].timer_counter = self.floors[j].timer_counter + 1
                    is_stop_simulation = False
                    
            # print()
                        
            if is_increase_time == True:
                for j in range(len(self.floors)):
                    min_time_j = self.floors[j].take_min_time()                        
                    if (min_time_j < min_time):
                        min_time = min_time_j
                
                if (min_time != float('inf')):
                    for j in range(len(self.elevators)):
                        self.elevators[j].increase_timer_counter(min_time)
                    is_increase_time = False
                
            if is_increase_time == False:
                for j in range(len(self.elevators)):
                    if self.elevators[j].timer_counter < self.time_limit:
                        is_stop_simulation = False
                        if self.elevators[j].run() == 1: 
                            is_increase_time = True                                                        
                            break        
            
    def report_statistics(self):
        total_passengers_in_elevators = 0
        total_passengers = 0
        total_trips = 0 
        total_waiting_pass_destination = 0
        average_time_of_waititng = float('inf')
        for i in range(len(self.floors)):
            total_passengers = total_passengers + self.floors[i].total_passengers  
            
        for i in range(len(self.elevators)):
            
            total_trips = total_trips + self.elevators[i].total_trips  
            total_passengers_in_elevators = total_passengers_in_elevators + self.elevators[i].total_passengers_all_time
            total_waiting_pass_destination = total_waiting_pass_destination + self.elevators[i].total_waiting_pass_destination 
        
        # print(f"\tОбщее время ожидания пассажирами: {total_waiting_pass_destination}")
        print(f"\tОбщее число проезжащих в лифтах пассажиров: {total_passengers_in_elevators}")
        if (total_passengers_in_elevators != 0):
            average_time_of_waititng = total_waiting_pass_destination / total_passengers_in_elevators
            print(f"\tСреднее время ожидания пассажирами: {average_time_of_waititng}")
        else:
            average_time_of_waititng = float('inf')
            print(f"\tСреднее время ожидания пассажирами: не определено")            
        print(f"\tОбщее количество поездок: {total_trips}")
        print(f"\tОбщее количество пассажиров: {total_passengers}")
        
        return total_waiting_pass_destination, total_passengers_in_elevators, average_time_of_waititng, total_trips, total_passengers