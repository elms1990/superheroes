from character import heroes, villains, shared_comics, VillainTeam, HeroTeam
from random import randint


import array
import random
import json
import sys

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools


cache_teams = {}

def convertChromosomeToHeroTeam(chromosome):
    #heroIds = tuple(set([heroes.keys()[idx] for idx in chromosome[:villain_team.size()]]))
    heroIds = tuple(set(chromosome))
    if heroIds not in cache_teams:
        cache_teams[heroIds] = HeroTeam(heroIds)
    return cache_teams[heroIds]


# This function is the evaluation function, we want
def fitness(chsTeam):
    team = convertChromosomeToHeroTeam(chsTeam)
    score = team.getCollaboration(oppositeTeam=villain_team) 

    numBeats = team.numBeats(villain_team)
    score += 1000 * numBeats
    
    if team.getCost() <= BUDGET :
        score *= 10

    return  max(0,score),


def cxTeam(ind1, ind2):
    size = min(len(ind1), len(ind2))
    numSwitches = random.randint(1, size-1)
    for i in xrange(numSwitches):
        cxpoint1 = random.randint(0, size - 1)
        cxpoint2 = random.randint(0, size - 1)
        ind1[cxpoint1], ind2[cxpoint1] = ind2[cxpoint2], ind1[cxpoint2]

    return ind1, ind2

def mutTeam(ind):
    size = len(ind)
    for i in xrange(size):
        if random.random() < 1.0 / size:
            #ind[i] = random.randint(0, len(heroes)-1)
            ind[i] = random.choice(heroes.keys())
    return ind,

def selectTeams(individuals, k):
    return  tools.selTournament(individuals, int(0.95*len(individuals)), tournsize=4) + \
            tools.selWorst(individuals, int(0.05*len(individuals)))

def printBestTeamStats(bestTeam):
    print 'Team Size:', bestTeam.size(), ' Villain Team Size:', villain_team.size()
    print 'BeatsTeam?',bestTeam.beatsTeam(villain_team), 'UnderBudget?',bestTeam.getCost() <= BUDGET
    print 'Power Grids:', bestTeam.getPowerGrid(), villain_team.getPowerGrid() 
    print 'Collaboration:', bestTeam.getCollaboration(oppositeTeam=villain_team, pprint=True) 
    print 'Cost:', bestTeam.getCost(), ' BUDGET:', BUDGET
    print bestTeam, ' vs ', villain_team

if __name__ == '__main__':
    if len(sys.argv) > 1:
        entryFile = sys.argv[1]
    else:
        entryFile = 'Villan Teams/V18_763.txt'
    
    with open(entryFile, 'r') as f:
        villains_team_ids= [int(x) for x in f.read().split(' ')]
    
    villain_team = VillainTeam(villains_team_ids)
    BUDGET = villain_team.calculateBudget()
    IND_SIZE = villain_team.size()

    CXPB, MUTPB, NGEN, NPOP, MAXGENNOCHANGE = 0.7, 0.2, 1000, 500, 100

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, heroes.keys(), IND_SIZE)
    #toolbox.register("indices", random.sample, range(len(heroes)), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", cxTeam)
    toolbox.register("mutate", mutTeam)
    #toolbox.register("select", selectTeams)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", fitness)

    pop = toolbox.population(n=NPOP)

    hof = tools.HallOfFame(2)
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    hof.update(pop)
    
    best_collab = 0
    best_ever = convertChromosomeToHeroTeam(hof[0])
    best_not_change = 0
    # Begin the evolution
    for g in range(NGEN):
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values,  
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        #print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        
        hof.update(pop)
        best_ind = hof[0]#tools.selBest(pop, 1)[0]       
        bestTeam = convertChromosomeToHeroTeam(best_ind)
        collab = bestTeam.getCollaboration(oppositeTeam=villain_team)
        cost = bestTeam.getCost()
        beats = bestTeam.beatsTeam(villain_team)

        if beats and cost < BUDGET and collab > best_collab:
            best_ever = bestTeam
            best_not_change = 0
            best_collab = collab
        else:
            best_not_change +=1

        if best_not_change > MAXGENNOCHANGE:
            break



        if g%10 == 0:
            print "-- Generation %i (%s)--  MAX:%i" % (g, len(pop), collab) 
    
    print("-- End of (successful) evolution --")    
    #best_ind = tools.selBest(pop, 1)[0]
    #print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    printBestTeamStats(best_ever)
    







    

