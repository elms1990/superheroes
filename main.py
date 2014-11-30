from character import heroes, villains, shared_comics, VillainTeam, HeroTeam




if __name__ == '__main__':
	## trocar pra ler da entrada
	entry = '763 627 577 558 749 438 624 716 607 711'
	villains_team = [int(x) for x in entry.split(' ')]
	
	v = VillainTeam(villains_team)
	h = HeroTeam([4,5,6,23,21,2,78,70,54])

	print h.beatsTeam(v)
	print v.calculateBudget()
	print v
	










	

