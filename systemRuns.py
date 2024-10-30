from elevetorSystem import ElevatorSystemRun


class SystemRuns:
    def __init__(self, data):
        self.data = data
        self.runs_total_waiting_pass_destination = 0
        self.runs_total_passengers_in_elevators = 0
        self.runs_average_time_of_waititng = 0
        self.runs_total_trips = 0
        self.runs_total_passengers = 0
        self.runs_average_occupancy_rate = 0
        
    def start(self):
        print()
        for i in range(self.data['number_runs']):
            print(f"========================== Run {i + 1} ===================================")
            
            system_run = self.data['runs'][0]
            elevator_system_run = ElevatorSystemRun(num_elevators = system_run['num_elevators'], 
                capacities = system_run['capacities'], 
                travel_time = system_run['travel_time'],
                load_time = system_run['load_time'], 
                floor_frequency=system_run['floor_frequency'],
                probability_matrix=system_run['probability_matrix'],
                time_limit=system_run['time_limit'],
                number_of_runs=self.data['number_runs']
            )          
            
            elevator_system_run.run_simulation()                                      
            
            total_waiting_pass_destination, total_passengers_in_elevators, average_time_of_waititng, total_trips, total_passengers, average_occupancy_rate = elevator_system_run.report_statistics()     
            
            self.runs_total_waiting_pass_destination = self.runs_total_waiting_pass_destination + total_waiting_pass_destination
            self.runs_total_passengers_in_elevators = self.runs_total_passengers_in_elevators + total_passengers_in_elevators            
            self.runs_average_time_of_waititng = self.runs_average_time_of_waititng + average_time_of_waititng
            self.runs_total_trips = self.runs_total_trips + total_trips
            self.runs_total_passengers = self.runs_total_passengers + total_passengers
            self.runs_average_occupancy_rate = self.runs_average_occupancy_rate + average_occupancy_rate
            
            print()
            print()
            print()
            
    def report_statistics(self):
        print("\n\n")
        number_runs = self.data['number_runs']
        print()
        print(f"======================= Статиситика прогонов (усреднённая): =========================================")
        # print(f"\tОбщее время ожидания пассажирами: {self.runs_total_waiting_pass_destination / number_runs}")
        print(f"\tОбщее число проезжащих в лифтах пассажиров: {self.runs_total_passengers_in_elevators / number_runs}")
        if (self.runs_average_time_of_waititng != float):
            print(f"\tСреднее время ожидания пассажирами: {self.runs_average_time_of_waititng / number_runs}")
        else:            
            print(f"\tСреднее время ожидания пассажирами: не определено")            
        print(f"\tОбщее количество поездок: {self.runs_total_trips / number_runs}")
        print(f"\tОбщее количество пассажиров: {self.runs_total_passengers / number_runs}")
        print(f"\tКоэффицент загрузки лифтов: {self.runs_average_occupancy_rate / number_runs}")
        print("\n")