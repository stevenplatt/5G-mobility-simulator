import random

# grid coordinates of each 5G towers
tower_1 = (0, 0)
tower_2 = (-5, 5)
tower_3 = (5, 5)
tower_4 = (5, -5)
tower_5 = (-5, -5)

# channel allocations of each 5G tower
allocation_tower_1 = (2)
allocation_tower_2 = (4)
allocation_tower_3 = (1)
allocation_tower_4 = (1)
allocation_tower_5 = (3)

def random_walk(n):
	#return coordinates after 'n' block random walk
	x = 0
	y = 0
	for i in range(n):
		step = random.choice(['N', 'S', 'E', 'W'])
		if step == 'N':
			y = y + 1
		elif step == 'S':
			y = y - 1
		elif step == 'E':
			x = x + 1
		else:
			x = x - 1
	return (x, y)

number_of_walks = 100

for walk_length in range(1, 10):
	associate_tower_1 = 0 # number of times the device requests to associate to tower [x]
	associate_tower_2 = 0
	associate_tower_3 = 0
	associate_tower_4 = 0
	associate_tower_5 = 0
	for i in range(number_of_walks):
		(x, y) = random_walk(walk_length)
		if (x) < -3: 
			print((x, y), "Associated to either tower 2 or 5")
		else: 
			print("Associated to either tower 1, 2, or 3")
