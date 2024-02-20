from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field, replace
from typing import TypeVar, NewType, Protocol, runtime_checkable, cast

from pyploid.types.cytogenetic_index import IndexType, ComplexPolyploidIndexType, SecondaryIndexType

T = TypeVar('T')
ValueType = TypeVar('ValueType')

GeneID = NewType('GeneID', str)


class Gene(Protocol[IndexType]):
    """
    Protocol for genes. Every gene must have a position which needn't be unique.
    """
    #: Position of the gene in the genome
    position: IndexType


GeneType = TypeVar('GeneType')


@dataclass(frozen=True)
class GeneDescription:
    """
    Description of a particular gene
    """
    uuid: GeneID
    allele_type: type[Gene]
    description: str | None = field(default=None)


@runtime_checkable
@dataclass(frozen=True)
class DataclassGene(Gene[IndexType], Protocol[IndexType]):
    """
    Protocol for genes that are realized using dataclasses. Genes of that type must be frozen dataclasses and
    modifications will only be applied by dataclasses.replace.
    """
    #: Position of the gene in the genome
    position: IndexType


def transform_position(gene: Gene[IndexType] | DataclassGene[IndexType], position: SecondaryIndexType) -> Gene[
    SecondaryIndexType]:
    """
    Transforms a gene by modifying its cytogenetic index. The new index might be of a different cytogenetic index
    type.
    Args:
        gene: The gene to alter
        position: New position of the gene in the genome

    Returns:
        New gene with its position updated.
    """
    if isinstance(gene, DataclassGene):
        return replace(cast(DataclassGene[SecondaryIndexType], gene), position=position)
    else:
        cast(Gene[SecondaryIndexType], gene).position = position
        return cast(Gene[SecondaryIndexType], gene)


def update_position(gene: Gene[IndexType] | DataclassGene[IndexType], position: IndexType) -> Gene[IndexType]:
    """
    Updates the position of a gene within the genome to another cytogenetic index value.
    Args:
        gene: The gene to alter
        position: New position of the gene in the genome

    Returns:
        New gene with its position updated.
    """
    if isinstance(gene, DataclassGene):
        return replace(gene, position=position)
    else:
        gene.position = position
        return gene


def reindex_chromosome_sets(genes: Iterable[Gene[ComplexPolyploidIndexType]]) -> Iterable[
    Gene[ComplexPolyploidIndexType]]:
    """
    Reindex genes so that genes with the same position on the same chromosome set are placed on different chromosomes
    within the set. This may add additional chromosomes to a set if necessary. This function is used mainly after
    merging genes of different parents.

    Args:
        genes: Genes to reindex

    Returns:
        Genes with updated position.
    """
    indices: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for gene in genes:
        position: ComplexPolyploidIndexType = gene.position
        new_set_index: int = indices[position.chromosome_number][position.index]
        yield update_position(gene, position.reindex(position.chromosome_number, new_set_index, position.index))
        indices[position.chromosome_number][position.index] += 1
