import random
import numpy as np

class ElevatorSystem:
    def __init__(self, env, num_elevators, capacities, travel_time, load_time):
        self.env = env
        self.elevators = [Elevator(env, i, capacities[i], travel_time, load_time) for i in range(num_elevators)]
        self.floors = [Floor(i) for i in range(9)]  # 9 этажей

    def request_elevator(self):
        # Выбор начального этажа на основе частот
        start_floor = np.random.choice(range(9), p=FLOOR_FREQUENCIES)
        
        # Выбор целевого этажа на основе вероятности из матрицы
        target_floor = np.random.choice(range(9), p=PROBABILITY_MATRIX[start_floor])

        if start_floor != target_floor:
            passenger = Passenger(id=random.randint(100, 999), start_floor=start_floor, target_floor=target_floor)
            self.floors[start_floor].add_request(passenger)
            print(f"Запрос на лифт с этажа {start_floor} на этаж {target_floor}")

            # Находим ближайший свободный лифт
            nearest_elevator = min(self.elevators, key=lambda e: abs(e.current_floor - start_floor) if not e.busy else float('inf'))
            if not nearest_elevator.busy:
                nearest_elevator.requests.append(start_floor)
                self.env.process(nearest_elevator.process_requests())
            else:
                print(f"Все лифты заняты")

def run_simulation():
    env = simpy.Environment()
    num_elevators = 2
    capacities = [6, 8]  # Вместимость лифтов
    travel_time = 1  # Время перемещения между этажами
    load_time = 0.5  # Время на загрузку и разгрузку
    system = ElevatorSystem(env, num_elevators, capacities, travel_time, load_time)

    # Генерация пассажиров
    for i in range(10):
        system.request_elevator()
        yield env.timeout(random.uniform(2, 5))  # Время между вызовами

    env.run(until=120)  # Симуляция 2 часа

if __name__ == "__main__":
    run_simulation()
