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

LOWER_BOUND = -500  # bounds for Schwefel Function search space
UPPER_BOUND = 500   # bounds for Schwefel Function search space

# you may change anything below this line that you wish too -----------------------------------------------------

# Parameters
NUM_DIMENSIONS = 2      # number of dimensions of problem
SWARM_SIZE = 5         # number of particles in swarm
NUM_ITERATIONS = 1                # Number of iterations
PHI_1 = .5              # Local Weight
PHI_2 = 0.1              # Global Weight
VELOCITY = 5
VEL_MAX = VELOCITY
VEL_MIN = -VELOCITY
# Best Solution=80759.249764k


class Particle:
    def __init__(self):
        self.pos = [myPRNG.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(NUM_DIMENSIONS)]
        self.vel = [myPRNG.uniform(-VELOCITY, VELOCITY) for _ in range(NUM_DIMENSIONS)]
        self.p_best = self.pos[:]
        self.val_best = evaluate(self.p_best)

    def get_pos(self):
        return self.pos

    def set_pos(self, position):
        self.pos = position[:]
        if evaluate(self.pos) < self.val_best:
            self.p_best = position[:]
            self.val_best = evaluate(self.p_best)

    def update_velocity(self):
        r1 = myPRNG.random()
        r2 = myPRNG.random()
        for d in range(NUM_DIMENSIONS):
            # We need to assign the velocity by dimension rather than the whole thing at once.
            local_distance = self.p_best[d] - self.pos[d]  # Distance from personal best position
            global_distance = p_best_g[d] - self.pos[d]  # Distance from global best position
            vel_new = self.vel[d] + PHI_1 * r1 * local_distance + PHI_2 * r2 * global_distance
            # Make sure each updated velocity is within the MIN & MAX bounds
            if vel_new < VEL_MIN:
                self.vel[d] = VEL_MIN
            elif vel_new > VEL_MAX:
                self.vel[d] = VEL_MAX
            else:
                self.vel[d] = vel_new

    def update_position(self):
        for d in range(NUM_DIMENSIONS):
            new_position = self.pos[d] + self.vel[d]
            if new_position > UPPER_BOUND or new_position < LOWER_BOUND:
                self.set_pos(self.pos[d] + self.vel[d])
            else:
                self.set_pos(new_position)


# Schwefel function to evaluate a real-valued solution x
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
def evaluate(x):          
    val = 0
    for d in range(NUM_DIMENSIONS):
        val = val + x[d]*math.sin(math.sqrt(abs(x[d])))
    val = 418.9829 * NUM_DIMENSIONS - val
    return val


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
    for particle in range(SWARM_SIZE):
        if pbestVal[particle] < evaluate(p_best):
            p_best = pbest[particle]
    return p_best


t = 0
p_best_g = copy.deepcopy(pbest[0])
p_best_g = set_global_p_best(p_best_g)
#plot_positions(t)
while t < NUM_ITERATIONS:
    if t % 1000 == 0:
        print(t, "/", NUM_ITERATIONS)
        print("\nTotal number of solutions checked: ", t * SWARM_SIZE)
        print("Best value found so far: ", evaluate(p_best_g))
        print("Best position found so far: ", p_best_g)

    for ant in range(SWARM_SIZE):
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



print("\nFinal number of solutions checked: ", t * SWARM_SIZE)
print("Best value found: ", evaluate(p_best_g))
print("Best position: ", p_best_g)
