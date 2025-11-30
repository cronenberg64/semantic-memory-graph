from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class GraphDB(ABC):
    """Abstract base class for Graph Database operations."""

    @abstractmethod
    def add_node(self, node_id: str, content: str, metadata: Dict[str, Any] = None) -> None:
        """Adds a node to the graph."""
        pass

    @abstractmethod
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a node by ID."""
        pass

    @abstractmethod
    def add_edge(self, source_id: str, target_id: str, weight: float, edge_type: str) -> None:
        """Adds a directed edge between two nodes."""
        pass

    @abstractmethod
    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """Returns neighboring nodes and edge data."""
        pass

    @abstractmethod
    def get_all_nodes(self) -> List[Dict[str, Any]]:
        """Returns all nodes in the graph."""
        pass
