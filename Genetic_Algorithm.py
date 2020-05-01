# the intial framework for a real-valued GA
# author: Charles Nicholson
# for ISE/DSA 5113

# need some python libraries
import math
from random import Random
import numpy as np
from matplotlib import pyplot as plt

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
        population_fitness.append(evaluate(population[i], generations))
        
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
def objective(x):
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
    val = 418.9829*d - val
    return val             
  

def evaluate(x, a=0, b=1):
    return a + objective(x) * b


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
    random_position = myPRNG.randint(0, len(x))
    x[random_position] = myPRNG.uniform(Schwefel_lower_bound, Schwefel_upper_bound)
    return x


def probabilistic_mutate(chromosome):
    mutation_roll = myPRNG.random()
    if mutation_roll < mutation_rate:
        chromosome = probabilistic_mutate(chromosome)
    return chromosome


def breeding(mating_pool, current_generation):
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

        fitness_scale = generations - current_generation
        children_fitness.append(evaluate(child1, a=fitness_scale))
        children_fitness.append(evaluate(child2, a=fitness_scale))
        
    temp_zip = zip(children, children_fitness)
    pop_vals = sorted(temp_zip, key=lambda x: x[1])
        
    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  pop_vals[0] is represents the best individual in the population
    # pop_vals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)
    # -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    return pop_vals


# insertion step (Now elitism based, takes k best parents and population - k best kids)
def insert(pop, kids, debug=False, k=5):
    if debug:
        print("pop:", pop)
        print("kids:", kids)
    pop.sort(key=lambda x: x[1])
    kids.sort(key=lambda x: x[1])
    elite_pop = pop[:k]
    elite_kids = kids[:len(kids) - k]
    elite_pop.extend(elite_kids)
    if debug:
        print("elite:", elite_pop)
    return elite_pop


# perform a simple summary on the population: returns the best chromosome fitness,
# the average population fitness, and the variance of the population fitness
def summary_fitness(pop):
    a = np.array(list(zip(*pop))[1])
    return np.min(a), np.mean(a), np.var(a)


# the best solution should always be the first element... if I coded everything correctly...
def print_best_sol_in_pop(pop):
    sol = pop[0]
    print("Best Chromosome:", sol)
    print("Best Evaluation:", sol[1])


def plot_population(pop):
    x = [p[0][0] for p in pop]
    y = [p[0][1] for p in pop]
    evals = [p[1] for p in pop]
    plt.scatter(x, y, c=evals)
    plt.gray()
    plt.xlim([Schwefel_lower_bound, Schwefel_upper_bound])
    plt.ylim([Schwefel_lower_bound, Schwefel_upper_bound])
    plt.show()


def genetic_algorithm_search(k=3, do_print=False, elite_k=5):
    population = initialize_population()
    #plot_population(population)
    for j in range(generations):
        mates = tournament_selection(population, k)
        offspring = breeding(mates, j)
        population = insert(population, offspring, k=elite_k)
        #plot_population(population)

        min_val, mean_val, var_val = summary_fitness(population)  # check out the population at each generation
        if do_print:
            print("Fitness Summary [ Gen", j, "] Mean:", mean_val, "Min", min_val)
        else:
            if j % 250 == 0:
                print(j, "/", generations)
    print_best_sol_in_pop(population)


#dimensions = 2  # set dimensions for Schwefel Function search space (should either be 2 or 200 for HM #5)
#population_size = 6  # size of GA population
#generations = 1000  # number of GA generations
#cross_over_rate = 0.9
#mutation_rate = 0.2

dimensions = 200  # set dimensions for Schwefel Function search space (should either be 2 or 200 for HM #5)

# Parameters (Best found in parenthesis)
population_size = 300  # size of GA population (300)
generations = 1000  # number of GA generations (1000)
cross_over_rate = 0.9  # (0.9)
mutation_rate = 0.25  # (0.25)


def main():
    genetic_algorithm_search(elite_k=10)
    print("Global Best:", 67734.73069639696)


if __name__ == '__main__':
    main()
