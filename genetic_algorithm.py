from functools import partial
from typing import List, Callable, Tuple, Dict
from random import choices, randint, randrange, random

from fitness import fitness


POPULATION_SIZE = 2
GENERATIONS = 2


Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def get_genome_cache_key(genome: Genome) -> str:
    return ''.join([str(char) for char in genome])


def fitness_wrapper(genome: Genome, cache: Dict[str, int]) -> int:
    genome_key = get_genome_cache_key(genome)
    print("Paramaters Generated:",args)
    branchLen = genome[:6][0]*32 + genome[:6][1]*16 + genome[:6][2]*8 + genome[:6][3]*4 + genome[:6][4]*2 + genome[:6][5]*1
    armLen = genome[6:12][0]*32 + genome[6:12][1]*16 + genome[6:12][2]*8 + genome[6:12][3]*4 + genome[6:12][4]*2 + genome[6:12][5]*1   
    angle = genome[12:][0]*32 + genome[12:][1]*16 + genome[12:][2]*8 + genome[12:][3]*4 + genome[12:][4]*2 + genome[12:][5]*1
    args = [branchLen, armLen, angle]
    print("Paramaters Generated:",args)
    value = fitness(args)
    cache[genome_key] = value
    return value


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(population=population, weights=[fitness_func(genome) for genome in population], k=2)


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        print('Error in single_point_crossover')
        return [], []
    length = len(a)
    if length < 2:
        return a, b
    p = randint(1, length - 1)
    return a[:p] + b[p:], b[:p] + a[p:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else (1 if genome[index] == 0 else 0)
    return genome


# Returns final population and number of generations
def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = GENERATIONS,
        fitness_limit: int = None,
) -> Tuple[Population, int]:

    population = populate_func()
    if generation_limit < 1:
        return [], -1
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        if fitness_limit is not None and fitness_func(population[0]) >= fitness_limit:
            break
        next_generation = population[:2]
        for j in range(len(population) // 2 - 1):
            parents = selection_func(population, fitness_func)
            child_a, child_b = crossover_func(parents[0], parents[1])
            child_a = mutation_func(child_a)
            child_b = mutation_func(child_b)
            next_generation += [child_a, child_b]
        population = next_generation

    population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
    return population, i + 1


def main():
    fitness_cache = {}
    populations, generations = run_evolution(
        populate_func=partial(generate_population, size=POPULATION_SIZE, genome_length=18),
        fitness_func=lambda genome: fitness_wrapper(genome, fitness_cache)
    )
    print(populations[0])
    print(generations)


main()

