import sys
import os
import time
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph.networkx_adapter import NetworkXAdapter
from src.embedding.mock_engine import MockEmbeddingEngine
from src.core.node_manager import NodeManager
from src.core.edge_manager import EdgeManager
from src.core.rules_engine import RulesEngine

def run_simulation():
    print("Initializing Semantic Memory Graph...")
    graph_db = NetworkXAdapter()
    embedding_engine = MockEmbeddingEngine()
    node_manager = NodeManager(graph_db, embedding_engine)
    edge_manager = EdgeManager(graph_db, embedding_engine)
    rules_engine = RulesEngine(graph_db, node_manager)

    # 1. Create initial thoughts
    thoughts = [
        "Artificial Intelligence is the future of computing",
        "Machine learning models require vast amounts of data",
        "Neural networks are inspired by the human brain",
        "Graph databases store relationships between entities",
        "Cognitive architectures aim to simulate human thought",
        "Python is a popular language for data science",
        "FastAPI is a modern web framework for building APIs",
        "NetworkX is a Python library for studying graphs",
        "Semantic memory stores general world knowledge",
        "Episodic memory stores personal experiences"
    ]

    print(f"Adding {len(thoughts)} thoughts...")
    node_ids = []
    for text in thoughts:
        node_id = node_manager.create_node(text)
        node_ids.append(node_id)
        # Simulate some random manual connections
        if len(node_ids) > 1 and random.random() > 0.7:
            target = random.choice(node_ids[:-1])
            edge_manager.connect_nodes(node_id, target, "manual", 1.0)

    print(f"Graph state: {len(graph_db.get_all_nodes())} nodes")

    # 2. Discover connections
    print("Discovering semantic connections...")
    total_new_edges = 0
    for node_id in node_ids:
        new_edges = edge_manager.discover_connections(node_id)
        total_new_edges += new_edges
    print(f"Created {total_new_edges} semantic edges.")

    # 3. Evolve
    print("Running evolution cycles...")
    for i in range(3):
        print(f"Cycle {i+1}...")
        stats = rules_engine.evolve()
        print(f"  Stats: {stats}")
        time.sleep(0.5)

    print("Simulation complete.")
    
    # Final stats
    nodes = graph_db.get_all_nodes()
    print(f"Final Node Count: {len(nodes)}")
    # print(f"Nodes: {[n['content'] for n in nodes]}")

if __name__ == "__main__":
    run_simulation()
