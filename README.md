# 5G-mobility-simulator
A simple 5G mobility simulator written in Python.

This mobility simulator recreates the devices handoff procedure that occurs in a 5G network and was used to produce a research paper titled "Using Transition Learning to Enhance Mobile-Controlled Handoff" (pending publication). 

The simulator operates based on the 23x23 grid environment shown below: 

![simulator grid environment](https://github.com/stevenplatt/5G-mobility-simulator/blob/main/img/coverage_grid_scenario_2.png?raw=true)

The simulation starts with a device placed at grid position [11,11], from here the device does a random walk of 10 steps (each step represents a city block). This 10 step walk is completed continuously 2000 times for a single round of simulation.  

## Running the Simulator
v3 is the most up-to-date version of the simulator, it can be run using the commands below: 

```
$: git clone https://github.com/stevenplatt/5G-mobility-simulator.git

$: cd 5G-mobility-simulator

~/5G-mobility-simulator$: python3 simulator_v3.py
```

## Simulator Output

The simulation environment runs two different simulations. One where the default behavior of connecting to the closest base station is used, and a second where an override is performed in certain conditions to enhance performance. At the end of the simulation there are a number of graph outputs. These include: 

### Random Walk Allocation Histogram

![Random Walk Allocation Histogram](https://github.com/stevenplatt/5G-mobility-simulator/blob/main/img/load_histogram.png?raw=true)

### Single Round Allocation

![Single Round Allocation](https://github.com/stevenplatt/5G-mobility-simulator/blob/main/img/load_snapshot.png?raw=true)

### Average Allocation Map

![Average Allocation Map](https://github.com/stevenplatt/5G-mobility-simulator/blob/main/img/load_learned.png?raw=true)

### Final Simulation Result

![Final Simulation Result](https://github.com/stevenplatt/5G-mobility-simulator/blob/main/img/simulation_results.png?raw=true)


Full explanation of the information theory relating to the random walk behavior and network allocation can be found in the research paper relating to this simulator (pending publication). 


