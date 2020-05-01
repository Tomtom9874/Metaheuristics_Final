# the intial framework for a real-valued GA
# author: Charles Nicholson
# for ISE/DSA 5113

# need some python libraries
import math
from random import Random
import numpy as np

# to setup a random number generator, we will specify a "seed" value
seed = 5113
myPRNG = Random(seed)

Schwefel_lower_bound = -500  # bounds for Schwefel Function search space
Schwefel_upper_bound = 500   # bounds for Schwefel Function search space

# you may change anything below this line that you wish too ------------------------------------------------------------

# Student name(s): Tom Welborn, Nik Frost
# Date: 5/1/2020

# parameters moved to main function


# create an continuous valued chromosome
def create_chromosome(d, l_bound, u_bound):
    return [myPRNG.uniform(l_bound, u_bound) for _ in range(d)]


# create initial population
def initialize_population():  # n is size of population; d is dimensions of chromosome
    population = []
    population_fitness = []
    
    for i in range(population_size):
        population.append(create_chromosome(dimensions, Schwefel_lower_bound, Schwefel_upper_bound))
        population_fitness.append(evaluate(population[i]))
        
    temp_zip = zip(population, population_fitness)
    pop_vals = sorted(temp_zip, key=lambda x: x[1])
    
    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  pop_vals[0] is represents the best individual in the population
    # pop_vals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)
    # -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    
    return pop_vals


# implement a linear crossover
def crossover(x1, x2):
    d = len(x1)  # dimensions of solution
    
    # choose crossover point
    # we will choose the smaller of the two [0:cross_over_pt] and [cross_over_pt:d] to be unchanged
    # the other portion be linear combo of the parents
        
    cross_over_pt = myPRNG.randint(1, d-1)  # I choose the crossover point where at least 1 element of parent is copied
    beta = myPRNG.random()  # random number between 0 and 1
        
    # note: using numpy allows us to treat the lists as vectors
    # here we create the linear combination of the solutions
    new1 = list(np.array(x1) - beta*(np.array(x1)-np.array(x2))) 
    new2 = list(np.array(x2) + beta*(np.array(x1)-np.array(x2)))
    
    # the crossover is then performed between the original solutions "x1" and "x2" and the "new1" and "new2" solutions
    if cross_over_pt < d/2:
        offspring1 = x1[0:cross_over_pt] + new1[cross_over_pt:d]  # note the "+" operator concatenates lists
        offspring2 = x2[0:cross_over_pt] + new2[cross_over_pt:d]
    else:
        offspring1 = new1[0:cross_over_pt] + x1[cross_over_pt:d]
        offspring2 = new2[0:cross_over_pt] + x2[cross_over_pt:d]
    return offspring1, offspring2  # two offspring are returned


# function to evaluate the Schwefel Function for d dimensions
def evaluate(x):  
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
    val = 418.9829*d - val
    return val             
  

# function to provide the rank order of fitness values in a list
# not currently used in the algorithm, but provided in case you want to...
def rank_order(any_list):
    rank_ordered = [0] * len(any_list)
    for i, x in enumerate(sorted(range(len(any_list)), key=lambda y: any_list[y])):
        rank_ordered[x] = i
    return rank_ordered


# performs tournament selection; k chromosomes are selected (with repeats allowed)
# and the best advances to the mating pool
# function returns the mating pool with size equal to the initial population
def tournament_selection(pop, k):
    # randomly select k chromosomes; the best joins the mating pool
    mating_pool = []
    
    while len(mating_pool) < population_size:
        ids = [myPRNG.randint(0, population_size - 1) for _ in range(k)]
        competing_individuals = [pop[i][1] for i in ids]
        best_id = ids[competing_individuals.index(min(competing_individuals))]
        mating_pool.append(pop[best_id][0])
    return mating_pool


# function to mutate solutions
def mutate(x):
    # TODO: Implement mutation function
    random_position = myPRNG.randint(0, len(x))
    x[random_position] = myPRNG.uniform(Schwefel_lower_bound, Schwefel_upper_bound)
    return x


def probabilistic_mutate(chromosome):
    mutation_roll = myPRNG.random()
    if mutation_roll < mutation_rate:
        chromosome = probabilistic_mutate(chromosome)
    return chromosome


def breeding(mating_pool):
    # the parents will be the first two individuals, then next two, then next two and so on
    
    children = []
    children_fitness = []
    for i in range(0, population_size - 1, 2):

        # Crossover
        crossover_roll = myPRNG.random()
        if crossover_roll < cross_over_rate:
            child1, child2 = crossover(mating_pool[i], mating_pool[i + 1])
        else:
            child1, child2 = mating_pool[i], mating_pool[i + 1]

        # Mutation (With mutation_rate)
        child1 = probabilistic_mutate(child1)
        child2 = probabilistic_mutate(child2)
        
        children.append(child1)
        children.append(child2)
        
        children_fitness.append(evaluate(child1))
        children_fitness.append(evaluate(child2))
        
    temp_zip = zip(children, children_fitness)
    pop_vals = sorted(temp_zip, key=lambda x: x[1])
        
    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  pop_vals[0] is represents the best individual in the population
    # pop_vals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)
    # -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    return pop_vals


# insertion step
def insert(pop, kids):
    # TODO: Implement elitism-based elimination
    return kids


# perform a simple summary on the population: returns the best chromosome fitness,
# the average population fitness, and the variance of the population fitness
def summary_fitness(pop):
    a = np.array(list(zip(*pop))[1])
    return np.min(a), np.mean(a), np.var(a)


# the best solution should always be the first element... if I coded everything correctly...
def print_best_sol_in_pop(pop):
    print(pop[0])

# TODO: (Optional) Implement Text Output


def genetic_algorithm_search(k=3):
    population = initialize_population()

    for j in range(generations):
        mates = tournament_selection(population, k)
        offspring = breeding(mates)
        population = insert(population, offspring)

        min_val, mean_val, var_val = summary_fitness(population)  # check out the population at each generation
        print(summary_fitness(population))  # print to screen; turn this off for faster results
    print(summary_fitness(population))
    print_best_sol_in_pop(population)


dimensions = 2  # set dimensions for Schwefel Function search space (should either be 2 or 200 for HM #5)
population_size = 6  # size of GA population
generations = 1000  # number of GA generations
cross_over_rate = 0.8
mutation_rate = 0.2


def main():
    # genetic_algorithm_search()
    c = create_chromosome(2, Schwefel_lower_bound, Schwefel_upper_bound)



if __name__ == '__main__':
    main()
