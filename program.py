import simpy
import numpy as np

from elevetorSystem import ElevatorSystem

# Входные 
NUM_ELEVATORS = 2
TRAVEL_TIME = 10  # Время движения лифта от этажа до этажа (сек)
LOAD_TIME = 5  # Время загрузки лифта (сек)
FLOOR_FREQUENCY = [0.2, 0.3, 0.5, 0.1, 0.4, 0.2, 0.6, 0.4, 0.3]  # Частота пассажиров на каждом этаже (в мин)
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
TIME_LIMIT = 120  # Ограничение по времени (минуты)

# Запуск симуляции
env = simpy.Environment()
elevator_system = ElevatorSystem(env, num_elevators=NUM_ELEVATORS, capacities=CAPACITIES, travel_time=TRAVEL_TIME, load_time=LOAD_TIME, floor_frequency=FLOOR_FREQUENCY, probability_matrix=PROBABILITY_MATRIX)
env.run(until=TIME_LIMIT)