from dataclasses import dataclass
from typing import Generic, TypeVar

from pyploid.types.cytogenetic_index import IndexType
from pyploid.types.gene import DataclassGene


ValueType = TypeVar('ValueType')

@dataclass(frozen=True)
class ValueGene(Generic[IndexType, ValueType], DataclassGene[IndexType]):
    position: IndexType
    value: ValueType
