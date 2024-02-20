from collections.abc import Sequence
from typing import Protocol, Iterable

from pyploid.types.cytogenetic_index import IndexType, SecondaryIndexType
from pyploid.types.gene import Gene


class GeneLayout(Protocol[SecondaryIndexType, IndexType]):
    """
    A layout maps genes with one cytogenetic index type to genes with another cytogenetic index type, changing the
    layout of the genome. Most of the time genes with a trivial cytogenetic index type are mapped to a more complex
    index type. Genes may be copied in this approach, based on the actual algorithm used.
    """
    def __call__(self, genes: Sequence[Gene[IndexType]]) -> Iterable[Gene[SecondaryIndexType]]:
        """
        Maps the genes depending on their individual index or based on their index within the sequence. The latter
        is often used for transforming the parameters of the problem into a genome.

        Args:
            genes: Genes to be transformed.

        Returns:
            Transformed genes.
        """
        ...