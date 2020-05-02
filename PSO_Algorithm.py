# the intial framework for a particle swarm optimization for Schwefel minimization problem
# author: Charles Nicholson
# for ISE/DSA 5113


# need some python libraries
import copy
import math
import numpy as np
from random import Random


# to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

# to get a random number between 0 and 1, write call this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

lowerBound = -500  # bounds for Schwefel Function search space
upperBound = 500   # bounds for Schwefel Function search space

# you may change anything below this line that you wish too -----------------------------------------------------

# note: for the more experienced Python programmers, you might want to consider taking a
# more object-oriented approach to the PSO implementation, i.e.:
# a particle class with methods to initialize itself, and update its own velocity and position;
# a swarm class with a method to iterates through all particles to call update functions, etc.

# Parameters
num_dimensions = 2      # number of dimensions of problem
swarmSize = 10          # number of particles in swarm
T = 500                 # Number of iterations
phi1 = 0.1              # how large or small should this constant be?
phi2 = 0.1              # how large or small should this constant be?
VEL_MAX = 20           # what's a good max velocity?
VEL_MIN = -20          # what's a good min velocity?

      
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
                                            # for a 2D problem with 3 particles: [[17,4],[-100,2],[87,-1.2]]

vel = [[] for _ in range(swarmSize)]        # velocity of particles -- will be a list of lists similar to the "pos" object
                                            # note: pos[0] and vel[0] provides the position and velocity of particle 0;
                                            # pos[1] and vel[1] provides the position and velocity of particle 1; and so on.


curValue = []   # evaluation value of current position  -- will be a list of real values;
                # curValue[0] provides the evaluation of particle 0 in it's current position
pbest = []      # particles' best historical position -- will be a list of lists: pbest[0] provides the position of particle 0's best historical position
pbestVal = []   # value of pbest position  -- will be a list of real values: pbestBal[0] provides the value of particle 0's pbest location


# initialize the swarm randomly
for i in range(swarmSize):
    for j in range(num_dimensions):
        pos[i].append(myPRNG.uniform(lowerBound, upperBound))   # assign random value between lower and upper bounds
        vel[i].append(myPRNG.uniform(-1, 1))                    # assign random value between -1 and 1 --- maybe these are good bounds?  maybe not...
        
    curValue.append(evaluate(pos[i]))                           # evaluate the current position
                                                 
pbest = pos[:]                                                  # initialize pbest to the starting position
pbestVal = curValue[:]                                          # initialize pbest to the starting position

                                                                           
# Currently missing several elements
# e.g., velocity update function; velocity max limitations; position updates; dealing with infeasible space;
# identifying the global best; main loop, stopping criterion, etc.

pbestg = pbest[0]


# calculates a new velocity for all particles of the swarm
# returns a new list of lists for velocities
def update_vel():
    r1 = myPRNG.random()
    r2 = myPRNG.random()
    # update the velocity
    for ant in range(swarmSize):
        for d in range(num_dimensions):
            # We need to assign the velocity by dimension rather than the whole thing at once.
            local_distance = pbest[ant][d] - pos[ant][d]  # Distance from personal best position
            global_distance = pbestg[d] - pos[ant][d]  # Distance from global best position
            vel_new = vel[ant][d] + phi1 * r1 * local_distance + phi2 * r2 * global_distance
            #print("Local best - current", local_distance, "Global best - current", global_distance)
            #print(vel_new)
            #print(pos[ant])
            # Make sure each updated velocity is within the MIN & MAX bounds
            if vel_new < VEL_MIN:
                vel[ant][d] = VEL_MIN
            elif vel_new > VEL_MAX:
                vel[ant][d] = VEL_MAX
            else:
                vel[ant][d] = vel_new


# updates the positions of all particles and returns a list of lists  
def update_pos():
    for ant in range(swarmSize):
        for d in range(num_dimensions):
            new_position = pos[ant][d] + vel[ant][d]
            if new_position < lowerBound:
                pos[ant][d] = lowerBound
            elif new_position > upperBound:
                pos[ant][d] = upperBound
            else:
                pos[ant][d] = new_position


# Find the global best position
def find_global_p_best():
    return_p = pbestg
    for ant in range(swarmSize):
        # decreasing to 0
        if evaluate(pbestg) > 0:
            if pbestVal[ant] < evaluate(pbestg):
                return_p = pbest[ant]
        # increasing to 0
        else:
            if evaluate(pbestg) > evaluate(pbestg):
                return_p = pbest[ant]
    return return_p


# Main loop
def particle_swarm_optimization():
    t = 0
    while t < T:  
        for ant in range(swarmSize):
            curValue[ant] = evaluate(pos[ant])
            # for negative values we need to increase towards 0
            if pbestVal[ant] > 0:
                if curValue[ant] < pbestVal[ant]:
                    pbestVal[ant] = curValue[ant]
                    pbest[ant] = pos[ant]
            # for positive values we need to increase towards 0
            else:
                if curValue[ant] > pbestVal[ant]:
                    pbestVal[ant] = curValue[ant]
                    pbest[ant] = pos[ant]

        # update velocities and positions of all particles
        update_vel()
        update_pos()
        t += 1
        print("\nTotal number of solutions checked: ", t)
        print("Best value found so far: ", evaluate(pbestg))
        print("Best position found so far: ", find_global_p_best())

    print("\nFinal number of solutions checked: ", t)
    print("Best value found: ", evaluate(find_global_p_best()))
    print("Best position: ", pbestg)


def main():
    particle_swarm_optimization()


if __name__ == '__main__':
    main()


