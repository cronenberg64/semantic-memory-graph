# Semantic Memory Graph

A cognitive-architecture-inspired system that represents ideas as nodes inside a continuously evolving graph.

## Architecture

- **Graph Layer**: Abstraction over NetworkX (MVP) or Neo4j.
- **Embedding Layer**: Handles semantic vector generation (Mock for MVP).
- **Core Logic**:
    - `NodeManager`: CRUD for thoughts.
    - `EdgeManager`: Semantic connections.
    - `RulesEngine`: Evolution logic (decay, clustering).
- **API**: FastAPI interface.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   uvicorn src.api.main:app --reload
   ```
