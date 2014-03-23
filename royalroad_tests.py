import royalroad

def test_crossover():
	algorithm = royalroad.Algorithm()

	ind1 = royalroad.Individual(True)
	ind2 = royalroad.Individual(True)

	ind = algorithm.crossover(ind1, ind2)
	assert len(ind.genes) == len(ind1.genes)
	assert not ind.genes == ind1.genes
	assert not ind.genes == ind2.genes

def test_tournament_selection():
	algorithm = royalroad.Algorithm()
	population = royalroad.Population(5, True)
	assert  isinstance(algorithm.tournament_selection(population), royalroad.Individual)

def test_mutate():
	ind1 = royalroad.Individual(True)
	algorithm = royalroad.Algorithm()

	algorithm.mutation_rate = 1
	start_sequence = str(ind1.genes)
	algorithm.mutate(ind1)
	assert not str(ind1.genes) == start_sequence

if __name__ == '__main__':

	target_individual = royalroad.Individual(True)
	royalroad.fitness_calculator = royalroad.FitnessCalculator(target_individual.genes)

	test_crossover()
	test_tournament_selection()
	test_mutate()