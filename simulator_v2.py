import random
import math  #
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
import seaborn as sns

tower_allocations = [7, 5, 5, 5, 5]
tower_positions = [(11,11), (0, 22), (22, 22), (22, 0), (0, 0)]


deadzone_x = [13,14,15]
deadzone_y = [13,14,15]
deadzones = list(itertools.product(deadzone_x, deadzone_y))

deadzone_allocation = 1

show = np.zeros((22,22))

def random_walk(start_loc, n):

    x = start_loc[0]
    y = start_loc[1]

    for i in range(n):
        step = random.choice(['N', 'S', 'E', 'W'])

        if step == 'N':
            if y == 22: pass
            else: y = y + 1
        elif step == 'S':
            if y == 0: pass
            else: y = y - 1
        elif step == 'E':
            if x == 22: pass
            else: x = x + 1
        else:
            if x == 0: pass
            else: x = x - 1

    return (x, y)

def get_towers(pos, debug=False):

    if debug: print("Agent pos: " + str(pos))
    closest_towers = []
    differences = []
    t_id = 1

    for tower_pos in tower_positions:
        diffx = tower_pos[0] - pos[0]
        diffy = tower_pos[1] - pos[1]
        total_diff = math.sqrt(diffx ** 2 + diffy ** 2)

        if debug: print("Distance to tower " + str(t_id) + ": " + str(total_diff))
        t_id += 1
        differences.append(total_diff)

    closest_towers = np.argsort(differences)[:3]
    closest_towers = [x+1 for x in closest_towers]
    if debug: print("Closest towers are :", closest_towers)
    return closest_towers


def get_allocation(deadzone, tower, pos):

    tower_index = tower - 1
    allocation = tower_allocations[tower_index]

    if deadzone:
        if pos in deadzones: # If agent is in dead zone, override normal allocation
            allocation = deadzone_allocation

    return allocation

def run_experiment(extra_logic=False, dead_zone = False, dead_zone_suppression=False, num_trials=10, num_walks=1000, num_steps=5, debug=False):

    mean_allocations = []

    override_counter = 0
    transition_counter = 0
    transitions_encountered = 0

    heatmap = np.zeros([23, 23])


    values = np.zeros((23,23), dtype=object)

    for e in range(num_trials):

        number_of_walks = num_walks

        agent_pos = (11,11)

        tower_ranking = get_towers(agent_pos, debug)

        current_ranking = tower_ranking[:3]
        new_ranking = []

        current_allocation = get_allocation(dead_zone, current_ranking[0], agent_pos)

        new_allocation = 0
        delta_allocation = 0

        transition_history = []
        allocation_dict = {}
        allocations = []

        suspended_transitions = []
        suspend_counter = 5
        lastallocation = np.zeros([23, 23])

        for i in range(number_of_walks):

            agent_pos = random_walk(agent_pos, num_steps)

            x, y = agent_pos
            closest_towers = get_towers(agent_pos, debug=debug)
            new_ranking = closest_towers[:3]

            if current_ranking != new_ranking:

                transitions_encountered += 1
                transition = current_ranking + new_ranking
                transition = tuple(transition)

                if debug:
                    print("__ Transition __")
                    print("Player pos: ", x, y)
                    print("Current ranking: ", current_ranking)
                    print("New ranking: ", new_ranking)
                    print("Current allocation", current_allocation)

                if transition not in transition_history:

                    if debug: print("New transition experience.")

                    new_allocation = get_allocation(dead_zone, new_ranking[0], agent_pos)
                    delta_allocation = new_allocation - current_allocation

                    allocation_dict[transition] = delta_allocation

                    transition_history.append(transition)

                    current_ranking = new_ranking
                    current_allocation = new_allocation
                    transition_counter += 1

                else:

                    if allocation_dict[transition] >= 0: # If expected allocation is higher, make the transition
                        if debug: print("Positive delta, transitioning to new tower.")
                        if dead_zone_suppression:  # If dead zone suppression is activated:

                            if transition not in suspended_transitions: # If transition not suspended:
                                new_allocation = get_allocation(dead_zone, new_ranking[0], agent_pos)

                                real_delta_allocation = new_allocation - current_allocation
                                expected_delta_allocation = allocation_dict[transition]

                                if expected_delta_allocation > real_delta_allocation:   # Dead zone check
                                    suspended_transitions.append(transition)
                                current_allocation = new_allocation
                                transition_counter += 1

                            else: # Suspended transition, do not make the transition
                                if suspend_counter == 0:
                                    suspended_transitions.remove(transition) # Get the transition off the suspend list
                                    suspend_counter = 5
                                else:
                                    suspend_counter -= 1

                        else: # Dead zone suppression is not activated! Continue with the transition
                            new_allocation = get_allocation(dead_zone, new_ranking[0], agent_pos)
                            current_allocation = new_allocation
                            transition_counter += 1

                    else: # If expected allocation is lower:
                        if not extra_logic: # If extra_logic is not activated make the transition
                            new_allocation = get_allocation(dead_zone, new_ranking[0], agent_pos)
                            current_allocation = new_allocation
                            transition_counter += 1
                        else:
                            if debug: print("Negative delta, not transitioning to new tower.")
                            override_counter += 1


                        pass # If extra_logic is activated do not make the transition

                if debug: print("New allocation: ", new_allocation)

            else:
                current_allocation = get_allocation(dead_zone, current_ranking[0], agent_pos)

            if type(values[agent_pos[0], agent_pos[1]]) == list:
                values[agent_pos[0], agent_pos[1]].append(current_allocation)
            else:
                values[agent_pos[0], agent_pos[1]] = []
                values[agent_pos[0], agent_pos[1]].append(current_allocation)
            #print(agent_pos, current_allocation)
            lastallocation[agent_pos[0]][agent_pos[1]] = current_allocation
            allocations.append(current_allocation) # After every walk add current allocation to list

        if debug: print("Trial " + str(e) + " Mean allocation: " + str(np.mean(allocations)))

        mean_allocations.append(np.mean(allocations))

    for x in range(23):
        for y in range(23):
            heatmap[x][y] = np.mean(values[x][y])

    sum_transitions = override_counter + transition_counter

    print("All encountered transitions: ", transitions_encountered)
    print("Sum of all transitions: ", sum_transitions)

    print("Overridden transitions: ", override_counter)
    print("Completed transitions: ", transition_counter)

    print("Override Percentage: ", np.round(override_counter/transitions_encountered,4))

    print("Mean Allocation: " + str(np.mean(mean_allocations)))
    print("Min Allocation: " + str(np.min(mean_allocations)))
    print("Max Allocation: " + str(np.max(mean_allocations)))
    return mean_allocations, heatmap, lastallocation


