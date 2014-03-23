import random

fitness_calculator = None


class FitnessCalculator:
    def __init__(self, solution):
        self.solution = solution

    def score_fitness(self, individual):
    	"""
    	Compares the genes of a given individual to check them against the target individual, seeing how many match
    	"""
        return len([i for i, j in zip(self.solution, individual.genes) if i == j])

    def get_max_fitness(self):
    	"""
    	Curently hard coded to match Individuals
    	"""
        return 64


class Individual:
    def __init__(self, init):
        self.genes = []
        self.gene_length = 64
        self.generate_individual()

    def generate_individual(self):
        """
        Creates a randomized individual by filling its gene list with random 1s and 0s
        """
        for i in xrange(self.gene_length):
            self.genes.append(random.randint(0, 1))

    def get_gene(self, index):
        return self.genes[index]

    def set_gene(self, index, to_set):
        self.genes[index] = to_set;

    def size(self):
    	return len(self.genes)


class Population:
    def __init__(self, population_size, init):
        self.individuals = []

        if not init:
            return

        for i in xrange(population_size):
            self.individuals.append(Individual(True))

    def add_individual(self, individual):
        self.individuals.append(individual)

    def get_fittest(self):
    	"""
    	Finds the fittest individual in this Population by scoring them all
    	"""
        fittest = self.individuals[0]
        for individual in self.individuals:
            if fitness_calculator.score_fitness(individual) > fitness_calculator.score_fitness(fittest):
                fittest = individual
        return fittest

    def get_random(self):
    	"""
    	Gets a random member of this Population
    	"""
        return random.choice(self.individuals)

    def size(self):
        return len(self.individuals)


class Algorithm:
    def __init__(self):
        self.mutation_rate = 0.015
        self.uniformRate = 0.5
        self.elitism = True
        self.tournament_size = 5

    def evolve_population(self, population):
    	"""
    	Evolves a given population into a new one

    	It does this by conditionally preserving the fittest individual, and then
    	crossing over existing Individuals into new ones.  Finally, it may mutate
    	Individuals based on the Algorithm's mutation_rate.
    	"""
        new_population = Population(population.size(), False)
        elitism_offset = 0

        if self.elitism:
            new_population.add_individual(population.get_fittest())
            elitism_offset = 1

        for i in xrange(elitism_offset, population.size()):
            individual1 = self.tournament_selection(population)
            individual2 = self.tournament_selection(population)
            new_individual = self.crossover(individual1, individual2)
            new_population.add_individual(new_individual)

        for count, individual in enumerate(new_population.individuals):
            if self.elitism and count == 0:
                continue
            self.mutate(individual)

        return new_population

    def mutate(self, individual):
    	"""
    	Checks to see if a given Individual should be mutated
    	"""
        for i in xrange(individual.size()):
        	if random.random() <= self.mutation_rate:
        		individual.set_gene(i, random.randint(0, 1))
                
    def crossover(self, individual1, individual2):
    	"""
    	Crosses two Individuals into one new one
    	"""
        hybrid = Individual(False)

        for i in xrange(individual1.gene_length):
            if random.random() <= self.uniformRate:
                hybrid.set_gene(i, individual1.get_gene(i))
            else:
                hybrid.set_gene(i, individual2.get_gene(i))

        return hybrid

    def tournament_selection(self, population):
    	"""
    	Creates a temporary 'tournament' Population from which to select a strong
    	individual from.  The tournament Population is generally a subset of the
    	provided Population.
    	"""
        tournament = Population(self.tournament_size, False)
        for i in xrange(self.tournament_size):
            tournament.add_individual(population.get_random())

        return tournament.get_fittest()


if __name__ == '__main__':
    algorithm = Algorithm()
    target_individual = Individual(True)
    fitness_calculator = FitnessCalculator(target_individual.genes)

    population = Population(20, True)

    generation_count = 0

    while fitness_calculator.score_fitness(population.get_fittest()) != fitness_calculator.get_max_fitness():
        generation_count += 1
        population = algorithm.evolve_population(population)

    print 'answer found in generation: ' + str(generation_count)
    print population.get_fittest().genes




