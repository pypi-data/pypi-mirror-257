from functools import lru_cache, wraps
from typing import Protocol

from pyploid.types.gene import GeneType
from pyploid.types.individual import Individual, NamedIndividual, EvaluatedIndividual, ContravariantIndividualType


class Fitness(Protocol[ContravariantIndividualType]):
    def __call__(self, individual: ContravariantIndividualType) -> float: ...


def create_caching_fitness(
        fitness: Fitness[NamedIndividual[GeneType]],
        max_size: int = 128
) -> Fitness[NamedIndividual[GeneType]]:
    @wraps(fitness)
    @lru_cache(max_size)
    def cached_fitness(individual: NamedIndividual) -> float:
        return fitness(individual)

    return cached_fitness


def make_evaluation_aware(
        fitness: Fitness[Individual[GeneType]],
        asign: bool = False
) -> Fitness[EvaluatedIndividual[GeneType]]:
    def use_prior_evaluation(individual: EvaluatedIndividual[GeneType]) -> float:
        if individual.fitness is None:
            evaluation: float = fitness(individual)
            if asign:
                individual.fitness = evaluation
            return evaluation
        else:
            return individual.fitness

    return use_prior_evaluation
