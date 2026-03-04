# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (Python list)

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`)
- Do not change function signatures in `pathfinding.py`
- DFS must be iterative (NO recursion)
- BFS must use `collections.deque`
- Use `visited` set and `parent` dict for path reconstruction
- Mark nodes as visited when enqueued/pushed (not when popped)
- Keep changes minimal and keep `main()` runnable

## Output Contract
Running `python pathfinding.py` must:
- run BFS and DFS on at least 2 maps
- print found/path length/visited count
- print a rendered map with overlays
  - Path tiles shown as `*`
  - Visited tiles shown as `·` (middle dot)
  - Preserve `S` and `G` characters

## Implementation Details
- `parse_grid`: Convert string to grid, find S and G
- `neighbors`: Return 4-direction valid moves
- `reconstruct_path`: Build path from parent dict
- `bfs_path`: Use deque, track visited and parent
- `dfs_path`: Use list as stack, track visited and parent
- `render`: Overlay path and visited on grid

## Testing
- Example maps demonstrate different pathfinding behaviors
- Third map shows maze-like structure where DFS may find longer path
- Optional Monster Chase game makes algorithm differences tangible