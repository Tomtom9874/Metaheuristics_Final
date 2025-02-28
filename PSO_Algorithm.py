# the intial framework for a particle swarm optimization for Schwefel minimization problem
# author: Charles Nicholson
# for ISE/DSA 5113


# need some python libraries
import math
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
NUM_ITERATIONS = 900        # Number of iterations
PHI_1 = 1.9                 # Local Weight
PHI_2 = 1.9                 # Global Weight
VELOCITY = 25               # Max Velocity
Best solution = 296.1099848292587
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
NUM_DIMENSIONS = 200        # number of dimensions of problem
SWARM_SIZE = 5              # number of particles in swarm
NUM_ITERATIONS = 4000       # Number of iterations
PHI_1 = 0.95                # Local Weight
PHI_2 = 0.95                # Global Weight
VELOCITY = 12                # Max Velocity
VEL_MAX = VELOCITY
VEL_MIN = -VELOCITY
PRINT_EVERY = 100           # Summary output every x iterations


# Each particle is at a certain position and velocity and also holds the best position it has visited
class Particle:
    def __init__(self):
        self.position = [myPRNG.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(NUM_DIMENSIONS)]
        self.velocity = [myPRNG.uniform(-VELOCITY, VELOCITY) for _ in range(NUM_DIMENSIONS)]
        self.p_best = self.position[:]  # Personal best position seen
        self.val_best = evaluate(self.p_best)
        self.n_best = self.p_best[:] # Best position found in neighborhood.
        self.n_best_val = evaluate(self.n_best)
        self.neighbors = None

    # Getters
    def get_n_best(self):
        return self.n_best

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_position(self):
        return self.position

    def get_p_best(self):
        return self.p_best

    def get_value_best(self):
        return self.val_best

    # Setters
    def set_position(self, position, index):
        self.position[index] = position
        if evaluate(self.position) < self.val_best:
            self.p_best = self.position[:]
            self.val_best = evaluate(self.p_best)
        if evaluate(self.position) < self.n_best_val:
            self.n_best = self.p_best
            self.n_best_val = self.val_best

    # Updates the particles velocity based on either best neighbor or global best.
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

    # Updates position based on velocity while remaining in bounds
    def update_position(self):
        for d in range(NUM_DIMENSIONS):
            new_position = self.position[d] + self.velocity[d]
            if new_position > UPPER_BOUND or new_position < LOWER_BOUND:
                self.set_position(self.position[d] - self.velocity[d], d)
            else:
                self.set_position(new_position, d)

    def meet_neighbors(self):
        # Gets the lowest evaluation of all the neighbors.
        neighbor_positions = [p.get_n_best() for p in self.neighbors]
        n_best = min(neighbor_positions, key=lambda x: evaluate(x))
        if evaluate(n_best) < self.n_best_val:
            self.n_best = n_best
            self.n_best_val = evaluate(n_best)



# This Holds all of the particles
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
                self.g_best = p.get_p_best()
                self.g_best_val = p.get_value_best()

    def plot_positions(self, generation):
        x = [i.get_position()[0] for i in self.particles]
        y = [i.get_position()[1] for i in self.particles]
        plt.scatter(x, y)
        plt.title(str(generation) + " Generation")
        plt.xlabel("x Coordinate")
        plt.ylabel("y Coordinate")
        #plt.show()

    def optimize(self):
        self.plot_positions(t)

    def global_optimize(self):
        plot_positions(t)
        
    # Optimizes based on a global best
    def global_optimize(self):
        self.plot_positions(0)

        for t in range(NUM_ITERATIONS):
            if t % PRINT_EVERY == 0:
                self.print_update(t)
            # update velocities and positions of all particles
            for particle in self.particles:
                particle.update_position()
                particle.update_velocity(self.g_best)
            self.set_global_p_best()
            #self.plot_positions(t)
            # plot_positions(t)
            # self.plot_positions(t)
        self.print_final_update()

    # Optimizes with knowledge from neighbors
    def neighbor_optimize(self):
        # Set Neighbors
        self.particles[-1].set_neighbors([self.particles[0]])
        for p in range(len(self.particles) - 1):
            self.particles[p].set_neighbors([self.particles[p + 1]])
        for p in self.particles:
            p.meet_neighbors()

        for t in range(NUM_ITERATIONS):
            if t % PRINT_EVERY == 0:
                self.print_update(t)
            for particle in self.particles:
                particle.update_position()
                particle.update_velocity(particle.get_n_best())  # Uses neighboring best instead of global.
                particle.meet_neighbors()
            self.set_global_p_best()
        self.print_final_update()

    # Prints Ending summary
    def print_final_update(self):
        print("\nFinal number of solutions checked: ", NUM_ITERATIONS * SWARM_SIZE)
        print("Best value found: ", self.g_best_val)
        print("Best position: ", self.g_best)

    # Prints Summary up to given generation
    def print_update(self, t):
        print(t, "/", NUM_ITERATIONS)
        print("\nTotal number of solutions checked: ", t * SWARM_SIZE)
        print("Best value found so far: ", self.g_best_val)
        print("Best position found so far: ", self.g_best)


# Schwefel function to evaluate a real-valued solution x
def evaluate(x):          
    val = 0
    for d in range(NUM_DIMENSIONS):
        val = val + x[d]*math.sin(math.sqrt(abs(x[d])))
    val = 418.9829 * NUM_DIMENSIONS - val
    return val


def main():
    swarm = Swarm()
    #warm.global_optimize()  # Calls PSO with global best
    #swarm.global_optimize()  # Calls PSO with global best
    swarm.neighbor_optimize()  # Calls PSO with Neighbor best


if __name__ == '__main__':
    main()
