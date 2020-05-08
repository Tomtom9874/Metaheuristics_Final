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
"""
Best Parameters (2D)
SWARM_SIZE = 5              # number of particles in swarm
NUM_ITERATIONS = 1300       # Number of iterations
PHI_1 = 1.75                 # Local Weight
PHI_2 = 1.75                 # Global Weight
VELOCITY = 0.8               # Max Velocity
Best solution = 296.10673923214495
-----------------------------------------------------------
Best Parameters (200D)
SWARM_SIZE =  10            # number of particles in swarm
NUM_ITERATIONS = 500        # Number of iterations
PHI_1 = 0.8                 # Local Weight
PHI_2 = 0.8                 # Global Weight
VELOCITY = 10               # Max Velocity
Best solution = 56,0119.57720359191
"""

# Parameters
NUM_DIMENSIONS = 2          # number of dimensions of problem
SWARM_SIZE = 5              # number of particles in swarm
NUM_ITERATIONS = 1800       # Number of iterations
PHI_1 = 1.75                 # Local Weight
PHI_2 = 0.1                 # Global Weight
VELOCITY = 0.8              # Max Velocity
VEL_MAX = VELOCITY
VEL_MIN = -VELOCITY
PRINT_EVERY = 100           # Summary output every x iterations


class Particle:
    def __init__(self):
        self.position = [myPRNG.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(NUM_DIMENSIONS)]
        self.velocity = [myPRNG.uniform(-VELOCITY, VELOCITY) for _ in range(NUM_DIMENSIONS)]
        self.p_best = self.position[:]
        self.val_best = evaluate(self.p_best)

    def get_position(self):
        return self.position

    def get_value_best(self):
        return self.val_best

    def set_position(self, position, index):
        self.position[index] = position
        if evaluate(self.position) < self.val_best:
            self.p_best = self.position[:]
            self.val_best = evaluate(self.p_best)

    def update_velocity(self, global_best):
        r1 = myPRNG.random()
        r2 = myPRNG.random()
        for d in range(NUM_DIMENSIONS):
            # We need to assign the velocity by dimension rather than the whole thing at once.
            local_distance = self.p_best[d] - self.position[d]  # Distance from personal best position
            global_distance = global_best[d] - self.position[d]  # Distance from global best position
            vel_new = self.velocity[d] + PHI_1 * r1 * local_distance + PHI_2 * r2 * global_distance
            # Make sure each updated velocity is within the MIN & MAX bounds
            if vel_new < VEL_MIN:
                self.velocity[d] = VEL_MIN
            elif vel_new > VEL_MAX:
                self.velocity[d] = VEL_MAX
            else:
                self.velocity[d] = vel_new

    def update_position(self):
        for d in range(NUM_DIMENSIONS):
            new_position = self.position[d] + self.velocity[d]
            if new_position > UPPER_BOUND or new_position < LOWER_BOUND:
                self.set_position(self.position[d] - self.velocity[d], d)
            else:
                self.set_position(new_position, d)


class Swarm:
    def __init__(self):
        self.particles = [Particle() for _ in range(SWARM_SIZE)]
        self.g_best = None
        self.g_best_val = float("inf")
        self.set_global_p_best()

    # Find the global best position
    def set_global_p_best(self):
        for p in self.particles:
            if p.get_value_best() < self.g_best_val:
                self.g_best = p.get_position()
                self.g_best_val = p.get_value_best()

    def plot_positions(self, generation):
        x = [i.get_position()[0] for i in self.particles]
        y = [i.get_position()[1] for i in self.particles]
        plt.scatter(x, y)
        plt.title(str(generation) + " Generation")
        plt.xlabel("x Coordinate")
        plt.ylabel("y Coordinate")
        plt.show()

    def optimize(self):
        #self.plot_positions(t)
        for t in range(NUM_ITERATIONS):
            if t % PRINT_EVERY == 0:
                print(t, "/", NUM_ITERATIONS)
                print("\nTotal number of solutions checked: ", t * SWARM_SIZE)
                print("Best value found so far: ", self.g_best_val)
                print("Best position found so far: ", self.g_best)

            # update velocities and positions of all particles
            for particle in self.particles:
                particle.update_position()
                particle.update_velocity(self.g_best)
            self.set_global_p_best()

            #self.plot_positions(t)
        print("\nFinal number of solutions checked: ", NUM_ITERATIONS * SWARM_SIZE)
        print("Best value found: ", self.g_best_val)
        print("Best position: ", self.g_best)


# Schwefel function to evaluate a real-valued solution x
def evaluate(x):          
    val = 0
    for d in range(NUM_DIMENSIONS):
        val = val + x[d]*math.sin(math.sqrt(abs(x[d])))
    val = 418.9829 * NUM_DIMENSIONS - val
    return val


def main():
    swarm = Swarm()
    swarm.optimize()


if __name__ == '__main__':
    main()
