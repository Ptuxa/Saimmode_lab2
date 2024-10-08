class Elevator:
    def __init__(self, env, id, capacity, travel_time, load_time):
        self.env = env
        self.id = id
        self.capacity = capacity
        self.travel_time = travel_time
        self.load_time = load_time
        self.current_floor = 0
        self.passengers = []
        self.requests = []
        self.busy = False
        self.direction = 1  # 1 - вверх, -1 - вниз

    def move_to(self, target_floor):
        travel_duration = abs(self.current_floor - target_floor) * self.travel_time
        print(f"Лифт {self.id} движется на {target_floor}, время: {travel_duration}")
        yield self.env.timeout(travel_duration)
        self.current_floor = target_floor
        print(f"Лифт {self.id} прибыл на этаж {self.current_floor}")

    def load_passengers(self, floor_requests):
        print(f"Лифт {self.id} загружает пассажиров на {self.current_floor}")
        for request in floor_requests:
            if len(self.passengers) < self.capacity:
                self.passengers.append(request)
                print(f"Пассажир с {request.start_floor} на {request.target_floor} сел в лифт {self.id}")
        yield self.env.timeout(self.load_time)

    def unload_passengers(self):
        print(f"Лифт {self.id} выгружает пассажиров на {self.current_floor}")
        self.passengers = [p for p in self.passengers if p.target_floor != self.current_floor]
        yield self.env.timeout(self.load_time)

    def find_nearest_request(self):
        if not self.requests:
            return None
        return min(self.requests, key=lambda r: abs(r - self.current_floor))

    def process_requests(self):
        while True:
            if self.requests:
                target_floor = self.find_nearest_request()
                yield self.env.process(self.move_to(target_floor))
                yield self.env.process(self.unload_passengers())
                self.requests.remove(target_floor)
            else:
                print(f"Лифт {self.id} ожидает запросов")
                yield self.env.timeout(1)  # Пауза перед проверкой очередных запросов
