# the intial framework for a particle swarm optimization for Schwefel minimization problem
# author: Charles Nicholson
# for ISE/DSA 5113


# need some python libraries
import math
import copy
from random import Random
from matplotlib import pyplot as plt


# to setup a random number generator, we will specify a "seed" value
seed = 12345  # (12345)
myPRNG = Random(seed)

# to get a random number between 0 and 1, write call this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

lowerBound = -500  # bounds for Schwefel Function search space
upperBound = 500   # bounds for Schwefel Function search space

# you may change anything below this line that you wish too -----------------------------------------------------

# Parameters
num_dimensions = 2      # number of dimensions of problem
swarmSize = 5         # number of particles in swarm
T = 1                # Number of iterations
phi1 = .5              # Local Weight
phi2 = 0.1              # Global Weight
VELOCITY = 5
VEL_MAX = VELOCITY
VEL_MIN = -VELOCITY
# Best Solution=80759.249764k


# Schwefel function to evaluate a real-valued solution x
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
def evaluate(x):          
    val = 0
    for d in range(num_dimensions):
        val = val + x[d]*math.sin(math.sqrt(abs(x[d])))
    val = 418.9829*num_dimensions - val
    return val
      

# the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in range(swarmSize)]        # position of particles -- will be a list of lists; e.g.,
vel = [[] for _ in range(swarmSize)]        # velocity of particles -- will be a list of lists

curValue = []   # evaluation value of current position  -- will be a list of real values;
pbest = []      # particles' best historical position -- will be a list of lists
pbestVal = []   # value of pbest position  -- will be a list of real values


# initialize the swarm randomly
for i in range(swarmSize):
    for j in range(num_dimensions):
        pos[i].append(myPRNG.uniform(lowerBound, upperBound))   # assign random value between lower and upper bounds
        vel[i].append(myPRNG.uniform(-VELOCITY, VELOCITY))
    curValue.append(evaluate(pos[i]))                           # evaluate the current position
                                                 
pbest = copy.deepcopy(pos)                                                  # initialize pbest to the starting position
pbestVal = copy.deepcopy(curValue)                                          # initialize pbest to the starting position


# calculates a new velocity for all particles of the swarm
# returns a new list of lists for velocities
def update_vel():
    r1 = myPRNG.random()
    r2 = myPRNG.random()
    # update the velocity
    for particle in range(swarmSize):
        for d in range(num_dimensions):
            # We need to assign the velocity by dimension rather than the whole thing at once.
            local_distance = pbest[particle][d] - pos[particle][d]  # Distance from personal best position
            global_distance = p_best_g[d] - pos[particle][d]  # Distance from global best position
            vel_new = vel[particle][d] + phi1 * r1 * local_distance + phi2 * r2 * global_distance
            # Make sure each updated velocity is within the MIN & MAX bounds
            if vel_new < VEL_MIN:
                vel[particle][d] = VEL_MIN
            elif vel_new > VEL_MAX:
                vel[particle][d] = VEL_MAX
            else:
                vel[particle][d] = vel_new


# updates the positions of all particles and returns a list of lists  
def update_pos():
    for particle in range(swarmSize):
        for d in range(num_dimensions):
            new_position = pos[particle][d] + vel[particle][d]
            if new_position > upperBound:
                pos[particle][d] = pos[particle][d] - vel[particle][d]
            elif new_position < lowerBound:
                pos[particle][d] = pos[particle][d] - vel[particle][d]
            else:
                pos[particle][d] = new_position


def plot_positions(generation):
    x = [i[0] for i in pos]
    y = [i[1] for i in pos]
    plt.scatter(x, y)
    plt.title(str(generation) + " Generation")
    plt.xlabel("x Coordinate")
    plt.ylabel("y Coordinate")
    plt.show()

# Find the global best position
def set_global_p_best(p_best):
    for particle in range(swarmSize):
        if pbestVal[particle] < evaluate(p_best):
            p_best = pbest[particle]
    return p_best


t = 0
p_best_g = copy.deepcopy(pbest[0])
p_best_g = set_global_p_best(p_best_g)
#plot_positions(t)
while t < T:
    if t % 1000 == 0:
        print(t, "/", T)
        print("\nTotal number of solutions checked: ", t * swarmSize)
        print("Best value found so far: ", evaluate(p_best_g))
        print("Best position found so far: ", p_best_g)

    for ant in range(swarmSize):
        curValue[ant] = evaluate(pos[ant])
        # need to assert that the position is within the feasible region
        # before adding it to the pbest list
        if curValue[ant] < pbestVal[ant]:
            pbest[ant] = pos[ant]
            pbestVal[ant] = curValue[ant]

    # update velocities and positions of all particles
    update_vel()
    update_pos()
    p_best_g = set_global_p_best(p_best_g)

    t += 1
    #plot_positions(t)



print("\nFinal number of solutions checked: ", t * swarmSize)
print("Best value found: ", evaluate(p_best_g))
print("Best position: ", p_best_g)
