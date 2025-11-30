import networkx as nx
from typing import List, Dict, Any, Optional
from .base import GraphDB

class NetworkXAdapter(GraphDB):
    """In-memory GraphDB implementation using NetworkX."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node_id: str, content: str, metadata: Dict[str, Any] = None) -> None:
        if metadata is None:
            metadata = {}
        self.graph.add_node(node_id, content=content, **metadata)

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        if not self.graph.has_node(node_id):
            return None
        return {"id": node_id, **self.graph.nodes[node_id]}

    def add_edge(self, source_id: str, target_id: str, weight: float, edge_type: str) -> None:
        self.graph.add_edge(source_id, target_id, weight=weight, type=edge_type)

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        if not self.graph.has_node(node_id):
            return []
        neighbors = []
        for neighbor_id in self.graph.neighbors(node_id):
            edge_data = self.graph.get_edge_data(node_id, neighbor_id)
            neighbors.append({
                "id": neighbor_id,
                "edge": edge_data,
                "node": self.graph.nodes[neighbor_id]
            })
        return neighbors

    def get_all_nodes(self) -> List[Dict[str, Any]]:
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            nodes.append({"id": node_id, **data})
        return nodes
