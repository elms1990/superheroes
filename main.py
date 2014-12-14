from character import heroes, villains, shared_comics, VillainTeam, HeroTeam
from random import randint

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
def fitness(team):

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


#def crossover(team1, team2):


def createInitialPopulation(size=100, teamsize=10):
    pop = []
    for i in xrange(size):
        teamIds = [heroes.keys()[randint(0, len(heroes)-1)] for j in xrange(teamsize)]
        pop.append(HeroTeam(teamIds))
    return pop

if __name__ == '__main__':
    ## trocar pra ler da entrada
    entryFile = 'V4_763.txt'
    with open('Villan Teams with 763/'+entryFile, 'r') as f:
        villains_team_ids= [int(x) for x in f.read().split(' ')]
    
    villain_team = VillainTeam(villains_team_ids)
    print villain_team

    BUDGET = villain_team.calculateBudget()

    NGEN = 200
    POPSIZE = 200



    

    population = createInitialPopulation(size=POPSIZE, teamsize=villain_team.size())

    for i in xrange(NGEN):
        fits = map(fitness, population)




    # Best individual
    #bestTeam = convertChromosomeToHeroTeam(ga.bestIndividual())  


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







    

