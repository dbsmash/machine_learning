package main

import "fmt"
import "math/rand"
import "time"

// Fitness
type FitnessCalculator struct {
	solution Individual
}

func (fc *FitnessCalculator) scoreFitness(ind Individual) int {
	score := 0
	for i := 0; i < 64; i++ {
		if fc.solution.genes[i] == ind.genes[i] {
			score++
		}
	}
	return score
}

func (fc *FitnessCalculator) getMaxFitness() int {
	return 64
}

// Individuals
type Individual struct {
	genes [64]int
}

func (ind *Individual) generateIndividual() {

	var buffer [64]int
	for i := 0; i < 64; i++ {
		buffer[i] = rand.Intn(2)
	}
	ind.genes = buffer
}

func (ind *Individual) getGene(index int) int {
	return ind.genes[index]
}

func (ind *Individual) setGene(index int, value int) {
	ind.genes[index] = value
}

func (ind *Individual) size() int {
	return len(ind.genes)
}

// Populations
type Population struct {
	individuals []Individual
}

func (pop *Population) initialize(size int, init bool) {
	if !init {
		return
	}
	for i := 0; i < size; i++ {
		ind := Individual{}
		ind.generateIndividual()
		pop.addIndividual(ind)
	}
}

func (pop *Population) addIndividual(ind Individual) {
	pop.individuals = append(pop.individuals, ind)
}

func (pop *Population) getFittest(fc FitnessCalculator) Individual {
	fittest := pop.individuals[0]
	for i := 0; i < len(pop.individuals); i++ {
		if fc.scoreFitness(pop.individuals[i]) > fc.scoreFitness(fittest) {
			fittest = pop.individuals[i]
		}
	}
	return fittest
}

func (pop *Population) getRandom() Individual {
	return pop.individuals[rand.Intn(20)]
}

func (pop *Population) size() int {
	return len(pop.individuals)
}

// Algorithms
type Algorithm struct {
	mutationRate   float32
	uniformRate    float32
	elitism        bool
	tournamentSize int
	fitnessCalc    FitnessCalculator
}

func (algor *Algorithm) evolvePopulation(pop Population) Population {
	newPopulation := Population{}
	elitismOffset := 0

	if algor.elitism {
		newPopulation.addIndividual(pop.getFittest(algor.fitnessCalc))
		elitismOffset = 1
	}

	for i := elitismOffset; i < pop.size(); i++ {
		individual1 := algor.tournamentSelection(pop)
		individual2 := algor.tournamentSelection(pop)
		newIndividual := algor.crossover(individual1, individual2)
		newPopulation.addIndividual(newIndividual)
	}

	for i := 0; i < newPopulation.size(); i++ {
		if algor.elitism && i == 0 {
			continue
		}
		algor.mutate(&newPopulation.individuals[i])
	}

	return newPopulation
}

func (algor *Algorithm) mutate(ind *Individual) {
	for i := 0; i < ind.size(); i++ {
		if rand.Float32() <= algor.mutationRate {
			ind.setGene(i, rand.Intn(2))
		}
	}
}

func (algor *Algorithm) crossover(individual1 Individual, individual2 Individual) Individual {
	hybrid := Individual{}
	for i := 0; i < individual1.size(); i++ {
		if rand.Float32() <= algor.uniformRate {
			hybrid.setGene(i, individual1.getGene(i))
		} else {
			hybrid.setGene(i, individual2.getGene(i))
		}
	}
	return hybrid
}

func (algor *Algorithm) tournamentSelection(pop Population) Individual {
	tournament := new(Population)
	for i := 0; i < algor.tournamentSize; i++ {
		tournament.addIndividual(pop.getRandom())
	}

	return tournament.getFittest(algor.fitnessCalc)
}

func main() {
	fmt.Println("Royal Road!")
	rand.Seed(time.Now().UTC().UnixNano())

	solution := Individual{}
	solution.generateIndividual()

	fitnessCalc := FitnessCalculator{solution}
	algorithm := Algorithm{0.015, 0.5, true, 5, fitnessCalc}

	generationCount := 0
	population := Population{}
	population.initialize(20, true)

	for {
		if fitnessCalc.scoreFitness(population.getFittest(fitnessCalc)) == fitnessCalc.getMaxFitness() {
			break
		}
		generationCount++
		population = algorithm.evolvePopulation(population)
		fmt.Println("generation & fitness", generationCount, fitnessCalc.scoreFitness(population.getFittest(fitnessCalc)))
	}
	fmt.Println("answer found in generation ", generationCount)
}
