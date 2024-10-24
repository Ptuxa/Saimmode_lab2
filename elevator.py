class Elevator:
    def __init__(self, env, elevator_id, capacity, travel_time, load_time, floors):
        self.env = env
        self.id = elevator_id
        self.capacity = capacity
        self.travel_time = travel_time
        self.load_time = load_time
        self.current_floor = 0
        self.direction = 0
        self.total_trips = 0
        self.passengers = []
        self.floors = floors
        self.timer_counter = 0

    def run(self):
        """Основная логика работы лифта"""
        # Если лифт стоит (direction = 0), ищем ближайший этаж с запросом
        if self.direction == 0:
            next_floor = self.find_closest_request()
            if next_floor is not None:
                # Если следующий этаж не текущий, просто перемещаемся без загрузки
                if next_floor != self.current_floor:
                    self.move_to_floor(next_floor)
                    self.load_unload_passengers()
                else:
                    # Если запрос на текущем этаже, загружаем/выгружаем пассажиров
                    self.load_unload_passengers()
            # else:
                # self.timer_counter = self.timer_counter + 1
        else:
            # Поиск следующего этажа
            next_floor = self.find_next_request()
            
            if next_floor is not None:
                # Лифт движется в направлении, если есть запросы на текущем этаже
                self.move_to_floor(next_floor)
                self.load_unload_passengers()

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
        self.timer_counter = self.timer_counter + (self.travel_time * travel_floors)
        self.current_floor = target_floor
        print(f"Лифт {self.id + 1} прибыл на этаж {self.current_floor + 1} в момент времени {self.timer_counter}")
        print()
        
    def load_unload_passengers(self):
        """Загрузка и выгрузка пассажиров"""
        print(f"Лифт {self.id + 1} выгружает пассажиров на {self.current_floor + 1} этаж в момент времени {self.timer_counter}")
        
        print(f"До выгрузки в лифте {self.id + 1} было {len(self.passengers)} человек")
        # Выгрузка пассажиров на нужном этаже
        self.passengers = [p for p in self.passengers if p[0] != self.current_floor]
        print(f"После выгрузки в лифте {self.id + 1} стало {len(self.passengers)} человек")

        # Загрузка новых пассажиров с очереди
        current_floor_requests = self.floors[self.current_floor].take_requests_before_time(self.timer_counter)[self.direction_to_str()]
        while current_floor_requests and len(self.passengers) < self.capacity:
            target_floor = current_floor_requests.pop(0)            
            self.passengers.append(target_floor)
        
        self.floors[self.current_floor].requests[self.direction_to_str()] = current_floor_requests
            
        print(f"В лифте {self.id + 1} после загрузки пассажиров стало {len(self.passengers)} человек")
        print()

        self.timer_counter = self.timer_counter + self.load_time

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
