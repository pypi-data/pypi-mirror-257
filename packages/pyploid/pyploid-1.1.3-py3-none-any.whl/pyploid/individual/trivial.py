from collections.abc import Sequence, Iterable
from dataclasses import dataclass
from typing import Generic

from pyploid.types.gene import GeneType
from pyploid.types.individual import IndividualType, Population


@dataclass(frozen=True)
class TrivialIndividual(Generic[GeneType]):
    """
    Describes an individual only by its genes without any further metadata.
    """
    #: Genes of the individual
    genes: Sequence[GeneType]


@dataclass(frozen=True)
class TrivialPopulation(Generic[IndividualType], Population[IndividualType]):
    """
    Describes a population only by its members without any further metadata.
    """
    #: Members of the population
    members: Sequence[IndividualType]


def create_trivial_individual(
        genes: Iterable[GeneType],
        _: Iterable[TrivialIndividual[GeneType]]
) -> TrivialIndividual[GeneType]:
    """
    Args:
        genes:
        _:

    Returns:

    """
    return TrivialIndividual(tuple(genes))


def create_trivial_population(members: Iterable[IndividualType]) -> TrivialPopulation[IndividualType]:
    """
    Creates a trivial population consisting of the individuals specified.
    Args:
        members: Individuals of the population.

    Returns:
        New trivial population with the specified individuals
    """
    return TrivialPopulation(tuple(members))
