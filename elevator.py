class Elevator:
    def __init__(self, elevator_id, capacity, travel_time, load_time, activitiesStatistics, floors, all_time):
        self.id = elevator_id
        self.capacity = capacity
        self.travel_time = travel_time
        self.load_time = load_time
        self.current_floor = 0
        self.direction = 0
        self.total_trips = 0
        self.passengers = []
        self.total_passengers_all_time = 0 
        self.total_waiting_pass_destination = 0
        self.activitiesStatistics = activitiesStatistics
        self.floors = floors
        self.timer_counter = 0
        self.all_time = all_time

    def run(self):
        """Основная логика работы лифта"""
                    
        # Если лифт стоит (direction = 0), ищем ближайший этаж с запросом
        if self.direction == 0:
            next_floor = self.find_closest_request()
            if next_floor is not None:
                # Если следующий этаж не текущий, просто перемещаемся без загрузки
                if next_floor != self.current_floor:
                    if self.move_to_floor(next_floor) == 0: return                  
                    if self.load_unload_passengers() == 0: return
                else:
                    # Если запрос на текущем этаже, загружаем/выгружаем пассажиров
                    if self.load_unload_passengers() == 0: return
            else:
                return 1
        else:
            # Поиск следующего этажа
            next_floor = self.find_next_request()
            
            if next_floor is not None:
                # Лифт движется в направлении, если есть запросы на текущем этаже
                if self.move_to_floor(next_floor) == 0: return
                if self.load_unload_passengers() == 0: return

    def find_closest_request(self):
        """Поиск ближайшего этажа с запросом"""
        closest_floor = None
        min_distance = float('inf')

        # Проходим по всем этажам и находим ближайший с запросом
        for floor in range(9):
            if any(self.floors[floor].take_requests_before_time(self.timer_counter).values()):
                distance = abs(self.current_floor - floor)
                if distance < min_distance:
                    closest_floor = floor
                    min_distance = distance

        if closest_floor != None:              
            if len(self.floors[closest_floor].take_requests_before_time(self.timer_counter)['down']) > 0:
                self.direction = -1 
            else:
                self.direction = 1
        else:            
            self.direction = 0
            return None
            
        return closest_floor

    def direction_to_str(self):
        """Преобразование направления в строку для запроса"""
        return 'up' if self.direction == 1 else 'down'
    
    def move_to_floor(self, target_floor):
        """Перемещение лифта на другой этаж"""
        self.total_trips = self.total_trips + 1 
        print(f"Лифт {self.id + 1} перемещается с {self.current_floor + 1} этажа на {target_floor + 1} этаж в момент времени {self.timer_counter}")
        travel_floors = abs(self.current_floor - target_floor)  # Время перемещения пропорционально расстоянию
        
        before_timer_counter = self.timer_counter
        self.timer_counter = min(self.timer_counter + (self.travel_time * travel_floors), self.all_time)
        self.activitiesStatistics.append_acivities_statistics(before_timer_counter, self.timer_counter, 1, 0)        

        self.current_floor = target_floor
        print(f"Лифт {self.id + 1} прибыл на этаж {self.current_floor + 1} в момент времени {self.timer_counter}")
        
        if self.timer_counter == self.all_time:
            return 0
                
    def load_unload_passengers(self):
        """Загрузка и выгрузка пассажиров"""
        print(f"Лифт {self.id + 1} выгружает пассажиров на {self.current_floor + 1} этаж в момент времени {self.timer_counter}")
        
        print(f"До выгрузки в лифте {self.id + 1} было {len(self.passengers)} человек")
        # Выгрузка пассажиров на нужном этаже
        
        for passengerInfo in self.passengers[:]:
            if passengerInfo[0] == self.current_floor:
                self.total_waiting_pass_destination = self.total_waiting_pass_destination + (self.timer_counter - passengerInfo[1]) + self.load_time
                self.passengers.remove(passengerInfo)                
        
        print(f"После выгрузки в лифте {self.id + 1} стало {len(self.passengers)} человек")

        # Загрузка новых пассажиров с очереди
        current_floor_requests = self.floors[self.current_floor].take_requests_before_time(self.timer_counter)[self.direction_to_str()]
        while current_floor_requests and len(self.passengers) < self.capacity:
            self.total_passengers_all_time = self.total_passengers_all_time + 1
            values = current_floor_requests.pop(0)
            # print(f"target floor: {values[0] + 1}")
            # print(f"timer_marker: {values[1]}")
            self.passengers.append((values[0], values[1]))
        
        self.floors[self.current_floor].requests[self.direction_to_str()] = current_floor_requests
            
        print(f"В лифте {self.id + 1} после загрузки пассажиров стало {len(self.passengers)} человек")
        print()

        before_timer_counter = self.timer_counter
        self.timer_counter = min(self.timer_counter + self.load_time, self.all_time)
        self.activitiesStatistics.append_acivities_statistics(before_timer_counter, self.timer_counter, 0, 1)        
        
        if self.timer_counter == self.all_time:
            return 0

    def find_next_request(self):
        
        """Поиск следующего этажа с запросом"""
        
        close_floor = float('inf')
        min_distance = float('inf')
        for floor in range(self.current_floor + self.direction, 9 if self.direction == 1 else -1, self.direction):
            if self.floors[floor].take_requests_before_time(self.timer_counter)[self.direction_to_str()]:
                if floor != self.current_floor:
                    close_floor = floor
                    min_distance = abs(close_floor - floor)
                
        for i in range(len(self.passengers)):   
            if self.passengers[i][0] != self.current_floor:  
                if (abs(self.passengers[i][0] - self.current_floor) < min_distance):
                    min_distance = abs(self.passengers[i][0] - self.current_floor)
                    close_floor = self.passengers[i][0]
        
        if (close_floor != float('inf')):
            return close_floor
            
        self.direction = 0
        return None
    
    def increase_timer_counter(self, timestamp):
        before_timer_counter = self.timer_counter
        self.timer_counter = min(max(timestamp, before_timer_counter), self.all_time)        
        
        self.activitiesStatistics.append_acivities_statistics(before_timer_counter, self.timer_counter, 0, 2)