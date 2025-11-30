import uuid
import time
from typing import Dict, Any, Optional
from ..graph.base import GraphDB
from ..embedding.base import EmbeddingEngine

class NodeManager:
    """Manages the lifecycle of nodes (thoughts) in the graph."""

    def __init__(self, graph_db: GraphDB, embedding_engine: EmbeddingEngine):
        self.graph_db = graph_db
        self.embedding_engine = embedding_engine

    def create_node(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Creates a new node with embedding and metadata."""
        if metadata is None:
            metadata = {}
        
        node_id = str(uuid.uuid4())
        embedding = self.embedding_engine.generate_embedding(content)
        
        # Enrich metadata
        metadata["created_at"] = time.time()
        metadata["embedding"] = embedding
        metadata["type"] = metadata.get("type", "concept")
        
        self.graph_db.add_node(node_id, content, metadata)
        return node_id

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a node."""
        return self.graph_db.get_node(node_id)

    def update_node(self, node_id: str, new_content: str = None, new_metadata: Dict[str, Any] = None) -> None:
        """Updates a node's content or metadata."""
        node = self.graph_db.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found")

        if new_content:
            node["content"] = new_content
            node["embedding"] = self.embedding_engine.generate_embedding(new_content)
        
        if new_metadata:
            node.update(new_metadata)
            
        # Re-save node (in NetworkX this is direct, for DBs might need explicit update)
        self.graph_db.add_node(node_id, node["content"], node)

    def merge_nodes(self, node_id1: str, node_id2: str) -> str:
        """Merges two nodes into a new one and deletes the originals."""
        n1 = self.get_node(node_id1)
        n2 = self.get_node(node_id2)
        
        if not n1 or not n2:
            raise ValueError("One or both nodes not found")

        # Create merged content
        merged_content = f"{n1['content']} + {n2['content']}"
        merged_metadata = {
            "merged_from": [node_id1, node_id2],
            "tags": list(set(n1.get("tags", []) + n2.get("tags", [])))
        }
        
        new_node_id = self.create_node(merged_content, merged_metadata)
        
        # TODO: Move edges from n1 and n2 to new_node_id
        
        # For now, just return new ID
        return new_node_id
