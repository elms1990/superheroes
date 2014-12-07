from character import heroes, villains, shared_comics, VillainTeam, HeroTeam

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import Mutators
from pyevolve import Initializators

BUDGET=0
PENALTY_BUDGET = 1000
PENALTY_SIZE = 1
PENALTY_BEAT = 22
REWARD_BEAT = 0
REWARD_COLLABORATION = 1

villain_team = None

def convertChromosomeToHeroTeam(chromosome):
    #heroIds = [heroes.keys()[idx] for idx in [i for i in xrange(len(chromosome)) if chromosome[i]==1]]
    heroIds = list(set([heroes.keys()[idx] for idx in chromosome]))
    return HeroTeam(heroIds)
# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):

    team = convertChromosomeToHeroTeam(chromosome)

    score = team.getCollaboration(oppositeTeam=villain_team) * REWARD_COLLABORATION

    # if team.getCost() > BUDGET:
    #     score -= (team.getCost() - BUDGET) * PENALTY_BUDGET
    # if team.size() > villain_team.size():
    #     score -= (team.size() - villain_team.size()) * PENALTY_SIZE

    if team.beatsTeam(villain_team):
         score += REWARD_BEAT
    else:
        score -= sum([a-b for a,b in zip(team.getPowerGrid(), villain_team.getPowerGrid())]) * PENALTY_BEAT

    return max(0,score)

if __name__ == '__main__':
    ## trocar pra ler da entrada
    entryFile = 'V4_763.txt'
    with open('Villan Teams with 763/'+entryFile, 'r') as f:
        villains_team_ids= [int(x) for x in f.read().split(' ')]
    
    villain_team = VillainTeam(villains_team_ids)
    print villain_team

    BUDGET = villain_team.calculateBudget()

    # Genome instance
    genome = G1DList.G1DList(villain_team.size())

    genome.setParams(rangemin=0, rangemax=len(heroes.keys())-1)
    
    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)
        # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    #ga.initialize(Initializators.G1DListInitializatorInteger)


    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    print dir(Selectors)
    print dir(ga)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

    ga.setPopulationSize(2000)
    ga.setGenerations(2000)
    ga.setMutationRate(0.02)
    ga.setCrossoverRate(0.9)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=100)

    # Best individual
    bestTeam = convertChromosomeToHeroTeam(ga.bestIndividual())  


    print bestTeam.size(), villain_team.size()
    print bestTeam.beatsTeam(villain_team), bestTeam.getCost() <= BUDGET
    print bestTeam.getPowerGrid(), villain_team.getPowerGrid() 
    print bestTeam.getCollaboration(oppositeTeam=villain_team, pprint=True) 
    print     BUDGET, bestTeam.getCost()
    print bestTeam, villain_team



    ##ALGORITMOS

    #REPR LISTA: fazer crossover com ponto de corte e tratar ids repetidos como vazios
    ## OU lista do tamanho do numero de herois, igual TSP, pega primeiros herois da lista e acha o melhor time

#6087
#captain america, iron man, darkhawk, hercules, jocasta, human torch, angel, spider-man, daredevil, black widow







    

