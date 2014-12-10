from character import heroes, villains, shared_comics, VillainTeam, HeroTeam
from random import randint


import array
import random
import json

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools



def convertChromosomeToHeroTeam(chromosome):
    #heroIds = [heroes.keys()[idx] for idx in [i for i in xrange(len(chromosome)) if chromosome[i]==1]]
    heroIds = list(set([heroes.keys()[idx] for idx in chromosome[:villain_team.size()]]))
    return HeroTeam(heroIds)


# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def fitness(team):
    #print 'fitness TEAM', team

    team = convertChromosomeToHeroTeam(team)

    #print team

    score = team.getCollaboration(oppositeTeam=villain_team)
    # if team.getCost() > BUDGET:
    #     score -= (team.getCost() - BUDGET) * PENALTY_BUDGET
    # if team.size() > villain_team.size():
    #     score -= (team.size() - villain_team.size()) * PENALTY_SIZE
    cost = max(0, team.getCost() - BUDGET)
    numBeats = sum([a<b for a,b in zip(team.getPowerGrid(), villain_team.getPowerGrid())])

    return cost, numBeats, score



if __name__ == '__main__':
    ## trocar pra ler da entrada
    entryFile = 'V4_763.txt'
    with open('Villan Teams with 763/'+entryFile, 'r') as f:
        villains_team_ids= [int(x) for x in f.read().split(' ')]
    
    villain_team = VillainTeam(villains_team_ids)
    print villain_team

    BUDGET = villain_team.calculateBudget()

    IND_SIZE = villain_team.size()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, 1.0))
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, indpb=0.1, low=0, up=len(heroes)-1)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("evaluate", fitness)


    #random.seed(48)

    pop = toolbox.population(n=500)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=1000, stats=stats, 
                        halloffame=hof)

    print fitness(hof[0])

    bestTeam = convertChromosomeToHeroTeam(hof[0])

    print bestTeam.size(), villain_team.size()
    print bestTeam.beatsTeam(villain_team), bestTeam.getCost() <= BUDGET
    print bestTeam.getPowerGrid(), villain_team.getPowerGrid() 
    print bestTeam.getCollaboration(oppositeTeam=villain_team) 
    print BUDGET, bestTeam.getCost()
    print bestTeam, villain_team
    ##ALGORITMOS

    #REPR LISTA: fazer crossover com ponto de corte e tratar ids repetidos como vazios
    ## OU lista do tamanho do numero de herois, igual TSP, pega primeiros herois da lista e acha o melhor time

#6087
#captain america, iron man, darkhawk, hercules, jocasta, human torch, angel, spider-man, daredevil, black widow







    

