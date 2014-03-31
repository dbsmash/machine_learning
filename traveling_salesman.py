import math
import random
from PIL import Image, ImageDraw

debug = False
fitness_calculator = None


class FitnessCalculator:
    def score_fitness(self, individual):
        """
        Compares the genes of a given individual to check them against the target individual, seeing how many match
        """
        return 1 / individual.get_total_distance()


class TravelPlan:
    def __init__(self):
        self.cities = []
        self.distance = 0
        self.fitness = 0

    def add_city(self, city):
        self.cities.append(city)

    def get_city(self, index):
        return self.cities[index]

    def set_city(self, index, city_to_set):
        self.cities[index] = city_to_set

    def set_cities(self, city_plan):
        for city in city_plan.cities:
            self.add_city(city)

    def set_city_list(self, cities):
        self.cities = cities

    def size(self):
        return len(self.cities)

    def randomize(self):
        random.shuffle(self.cities)

    def get_total_distance(self):
        if not self.distance:

            from_city = self.cities[0]

            for city in self.cities:
                self.distance += from_city.distance_to(city)
                from_city = city

            # add in distance for return to start city
            self.distance += from_city.distance_to(self.cities[0])

        return self.distance


class City:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, destination_city):
        x_distance = math.fabs(self.x - destination_city.x)
        y_distance = math.fabs(self.y - destination_city.y)
        distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
        return distance


class CityList:
    list_size = 20

    def __init__(self):
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

    def get_city(self, index):
        try:
            return self.cities[index]
        except IndexError:
            return None

    def size(self):
        return len(self.cities)

    def populate_list(self):
        for i in xrange(CityList.list_size):
            city = City()
            city.set_location(random.randint(1, 500), random.randint(1, 500))
            self.add_city(city)


class Population:
    def __init__(self, population_size, init):
        self.individuals = []

        if not init:
            return

        for i in xrange(population_size):
            self.individuals.append(TravelPlan())

    def add_individual(self, individual):
        self.individuals.append(individual)

    def get_individual(self, index):
        return self.individuals[index]

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
        Checks to see if a given Individual should be mutated and mutates
        by switching two elements randomly
        """
        if random.random() <= self.mutation_rate:
            individual.distance = 0
            index1 = random.randint(0, individual.size() - 1)
            index2 = random.randint(0, individual.size() - 1)
            while index1 == index2:
                index2 = random.randint(0, individual.size() - 1)
            element1 = individual.get_city(index1)
            element2 = individual.get_city(index2)
            individual.set_city(index1, element2)
            individual.set_city(index2, element1)

    def crossover(self, individual1, individual2):
        """
        Crosses two Individuals into one new one
        """
        hybrid = TravelPlan()
        index1 = random.randint(0, individual1.size() - 1)
        index2 = random.randint(0, individual1.size() - 1)
        ind1_subset = individual1.cities[index1:index2]
        for city in individual2.cities:
            if not city in ind1_subset:
                ind1_subset.append(city)

        hybrid.set_city_list(ind1_subset)
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


def render_route(cities):
    im = Image.new('RGBA', (500, 500), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    for city in cities:
        draw.ellipse((city.x - 5, city.y - 5, city.x + 5, city.y + 5), fill=(0, 0, 0))

    from_city = cities[0]
    for city in cities:
        draw.line((from_city.x, from_city.y, city.x, city.y), fill=0)
        from_city = city
    im.show()


if __name__ == '__main__':
    fitness_calculator = FitnessCalculator()
    algorithm = Algorithm()

    # build random list of cities
    city_list = CityList()
    city_list.populate_list()

    test_route = TravelPlan()
    test_route.set_cities(city_list)
    initial_distance = float(test_route.get_total_distance())

    render_route(city_list.cities)

    population = Population(20, True)
    for i in xrange(population.size()):
        tp = population.get_individual(i)
        tp.set_cities(city_list)
        tp.randomize()
        population.add_individual(tp)

    for i in xrange(1, 250):
        population = algorithm.evolve_population(population)

    final_distance = population.get_fittest().get_total_distance()
    print 'Initial distance: ' + str(initial_distance)
    print 'Final distance: ' + str(final_distance)
    print 'Improvement: ' + str(final_distance / initial_distance)

    render_route(population.get_fittest().cities)