# Experiment 1

exp1vals = []
exp1means = []
exp1stds = []
exp1heatmaps = []
exp1lastallocations = []

print("\nNormal Environment / Default Agent: ")
allocs, heatmap, lastallocation = run_experiment(extra_logic=False, dead_zone=False, dead_zone_suppression=False,
                                    num_trials=1000, num_walks=1000, num_steps=10, debug=False)

exp1vals.append(allocs)
exp1means.append(np.mean(allocs))
exp1stds.append(np.std(allocs))
exp1heatmaps.append(heatmap)
exp1lastallocations.append(lastallocation)

print("\nNormal Environment / Agent w Extra Logic: ")
allocs, heatmap, lastallocation = run_experiment(extra_logic=True, dead_zone=False, dead_zone_suppression=False,
                                    num_trials=1000, num_walks=1000, num_steps=10, debug=False)
exp1vals.append(allocs)
exp1means.append(np.mean(allocs))
exp1stds.append(np.std(allocs))
exp1heatmaps.append(heatmap)
exp1lastallocations.append(lastallocation)

# Plots for Experiment 1

df = pd.DataFrame()
df["Scenario 1"] = exp1vals[0]
df["Scenario 2"] = exp1vals[1]

"""
sns.boxplot(data=df, whis=[5,95])
plt.xticks([0,1],["Scenario 1", "Scenario 2"])
plt.title("Mean Allocations for Experiment 1")
plt.savefig('barchart.png', dpi=300)
plt.show()
"""

exp1_stats, pval = stats.ttest_ind(exp1vals[0], exp1vals[1] , axis=0, equal_var=True)
# print("t-value: ", exp1_stats)
# print("p-value: ", pval)

sns.histplot(exp1vals[0], color = "green", bins=50)
sns.histplot(exp1vals[1], color = "skyblue", bins=50)
green_patch = mpatches.Patch(color='green', label='Strongest Signal')
skyblue_patch = mpatches.Patch(color='skyblue', label='Transition Learning')
plt.legend(handles=[green_patch, skyblue_patch])
plt.xlabel("Average Allocation")
plt.ylabel("Number of Rounds")
# plt.savefig('scen1_histogram.png', dpi=300)
plt.show()
plt.close()

sns.heatmap(exp1heatmaps[0], cmap="PuBu", center=6, annot=True)
# plt.savefig("scen1_alloc_default.png", dpi=300)
plt.show()
plt.close()

