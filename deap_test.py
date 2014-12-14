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
    #heroIds = [heroes.keys()[idx] for idx in [i for i in xrange(len(chromosome)) if chromosome[i]==1]]
    heroIds = tuple(set([heroes.keys()[idx] for idx in chromosome[:villain_team.size()]]))
    if heroIds not in cache_teams:
        cache_teams[heroIds] = HeroTeam(heroIds)
    return cache_teams[heroIds]


# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def fitness(chsTeam):
    team = convertChromosomeToHeroTeam(chsTeam)

    score = 100*team.getCollaboration(oppositeTeam=villain_team)    
    #if team.getCost() <= BUDGET:
    #     score += 10000

    numBeats = sum([a>=b for a,b in zip(team.getPowerGrid(), villain_team.getPowerGrid())])
    score += 10000 * numBeats

    #else:
    #    score -= 10000 
    #if team.beatsTeam(villain_team):
    #    score += 10000 
    # if team.size() > villain_team.size():
    #     score -= (team.size() - villain_team.size()) * PENALTY_SIZE
    
    #cost = 1000 * max(0, team.getCost() - BUDGET)
    #score += numBeats * 10000
    cost=0

    return  max(0,score), cost



def cxTeam(ind1, ind2):
   # print ind1, ind2
    fullTeam = ind1 + ind2
    
    size = len(fullTeam)/2
    ind1[:] = [fullTeam.pop(randint(0, len(fullTeam)-1)) for i in xrange(size)]
    ind2[:] = fullTeam

    return ind1, ind2

    size = min(len(ind1), len(ind2))
    cxpoint = random.randint(1, size - 1)
    ind1[cxpoint:], ind2[cxpoint:] = ind2[cxpoint:], ind1[cxpoint:]
    
    return ind1, ind2

def printBestTeamStats(bestTeam):
    print bestTeam.size(), villain_team.size()
    print bestTeam.beatsTeam(villain_team), bestTeam.getCost() <= BUDGET
    print bestTeam.getPowerGrid(), villain_team.getPowerGrid() 
    print bestTeam.getCollaboration(oppositeTeam=villain_team) 
    print BUDGET, bestTeam.getCost()
    print bestTeam, villain_team

if __name__ == '__main__':
    ## trocar pra ler da entrada
    print sys.argv
    if len(sys.argv) > 1:
        entryFile = sys.argv[1]
    else:
        entryFile = 'Villan Teams with 763/V20_763.txt'
    with open(entryFile, 'r') as f:
        villains_team_ids= [int(x) for x in f.read().split(' ')]
    
    villain_team = VillainTeam(villains_team_ids)
    print villain_team

    BUDGET = villain_team.calculateBudget()

    IND_SIZE = villain_team.size()

    creator.create("FitnessMax", base.Fitness, weights=(1.0, -1.0))
    #creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxOnePoint)
    #toolbox.register("mate", cxTeam)
    toolbox.register("mutate", tools.mutUniformInt, indpb=0.1, low=0, up=len(heroes)-1)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", fitness)


    #random.seed(48)
    CXPB, MUTPB, NGEN, NPOP = 0.5, 0.5, 500, 400

    pop = toolbox.population(n=NPOP)

    #hof = tools.HallOfFame(1)
    #stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("avg", numpy.mean)
    #stats.register("std", numpy.std)
    #stats.register("min", numpy.min)
    #stats.register("max", numpy.max)
    
    #algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=stats, 
    #                halloffame=hof)

    #print fitness(hof[0])
    #bestTeam = convertChromosomeToHeroTeam(hof[0])
    #printBestTeamStats(bestTeam)
    #exit()
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    
    last_fits = [0] * 50
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
                del child1.fitness.values
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
        
        
        last_fits.pop(0)
        last_fits.append(max(fits))
        if len(set(last_fits)) == 1:
            break
            #pass

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        if g%10 == 0:
            print"-- Generation %i (%s)--  MAX:%i" % (g, len(invalid_ind), max(fits))
        #print("  Min %s | Max%s | Avg:%s" % (min(fits), max(fits), mean))
        #print("  Max %s" % max(fits))
        #print("  Avg %s" % mean)
        #print("  Std %s" % std)
    
    print("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


    bestTeam = convertChromosomeToHeroTeam(best_ind)
    printBestTeamStats(bestTeam)
    
    ##ALGORITMOS

    #REPR LISTA: fazer crossover com ponto de corte e tratar ids repetidos como vazios
    ## OU lista do tamanho do numero de herois, igual TSP, pega primeiros herois da lista e acha o melhor time

#6087
#captain america, iron man, darkhawk, hercules, jocasta, human torch, angel, spider-man, daredevil, black widow







    

