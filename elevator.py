class Elevator:
    def __init__(self, env, current_floor, capacity, travel_time, load_time, floors):
        self.env = env
        self.current_floor = current_floor  # Текущий этаж
        self.capacity = capacity  # Вместимость лифта
        self.travel_time = travel_time
        self.load_time = load_time
        self.floors = floors  # Список всех этажей, для доступа к их очередям
        self.direction = 0  # 1 - вверх, -1 - вниз, 0 - стоит
        self.passengers = []  # Пассажиры в лифте

    def run(self):
        """Основная логика работы лифта"""
        while True:
            # Если лифт стоит (direction = 0), ищем ближайший этаж с запросом
            if self.direction == 0:
                next_floor = self.find_closest_request()
                if next_floor is not None:
                    # Если следующий этаж не текущий, просто перемещаемся без загрузки
                    if next_floor != self.current_floor:
                        yield self.env.process(self.move_to_floor(next_floor))
                        yield self.env.process(self.load_unload_passengers())
                    else:
                        # Если запрос на текущем этаже, загружаем/выгружаем пассажиров
                        yield self.env.process(self.load_unload_passengers())
                else:
                    yield self.env.timeout(1)
            else:
                # Поиск следующего этажа
                next_floor = self.find_next_request()
                
                # Лифт движется в направлении, если есть запросы на текущем этаже
                if self.floors[self.current_floor].requests[self.direction_to_str()]:
                    yield self.env.process(self.load_unload_passengers())
                
                if next_floor is not None:
                    yield self.env.process(self.move_to_floor(next_floor))
                else:
                    # Если запросов нет, лифт остается на текущем этаже и ждет
                    yield self.env.timeout(1)

    # def find_next_request(self):
    #     """Поиск следующего этажа по направлению"""
    #     for floor in range(self.current_floor + self.direction, 10 if self.direction == 1 else 0, self.direction):
    #         if self.requests[floor][self.direction_to_str()]:
    #             return floor
    #     # Если запросов нет, меняем направление
    #     self.direction *= -1
    #     return None

    def find_closest_request(self):
        """Поиск ближайшего этажа с запросом"""
        closest_floor = None
        min_distance = float('inf')

        # Проходим по всем этажам и находим ближайший с запросом
        for floor in range(9):
            if any(self.floors[self.current_floor].requests.values()):
                distance = abs(self.current_floor - floor)
                if distance < min_distance:
                    closest_floor = floor
                    min_distance = distance
                    
        if self.floors[floor].requests['down']:
            self.direction = -1 
        else:
            self.direction = 1

        return closest_floor

    def direction_to_str(self):
        """Преобразование направления в строку для запроса"""
        return 'up' if self.direction == 1 else 'down'

    def move_to_floor(self, target_floor):
        """Перемещение лифта на другой этаж"""
        print(f"Лифт перемещается с {self.current_floor} на {target_floor} в {self.env.now}")
        travel_floors = abs(self.current_floor - target_floor)  # Время перемещения пропорционально расстоянию
        yield self.env.timeout(self.travel_time * travel_floors)
        self.current_floor = target_floor
        print(f"Лифт прибыл на {self.current_floor} в {self.env.now}")

    # def load_unload_passengers(self):
    #     """Процесс загрузки/выгрузки пассажиров"""
    #     print(f"Лифт загружает/выгружает пассажиров на {self.current_floor} в {self.env.now}")
    #     yield self.env.timeout(self.travel_time)  # Время загрузки/выгрузки пассажиров
        
    def load_unload_passengers(self):
        """Загрузка и выгрузка пассажиров"""
        print(f"Лифт загружает/выгружает пассажиров на {self.current_floor} в {self.env.now}")
        
        # Выгрузка пассажиров на нужном этаже
        self.passengers = [p for p in self.passengers if p != self.current_floor]

        # Загрузка новых пассажиров с очереди
        current_floor_requests = self.floors[self.current_floor].requests[self.direction_to_str()]
        while current_floor_requests and len(self.passengers) < self.capacity:
            target_floor = current_floor_requests.pop(0)
            self.passengers.append(target_floor)

        yield self.env.timeout(self.load_time)

    def find_next_request(self):
        
        """Поиск следующего этажа с запросом"""
        for floor in range(self.current_floor + self.direction, 9 if self.direction == 1 else -1, self.direction):
            if self.floors[floor].requests[self.direction_to_str()]:
                return floor
            
        self.direction = 0
        return None