sns.heatmap(exp1heatmaps[1], cmap="PuBu", center=6, annot=True)
# plt.savefig("scen1_alloc_learned_ave.png", dpi=300)
plt.show()
plt.close()

sns.heatmap(exp1lastallocations[1], cmap="PuBu", center=6, annot=True)
# plt.savefig("scen1_alloc_learned.png", dpi=300)
plt.show()
plt.close()

"""
sns.heatmap(exp1lastallocations[0], annot=True)
plt.savefig("scen1_alloc_default_last.png", dpi=300)
plt.show()
plt.close()
"""


# Experiment 2


exp2vals = []
exp2means = []
exp2stds = []
exp2heatmaps = []
exp2lastallocations = []


print("\nDead Zone Environment / Default Agent: ")
allocs, heatmap, lastallocation = run_experiment(extra_logic=False, dead_zone=True, dead_zone_suppression=False,
                                    num_trials=1000, num_walks=1000, num_steps=10, debug=False)

exp2vals.append(allocs)
exp2means.append(np.mean(allocs))
exp2stds.append(np.std(allocs))
exp2heatmaps.append(heatmap)
exp2lastallocations.append(lastallocation)


print("\nDead Zone Environment / Agent w Extra Logic: ")
allocs, heatmap, lastallocation = run_experiment(extra_logic=True, dead_zone=True, dead_zone_suppression=False,
                                    num_trials=1000, num_walks=1000, num_steps=10, debug=False)

exp2vals.append(allocs)
exp2means.append(np.mean(allocs))
exp2stds.append(np.std(allocs))
exp2heatmaps.append(heatmap)
exp2lastallocations.append(lastallocation)


"""
print("\nDead Zone Environment / Agent w Dead Zone Suppression Logic")
allocs, heatmap, lastallocation = run_experiment(extra_logic=True, dead_zone=True, dead_zone_suppression=True,
                                    num_trials=100, num_walks=5000, num_steps=10, debug=False)


exp2vals.append(allocs)
exp2means.append(np.mean(allocs))
exp2stds.append(np.std(allocs))
exp2heatmaps.append(heatmap)
exp2lastallocations.append(lastallocation)
"""

# Plots for Experiment 2

df = pd.DataFrame()
df["Scenario 1"] = exp2vals[0]
df["Scenario 2"] = exp2vals[1]
# df["Scenario 3"] = exp2vals[2]

"""
sns.boxplot(data=df, whis=[5,95])
plt.xticks([0,1],["Scenario 1", "Scenario 2"])
plt.title("Mean Allocations for Experiment 2")
plt.savefig('dz_barchart.png', dpi=300)
plt.show()
"""

exp2_stats, pval = stats.ttest_ind(exp2vals[0], exp2vals[1] , axis=0, equal_var=True)
# print("t-value: ", exp2_stats)
# print("p-value: ", pval)


sns.histplot(exp2vals[0], color = "green", bins=50)
sns.histplot(exp2vals[1], color = "skyblue", bins=50)
green_patch = mpatches.Patch(color='green', label='Strongest Signal')
skyblue_patch = mpatches.Patch(color='skyblue', label='Transition Learning')
plt.legend(handles=[green_patch, skyblue_patch])
plt.xlabel("Average Allocation")
plt.ylabel("Number of Rounds")
# plt.savefig('scen2_histogram.png', dpi=300)
plt.show()
plt.close()

sns.heatmap(exp2heatmaps[0], cmap="PuBu", annot=True)
# plt.savefig("scen2_alloc_default.png", dpi=300)
plt.show()
plt.close()

sns.heatmap(exp2heatmaps[1], cmap="PuBu", annot=True)
# plt.savefig("scen2_alloc_learned_ave.png", dpi=300)
plt.show()
plt.close()

sns.heatmap(exp2lastallocations[1], cmap="PuBu", annot=True)
# plt.savefig("scen2_alloc_learned.png", dpi=300)
plt.show()
plt.close()

"""
sns.heatmap(exp2lastallocations[0], annot=True)
plt.savefig("scen2_alloc_default_map.png", dpi=300)
plt.show()
plt.close()
"""

"""
sns.heatmap(exp2heatmaps[2], annot=True)
plt.savefig("scen2_heatmap_suppression.png", dpi=300)
plt.show()
plt.close()
"""

"""
sns.heatmap(exp2lastallocations[2], annot=True)
plt.savefig("scen2_allocmap_suppression.png", dpi=300)
plt.show()
plt.close()
"""