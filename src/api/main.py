from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..graph.networkx_adapter import NetworkXAdapter
from ..embedding.mock_engine import MockEmbeddingEngine
from ..core.node_manager import NodeManager
from ..core.edge_manager import EdgeManager
from ..core.rules_engine import RulesEngine

app = FastAPI(title="Semantic Memory Graph API")

# Initialize components (Singleton pattern for MVP)
graph_db = NetworkXAdapter()
embedding_engine = MockEmbeddingEngine()
node_manager = NodeManager(graph_db, embedding_engine)
edge_manager = EdgeManager(graph_db, embedding_engine)
rules_engine = RulesEngine(graph_db, node_manager)

class CreateNodeRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class NodeResponse(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]

@app.post("/nodes", response_model=NodeResponse)
def create_node(request: CreateNodeRequest):
    node_id = node_manager.create_node(request.content, request.metadata)
    
    # Trigger edge discovery immediately for demo purposes
    edge_manager.discover_connections(node_id)
    
    node = node_manager.get_node(node_id)
    return NodeResponse(id=node["id"], content=node["content"], metadata=node)

@app.get("/graph")
def get_graph():
    """Returns the entire graph for visualization."""
    nodes = graph_db.get_all_nodes()
    # Edges are embedded in neighbors or we can fetch them separately.
    # For D3/Vis.js, we usually want {nodes: [], links: []}
    
    links = []
    if hasattr(graph_db, 'graph'):
        for u, v, data in graph_db.graph.edges(data=True):
            links.append({
                "source": u,
                "target": v,
                "weight": data.get("weight", 1.0),
                "type": data.get("type", "unknown")
            })
            
    return {"nodes": nodes, "links": links}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static files
app.mount("/static", StaticFiles(directory="d:/Programming Projects/semantic-memory-graph/src/api/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("d:/Programming Projects/semantic-memory-graph/src/api/static/index.html")

@app.post("/evolve")
def evolve_graph():
    """Triggers an evolution step."""
    stats = rules_engine.evolve()
    return {"status": "success", "stats": stats}
