import random

def create_tower_range(x_start, x_end, y_start, y_end):
    coors=[]
    
    x_step, y_step = 1, 1
    
    if x_start > x_end: 
        x_step = -1

    if y_start > y_end: 
        y_step = -1

    
    for x in range(x_start, x_end, x_step):
        for y in range(y_start, y_end, y_step):
            if (x,y) not in coors:
                coors.append((x,y))
    
    return coors


tower_1_range = create_tower_range(-3, 4, -3, 4)
tower_1_greater_range = create_tower_range(-4,5,-4,5)
tower_1_extension = [x for x in tower_1_greater_range if x not in tower_1_range]

tower_2_range = create_tower_range(0,-11, 0, 11)
tower_3_range = create_tower_range(0, 11, 0, 11)
tower_4_range = create_tower_range(0, 11, 0,-11)
tower_5_range = create_tower_range(0,-11, 0,-11)

total_tower_range = create_tower_range(-10,11, -10,11)

"""
print("1:", len(tower_1_range), 
      "2:", len(tower_2_range), 
      "3:", len(tower_3_range), 
      "4:", len(tower_4_range),
      "5:", len(tower_5_range), 
      "T:", len(total_tower_range))


print("TOWER 1: ", tower_1_range)
print("::::::::::::::::::::::::")

print("TOWER 2: ", tower_2_range)
print("::::::::::::::::::::::::")

print("TOWER 3: ", tower_3_range)
print("::::::::::::::::::::::::")

print("TOWER 4: ", tower_4_range)
print("::::::::::::::::::::::::")

print("TOWER 5: ", tower_5_range)
print("::::::::::::::::::::::::")

print("TOTAL TOWER RANGER: ", total_tower_range)
print("::::::::::::::::::::::::")

"""
tower_1_coverage = tower_1_range
tower_2_coverage = [x for x in tower_2_range if x not in tower_1_range]
tower_3_coverage = [x for x in tower_3_range if x not in tower_1_range]
tower_4_coverage = [x for x in tower_4_range if x not in tower_1_range]
tower_5_coverage = [x for x in tower_5_range if x not in tower_1_range]
tower_coverages = [tower_1_coverage, tower_2_coverage, tower_3_coverage, tower_4_coverage, tower_5_coverage]

tower_1_coverage_opt = tower_1_range
tower_1ext_coverage = tower_1_extension
tower_2_coverage_opt = [x for x in tower_2_range if x not in tower_1_greater_range]
tower_3_coverage_opt = [x for x in tower_3_range if x not in tower_1_greater_range]
tower_4_coverage_opt = [x for x in tower_4_range if x not in tower_1_greater_range]
tower_5_coverage_opt = [x for x in tower_5_range if x not in tower_1_greater_range]
tower_coverages_opt = [tower_1_coverage_opt, tower_2_coverage_opt, tower_3_coverage_opt, tower_4_coverage_opt, tower_5_coverage_opt, tower_1ext_coverage]


def random_walk(n):
	#return coordinates after 'n' block random walk
	x = 0
	y = 0
	for i in range(n):
		step = random.choice(['N', 'S', 'E', 'W'])
		if step == 'N': y = y + 1
		elif step == 'S': y = y - 1
		elif step == 'E': x = x + 1
		else: x = x - 1
	return (x, y)


def find_tower(agent_x, agent_y, ext=False):
    coverage_area = tower_coverages
    if ext: coverage_area = tower_coverages_opt
    
    tower = 1
    towers_in_range = []
    
    for area in coverage_area:
        if (agent_x,agent_y) in area: 
            towers_in_range.append(tower)
        tower += 1
    return random.choice(towers_in_range)

s1_history = [0, 0, 0, 0, 0]
s2_history = [0, 0, 0, 0, 0, 0]

def keep_history(history, tower):
    history[tower-1] += 1

"""
def get_allocation(tower, agent_loc, ext=True):

    alloc = alloc_dict[str(tower)]
    return alloc
"""


def get_allocation(history):
    alloc_dict = {"1":7, "2":5, "3":5, "4":5, "5":5, "6":6}
    allocs = []
    
    number_of_walks = 0
    
    for tower in range(len(history)):
        number_of_walks += history[tower]
        allocs.append(history[tower] * alloc_dict[str(tower+1)])

    return float(sum(allocs))/float(number_of_walks)
        
for i in range(1000):
    agent_pos = random_walk(10)
    x, y = agent_pos
    
    # Scenario 1
    tower = find_tower(x, y, ext=False)
    keep_history(s1_history, tower)
        
    # Scenario 2
    tower = find_tower(x, y,ext=True)
    keep_history(s2_history, tower)
    

print("Scenario 1 History")
print(s1_history)
print("Total Average Allocation: ")
print(get_allocation(s1_history))

print("Scenario 2 History")
print(s2_history)
print("Total Average Allocation: ")
print(get_allocation(s2_history))
