from abc import ABC, abstractmethod
from typing import List

class EmbeddingEngine(ABC):
    """Abstract base class for Embedding Engine."""

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generates a vector embedding for the given text."""
        pass

    @abstractmethod
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculates similarity between two vectors."""
        pass
