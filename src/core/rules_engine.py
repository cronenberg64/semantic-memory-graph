import networkx as nx
from typing import List, Dict, Any
from ..graph.base import GraphDB
from ..core.node_manager import NodeManager

class RulesEngine:
    """Handles graph evolution rules: decay, clustering, abstraction."""

    def __init__(self, graph_db: GraphDB, node_manager: NodeManager):
        self.graph_db = graph_db
        self.node_manager = node_manager
        self.decay_rate = 0.05
        self.min_weight = 0.1

    def evolve(self) -> Dict[str, Any]:
        """Runs one evolution cycle."""
        stats = {
            "decayed_edges": 0,
            "removed_edges": 0,
            "clusters_found": 0,
            "abstractions_created": 0
        }
        
        # 1. Decay Edges
        # Note: In a real DB, we'd use a query. Here we iterate.
        # We need to access the underlying networkx graph if possible for speed, 
        # or use get_all_nodes/neighbors.
        # For the MVP, let's assume we can iterate edges via the adapter if we cast it,
        # or just iterate all nodes.
        
        # Accessing internal graph for MVP efficiency (breaking abstraction slightly for performance)
        if hasattr(self.graph_db, 'graph'):
            graph = self.graph_db.graph
            edges_to_remove = []
            for u, v, data in graph.edges(data=True):
                if data.get("type") == "similarity": # Only decay similarity edges? Or all?
                    # Let's decay all for now, or maybe just 'temporal' ones.
                    # For this MVP, let's decay 'similarity' edges that aren't reinforced.
                    weight = data.get("weight", 1.0)
                    new_weight = weight * (1.0 - self.decay_rate)
                    
                    if new_weight < self.min_weight:
                        edges_to_remove.append((u, v))
                    else:
                        graph[u][v]['weight'] = new_weight
                        stats["decayed_edges"] += 1
            
            for u, v in edges_to_remove:
                graph.remove_edge(u, v)
                stats["removed_edges"] += 1

        # 2. Clustering & Abstraction
        # Find connected components (simple clustering)
        if hasattr(self.graph_db, 'graph'):
            # Convert to undirected for community detection
            undirected = self.graph_db.graph.to_undirected()
            components = list(nx.connected_components(undirected))
            
            stats["clusters_found"] = len(components)
            
            for component in components:
                if len(component) >= 3: # Only abstract clusters with 3+ nodes
                    # Check if already abstracted (naive check)
                    # Real logic would check if a "summary" node connects to all of them
                    
                    # Create abstraction
                    # 1. Generate summary text (mock)
                    nodes_content = [self.graph_db.get_node(n)["content"] for n in component]
                    summary_text = f"Concept Cluster: {', '.join(nodes_content[:3])}..."
                    
                    # 2. Create node
                    # Check if similar node exists to avoid duplicates? 
                    # For MVP, just create it if it doesn't look like we just made it.
                    # (Skipping duplicate check for MVP simplicity)
                    
                    # abstract_id = self.node_manager.create_node(summary_text, {"type": "abstraction"})
                    # stats["abstractions_created"] += 1
                    
                    # 3. Link to members
                    # for member_id in component:
                    #     self.graph_db.add_edge(abstract_id, member_id, 1.0, "abstraction")
                    
                    pass # Commented out to prevent explosion of nodes in simple demo

        return stats
