from itertools import combinations,product

heroes = {}
villains = {}
shared_comics = {}
budget = 0

class Character():
    def __init__(self, array):
        self.id = int(array[0])
        self.name = array[1]
        self.hero = array[2] == 'hero'
        if self.hero:
            heroes[self.id] = self
        else:
            villains[self.id] = self
        self.intelligence = int(array[3])
        self.strength = int(array[4])
        self.speed = int(array[5])
        self.durability = int(array[6])
        self.energy = int(array[7])
        self.fighting = int(array[8])
        self.numComics = int(array[9])
    
    def __str__(self):
        return str({'id': self.id, 'name': self.name, 'hero': self.hero, 'intelligence': self.intelligence,
                'strength': self.strength, 'speed': self.speed, 'durability': self.durability, 
                'energy':self.energy, 'fighting': self.fighting, 'numComics': self.numComics})

    def getPowerGrid(self):
        return [self.intelligence, self.strength, self.speed, self.durability, self.energy, self.fighting]

    def getCost(self):
        return self.averagePowerGrid() * self.numComics

    def averagePowerGrid(self):
        pg = self.getPowerGrid()
        return sum(pg)/len(pg)

    def sharedComicsWithCharacter(self, c):
        k = (min(self.id,c.id),max(self.id,c.id))
        return shared_comics[k] if k in shared_comics else 0


class Team():
    def __init__(self, memberIds, dic):
        self.members = [dic[x] for x in memberIds]

    def __str__(self):
        return ', '.join([x.name for x in self.members])

    def __iter__(self):
        return iter(self.members)

    def size(self):
        return len(self.members)

    def averagePowerGrid(self):
        g = [x.averagePowerGrid() for x in self]
        return 1.0* sum(g)/len(g)

    def getPowerGrid(self):
       return [1.0* sum(attr)/len(attr) for attr in zip(*[m.getPowerGrid() for m in self])]

    def averagePopularity(self):
        p = [x.numComics for x in self.members]
        return 1.0* sum(p)/len(p)

    def beatsTeam(self, team):
        return all([a >= b for a,b in zip(self.getPowerGrid(),team.getPowerGrid())])

    def getCost(self):
        return sum([x.getCost() for x in self.members])

    def getCollaboration(self,oppositeTeam=[]):
        #collaboration among team + collaboration with opposite team ## EH ISSO MESMO QUE O PROF PASSOU?
        return sum([x.sharedComicsWithCharacter(y) for x,y in combinations(self,2)]) + \
               sum([x.sharedComicsWithCharacter(y) for x,y in product(self, oppositeTeam)])

class HeroTeam(Team):
    def __init__(self, memberIds):
        Team.__init__(self, memberIds, heroes)

class VillainTeam(Team):
    def __init__(self, memberIds):
        Team.__init__(self, memberIds, villains)
    
    def calculateBudget(self):
        allHeroes = HeroTeam([h for h in heroes])
        allVillains = VillainTeam([v for v in villains])

        avgHeroPG = allHeroes.averagePowerGrid()
        avgVillainTeamPG = self.averagePowerGrid()
        avgHeroPopularity = allHeroes.averagePopularity()
        avgVillainTeamPopularity = self.averagePopularity()
        
        #exp1
        ratioPG = avgHeroPG/avgVillainTeamPG
        radioPop = avgHeroPopularity/ avgVillainTeamPopularity
        exp1 = ratioPG * radioPop * self.getCost()

        #exp2
        factor = avgVillainTeamPG/allVillains.averagePowerGrid()
        exp2 =  factor * avgHeroPG * avgHeroPopularity * self.size()

        return max(exp1, exp2)



#read data
with open('marvel_character - victorfc.csv', 'r') as f:
    map(lambda x: Character(x), (y.split(',') for y in f.readlines()[1:]))

with open('shared_comic_books - victorfc.csv') as f:
    for x in ((y.split(',') for y in f.readlines()[1:])):
        shared_comics[(min(int(x[0]), int(x[1])), max(int(x[0]),int(x[1])))] = int(x[2])






