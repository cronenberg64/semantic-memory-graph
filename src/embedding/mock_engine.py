import random
import numpy as np
from typing import List
from .base import EmbeddingEngine

class MockEmbeddingEngine(EmbeddingEngine):
    """Mock embedding engine for testing and MVP."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def generate_embedding(self, text: str) -> List[float]:
        # Deterministic mock embedding based on text hash for consistency in tests
        # In a real scenario, this would call an API or local model
        seed = sum(ord(c) for c in text)
        rng = np.random.default_rng(seed)
        return rng.random(self.dimension).tolist()

    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        # Cosine similarity
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))
