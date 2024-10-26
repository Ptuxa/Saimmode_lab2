# 1 BUILDING A SIMULATION MODEL
## 1.1 Content description of the object
A nine-story office is served by 2 elevators. The movement of the occupied or called elevator cannot be interrupted.
## 1.2 Conceptual model
The conceptual model is represented by 2 elevators that move between 9 floors. On each floor, one of the elevators is waiting for passengers. Each elevator has 2 buttons (up, down). All passengers are assumed to press the elevator button according to the direction of travel required to reach the desired floor. It is assumed that a passenger calls both elevators on request to reach the corresponding floor, i.e., presses the call buttons of both elevators. As the elevator moves, the elevator may stop at the floors on which it was called in the direction of travel, i.e., the elevator may load and unload passengers as it moves. If the elevator is found to be empty, it searches for the nearest floor with a request. If the “distance” between the request from the floor above the elevator and the elevator is the same as the “distance” between the request from the floor below the elevator and the elevator, the request below the elevator is preferred. Passenger loading and unloading are simplistically considered as a single simultaneous process.
The unit of model time will be 1 minute. The IE will be terminated after the specified time interval. We will choose the following characteristics as model responses:
1) total number of elevator trips (discrete response);
2) the total number of passengers carried by the elevators (discrete response);
3) total number of passengers who waited for an elevator (discrete response);
4) the average time it takes for a passenger to get to the floor they want (continuous response), 
where - total time of passengers waiting for the elevator, elevator loading, time needed for the elevator to get to the floor needed by the passenger, time of unloading passengers from the elevator.