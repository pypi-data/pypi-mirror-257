from typing import Protocol, Self, TypeAlias, TypeVar, Sequence

GenePosition: TypeAlias = int
Qualifier: TypeAlias = Sequence[int | float | str | bool]


class CytogeneticIndex(Protocol):
    """
    Defines the position of a gene regarding the genome, like chromosome set, chromosome number and position on a
    chromosome.
    """
    def __lt__(self, other: Self) -> bool: ...

    def __eq__(self, other: object) -> bool: ...

    def __hash__(self) -> int: ...

    def qualifier(self) -> Qualifier:
        """

        Returns:

        """
        ...


class TrivialCytogeneticIndex(CytogeneticIndex):
    """
    Trivial cytogenetic indices do not specify any location for genes at all, meaning genes cannot be mapped to specific
    locations.
    """
    def __lt__(self, other: Self): return False

    def __eq__(self, other: object): return True if self is other else False

    def qualifier(self) -> Qualifier:
        return []

    def __hash__(self) -> int:
        return id(self)


class SequentialCytogeneticIndex(CytogeneticIndex, Protocol):
    """
    Sequential cytogenetic indices allow genes to be mapped linear by an index. This assignment may not be exclusive,
    multiple genes may be assigned to the same index.
    """

    #: Index of the gene
    index: int

    def __hash__(self) -> int: return self.index


class ComplexCytogeneticIndex(CytogeneticIndex, Protocol):
    """
    Complex cytogenetic indices introduce chromosomes which genes can be mapped to. This mapping is usually not
    exclusive, multiple genes are often mapped to the same chromosome number.
    """
    #: Chromosome number of the chromosome the gene belongs to.
    chromosome_number: int

    def __hash__(self) -> int: return self.chromosome_number


class PolyploidCytogeneticIndex(CytogeneticIndex, Protocol):
    """
    Polyploid cytogenetic indices introduce sets, meaning genes can come in pairs. This usually refers to polyploid
    species where each chromosome is found multiple times in the genome.
    """
    #: Set to which the gene belongs.
    set_index: int

    def __hash__(self) -> int: return self.set_index


class ComplexPolyploidCytogeneticIndex(
    ComplexCytogeneticIndex, PolyploidCytogeneticIndex, SequentialCytogeneticIndex, Protocol
):
    """
    Complex polyploid cytogenetic indices unite all index types, allowing genes to be located by position on a
    chromosome, which itself is part of a chromosome set.
    """
    def reindex(self, chromosome_number: int, set_index: int, index: int) -> Self:
        """
        Changes the index of the gene, returning a copy with only the index changed.
        Args:
            chromosome_number: New chromosome number for the gene
            set_index: New chromosome set number for the gene
            index: New index on the chromosome for the gene

        Returns:
            Gene with its index changed
        """
        ...


    def __hash__(self) -> int: return hash((self.chromosome_number, self.set_index, self.index))


IndexType = TypeVar('IndexType', bound=CytogeneticIndex)
SecondaryIndexType = TypeVar('SecondaryIndexType', bound=CytogeneticIndex)
PolyploidIndexType = TypeVar('PolyploidIndexType', bound=PolyploidCytogeneticIndex)
ComplexPolyploidIndexType = TypeVar('ComplexPolyploidIndexType', bound=ComplexPolyploidCytogeneticIndex)
