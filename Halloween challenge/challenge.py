from itertools import product
from functools import reduce
from random import random, randint, shuffle, seed
import numpy as np
from scipy import sparse
from copy import copy

def make_set_covering_problem(num_points, num_sets, density):
    """Returns a sparse array where rows are sets and columns are the covered items"""
    seed(num_points*2654435761+num_sets+density)
    sets = sparse.lil_array((num_sets, num_points), dtype=bool)
    for s, p in product(range(num_sets), range(num_points)):
        if random() < density:
            sets[s, p] = True
    for p in range(num_points):
        sets[randint(0, num_sets-1), p] = True
    return sets.toarray()

def fitness(state, problem_size, sets):
    cost = sum(state)
    valid = np.sum(
        reduce(
            np.logical_or,
            [sets[i] for i, t in enumerate(state) if t],
            np.array([False for _ in range(problem_size)]),
        )
    )
    return valid, -cost

def tweak(state, problem_size):
    new_state = copy(state)
    index = randint(0, problem_size - 1)
    new_state[index] = not new_state[index]
    return new_state
    
PROBLEM_SIZE = [100, 1000, 5000]
DENSITY = [0.3, 0.7]

for size, density in product(PROBLEM_SIZE, DENSITY):
    state = [False for _ in range(size)]
    print(f"Problem size: {size}, Number of sets: {size}, density: {density}")
    SETS = make_set_covering_problem(size, size, density)
    step_counter = 0
    for step in range(10000):
        new_state = tweak(state, size)
        if fitness(new_state, size, SETS) >= fitness(state, size, SETS):
            step_counter+=1
            state = new_state
    print(f"Solution: {fitness(state, size, SETS)} in {step_counter} steps")
    