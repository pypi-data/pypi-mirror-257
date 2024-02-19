from collections.abc import Sequence

from pyploid.types.individual import IndividualType, Population


def constant_population(population: Population[IndividualType], survivors: Sequence[IndividualType]) -> int:
    """
    Strategy for determining the number of children born in the next generation to ensure a constant population.
    Args:
        population: Current population
        survivors: Survivors of the current population

    Returns:
        Difference of the size of the current population and the size of survivors.
    """
    return len(population.members) - len(survivors)