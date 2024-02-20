"""
Data structures for the usage of mathematics functions as basis for evolutionary algorithms.
"""
from collections.abc import Iterable
from dataclasses import dataclass, replace
from inspect import signature
from operator import attrgetter
from typing import Generic, Protocol, Sequence, Callable

from toolz import groupby, valmap

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.mutation import Mutation
from pyploid.types.cytogenetic_index import IndexType
from pyploid.types.gene import DataclassGene
from pyploid.types.individual import Individual


class MathFunction(Protocol):
    """
    Protocol for a mathematics function defined by its name and parameter count used in or as a fitness function in an
    evolutionary algorithm. This implies that the function must return a value for every set of parameter, even if
    undefined at given point. The usual way of describing this is returning positive infinity but other values are
    possible, especially for bounded functions. The function needn't be continuous.
    """
    #: Number of parameters the function takes
    parameter_count: int
    #: Name of the function
    name: str

    def __call__(self, parameter: Sequence[float]) -> float:
        """
        Evaluates the function at a given point.
        Args:
            parameter: Point the function should be evaluated at.
        Returns:
            Value of the function at the given point or a penalty value (+infinity most of the time) in case the
            function is undefined at given point.
        """
        ...


class _WrappedMathFunction:
    def __init__(self, func: Callable[..., float]):
        self.name = func.__name__
        self.parameter_count: int = len(signature(func).parameters)
        self._func: Callable[..., float] = func

    def __call__(self, parameter: Sequence[float]) -> float:
        try:
            return self._func(*parameter)
        except ValueError:
            return float('inf')


def as_math_function(func: Callable[..., float]) -> MathFunction:
    """
    Converts a function that takes n parameters into a MathFunction taking one parameter of length n. Should the
    converted function throw a ValueError +infinity is returned instead.

    Args:
        func: The function to be converted.

    Returns:
        MathFunction: Function as MathFunction with the same name and the parameter count reflecting the argument count
        of the original function.
    """
    return _WrappedMathFunction(func)


@dataclass(frozen=True)
class FunctionParameterGene(DataclassGene[IndexType], Generic[IndexType]):
    """
    Gene representing the value of one dimension of a mathematical function. If a function with three parameters is used
    there should be at least three genes, at least one for every dimension in the parameter.
    """
    #: Function the parameter is related to
    function: MathFunction
    #: Value of the parameter
    value: float
    #: Position of the parameter in the parameter vector.
    parameter_index: int

    def get_function(self) -> MathFunction:
        """
        Returns the mathematics function the gene refers to.

        Returns:
            MathFunction: Related function
        """
        return self.function

    def get_parameter_index(self) -> int:
        """
        Returns the index of the parameter in the overall parameter vector.

        Returns:
            int: Index of the parameter in the parameter vector.
        """
        return self.parameter_index


def average(values: Sequence[float]) -> float:
    """
    Returns the average of a sequence of numbers.

    Args:
        values: Sequence of numbers

    Returns:
        float: Average of the given sequence
    """
    return sum(values) / len(values)


def _calculate_value(function: MathFunction, parameter: Sequence[FunctionParameterGene[IndexType]],
                     default_for_missing: float, aggregate: Callable[[Sequence[float]], float]) -> float:
    values: dict[int, float] = valmap(
        lambda p: aggregate(tuple(map(attrgetter('value'), p))), groupby(attrgetter('parameter_index'), parameter)
    )
    return function([values.get(i, default_for_missing) for i in range(function.parameter_count)])


def create_function_parameter_fitness(
        aggregate: Callable[[Sequence[float]], float] = average,
        default_for_missing: float = float('inf')
) -> Fitness[Individual[FunctionParameterGene[IndexType]]]:
    """
    Creates a fitness function that evaluates every MathFunction referenced in the genome. If multiple genes for the
    same function are defined that have the same parameter index, the aggregate function will reduce the values to a
    single one. If a function lacks a parameter the default_for_missing value is used instead. Genes with a parameter
    index greater than the dimension of the function are ignored. Functions that are not present in the genome are
    not evaluated, either.
    Args:
        aggregate: Function to reduce multiple values for the same function and parameter_index to a single value
        default_for_missing: Value used for missing parameters

    Returns:
        Sum of the evaluated function values.
    """
    def fitness(individual: Individual[FunctionParameterGene[IndexType]]) -> float:
        """
        Evaluates the individual's fitness in regard to parameters of mathematics functions defined in the genome.
        Args:
            individual: Individual to be evaluated.

        Returns:
            float: Fitness of the individual.
        """
        evaluations: dict[MathFunction, Sequence[FunctionParameterGene[IndexType]]] = groupby(attrgetter('function'),
                                                                                              individual.genes)
        return sum(_calculate_value(func, genes, default_for_missing, aggregate) for func, genes in evaluations.items())

    return fitness


def create_value_mutation(mutate_value: Callable[[float], float], ) -> Mutation[FunctionParameterGene[IndexType]]:
    """
    Creates a value mutator for FunctionParameterGens, altering the value in respect to the specified mutator.

    Args:
        mutate_value: Mutator for the value, taking the original value and producing the new value.

    Returns:
        Mutation: Mutation strategy to be used in evolutionary algorithms.
    """
    def mutate_values(genes: Sequence[FunctionParameterGene[IndexType]]) -> Iterable[FunctionParameterGene[IndexType]]:
        """
        Mutates the values of a sequence FunctionParameterGene
        Args:
            genes: Genes to be modified

        Returns:
            Mutated genes with possibly altered values.
        """
        for gene in genes:
            yield replace(gene, value=mutate_value(gene.value))

    return mutate_values
