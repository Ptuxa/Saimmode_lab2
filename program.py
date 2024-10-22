import simpy

from elevetorSystem import ElevatorSystem

# Входные 
NUM_ELEVATORS = 2
TRAVEL_TIME = 3 / 60  # Время движения лифта от этажа до этажа (мин)
LOAD_TIME = 5 / 60  # Время загрузки лифта (мин)
FLOOR_FREQUENCY = [3, 1, 1, 2, 2, 2, 2, 2, 2]  # Частота пассажиров на каждом этаже (в мин)
CAPACITIES = [6, 8]  # Вместимость лифтов
PROBABILITY_MATRIX = [
    [0, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1],  # The 1st floor -> to every other floor. 
    [0.2, 0, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1],  # The 2nd floor -> to every other floor. 
    [0.2, 0.1, 0, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1],  # The 3rd floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0, 0.1, 0.2, 0.1, 0.1, 0.1],  # The 4th floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0.1, 0, 0.2, 0.1, 0.1, 0.1],  # The 5th floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0.1, 0.1, 0, 0.2, 0.1, 0.1],  # The 6th floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0, 0.1, 0.1],  # The 7th floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0, 0.1],   # The 8th floor -> to every other floor. 
    [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0]   # The 9th floor -> to every other floor. 
]
TIME_LIMIT = 5  # Ограничение по времени (мин)
NUMBER_OF_RUNS = 1

# Запуск симуляции
env = simpy.Environment()
elevator_system = ElevatorSystem(env, num_elevators=NUM_ELEVATORS, capacities=CAPACITIES, travel_time=TRAVEL_TIME, load_time=LOAD_TIME, floor_frequency=FLOOR_FREQUENCY, probability_matrix=PROBABILITY_MATRIX, time=TIME_LIMIT, number_of_runs=NUMBER_OF_RUNS)

print()
elevator_system.start()
print()
print()

elevator_system.report_statistics(TIME_LIMIT)