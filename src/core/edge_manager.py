from typing import List
from ..graph.base import GraphDB
from ..embedding.base import EmbeddingEngine

class EdgeManager:
    """Manages connections between nodes."""

    def __init__(self, graph_db: GraphDB, embedding_engine: EmbeddingEngine):
        self.graph_db = graph_db
        self.embedding_engine = embedding_engine
        self.similarity_threshold = 0.7

    def connect_nodes(self, source_id: str, target_id: str, edge_type: str = "manual", weight: float = 1.0) -> None:
        """Explicitly connects two nodes."""
        self.graph_db.add_edge(source_id, target_id, weight, edge_type)

    def discover_connections(self, node_id: str) -> int:
        """Scans the graph for similar nodes and creates edges."""
        target_node = self.graph_db.get_node(node_id)
        if not target_node or "embedding" not in target_node:
            return 0

        target_embedding = target_node["embedding"]
        all_nodes = self.graph_db.get_all_nodes()
        new_edges_count = 0

        for node in all_nodes:
            if node["id"] == node_id:
                continue
            
            if "embedding" not in node:
                continue

            sim = self.embedding_engine.similarity(target_embedding, node["embedding"])
            
            if sim >= self.similarity_threshold:
                self.graph_db.add_edge(node_id, node["id"], weight=sim, edge_type="similarity")
                self.graph_db.add_edge(node["id"], node_id, weight=sim, edge_type="similarity") # Bi-directional
                new_edges_count += 1
        
        return new_edges_count
