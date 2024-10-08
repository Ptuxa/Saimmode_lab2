import simpy
import random

from elevetorSystem import ElevatorSystem, LiftSystem
    
NUM_FLOORS = 9
NUM_ELEVATORS = 2
    
ELEVATOR_CAPACITIES = [6, 8]  
TRAVEL_TIME = 1  
LOAD_PASSENGERS_TIME = 0.5
SIMULATION_TIME = 120

PROBABILITY_FLOOR_MATRIX = [
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 1 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 2 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 0 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 3 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 4 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 5 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],  # Этаж 6 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]   # Этаж 7 -> на каждый другой этаж
    [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]   # Этаж 8 -> на каждый другой этаж
]

FLOOR_FREQUENCIES = [0.1, 0.15, 0.2, 0.1, 0.1, 0.1, 0.05, 0.1, 0.1]


def main(num_elevators, num_floors, elevator_capacities, travel_time, load_passengers_time, probability_floor_matrix, floor_frequencies):
    env = simpy.Environment()
    system = ElevatorSystem(env, num_elevators, elevator_capacities, travel_time, load_passengers_time)

    for i in range(10):
        start_floor = random.randint(0, 8)
        target_floor = random.randint(0, 8)
        if start_floor != target_floor:
            system.request_elevator(start_floor, target_floor)
            yield env.timeout(random.uniform(2, 5)) 

    env.run(until=SIMULATION_TIME) 
    
main(NUM_ELEVATORS, NUM_FLOORS, ELEVATOR_CAPACITIES, TRAVEL_TIME, LOAD_PASSENGERS_TIME, PROBABILITY_FLOOR_MATRIX, FLOOR_FREQUENCIES)