#!/usr/bin/env python3
"""
MonsterChase - BFS vs DFS Pathfinding Demo
GitHub Repository: https://github.com/Zencode22/MonsterChase
"""

from __future__ import annotations

from collections import deque
import time
import os
import sys
from typing import Dict, List, Optional, Set, Tuple, Union

# Type aliases
Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]

# Repository info
REPO_NAME = "MonsterChase"
REPO_URL = "https://github.com/Zencode22/MonsterChase"
VERSION = "1.0.0"

# Example maps
EXAMPLE_MAP_1 = """
##########
#S..#....#
#..##.##.#
#...#...G#
##########
""".strip("\n")

EXAMPLE_MAP_2 = """
############
#S.....#...#
###.##.#.#.#
#...#..#.#G#
#.###..#...#
#......###.#
############
""".strip("\n")

EXAMPLE_MAP_3 = """
##########
#S.......#
#.#####..#
#.#...#..#
#.#.#.#G.#
#.#.#.#..#
#...#....#
##########
""".strip("\n")

# Game map
GAME_MAP = """
##########
#P.......#
#.#####..#
#.#...#..#
#.#.#.#G.#
#.#.#.#..#
#...#....#
#....M...#
##########
""".strip("\n")


def print_banner():
    """Print a cool banner for the game."""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                     🏃 MONSTER CHASE 🏃                       ║
║         BFS vs DFS - Pathfinding Algorithm Showdown          ║
║                                                              ║
║   GitHub: {REPO_URL}  ║
║   Version: {VERSION}                                           ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    # Split into lines and remove empty lines
    lines = [line for line in text.strip().split('\n') if line.strip()]
    grid = [list(line) for line in lines]
    
    start = None
    goal = None
    
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
            elif cell == 'G':
                goal = (r, c)
    
    if start is None:
        raise ValueError("Map must contain exactly one 'S' start position")
    if goal is None:
        raise ValueError("Map must contain exactly one 'G' goal position")
    
    return grid, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    r, c = node
    rows, cols = len(grid), len(grid[0])
    candidates = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
    
    valid = []
    for nr, nc in candidates:
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            valid.append((nr, nc))
    
    return valid


def reconstruct_path(parent: Dict[Pos, Union[Pos, None]], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if goal not in parent and goal != start:
        return None
    
    path = []
    current = goal
    
    while current != start:
        path.append(current)
        if current not in parent:
            return None
        current = parent[current]
        if current is None:  # Safety check
            return None
    
    path.append(start)
    return list(reversed(path))


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    if start == goal:
        return [start], {start}
    
    # Initialize
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            path = reconstruct_path(parent, start, goal)
            return path, visited
        
        for neighbor in neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    # No path found
    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    if start == goal:
        return [start], {start}
    
    # Initialize
    stack = [start]
    visited = {start}
    parent = {start: None}
    
    while stack:
        current = stack.pop()
        
        if current == goal:
            path = reconstruct_path(parent, start, goal)
            return path, visited
        
        for neighbor in neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    # No path found
    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules:
    - path tiles shown as '*'
    - visited tiles shown as '·' (middle dot)
    - preserve 'S' and 'G'
    """
    path_set = set(path) if path else set()
    visited_set = visited or set()
    
    result = []
    for r, row in enumerate(grid):
        line = []
        for c, cell in enumerate(row):
            pos = (r, c)
            
            if cell == 'S' or cell == 'G':
                line.append(cell)
            elif pos in path_set:
                line.append('*')
            elif pos in visited_set:
                line.append('·')
            else:
                line.append(cell)
        result.append(''.join(line))
    
    return '\n'.join(result)


def run_one(label: str, grid_text: str) -> None:
    """Run both algorithms on a single map and print results."""
    try:
        grid, start, goal = parse_grid(grid_text)
    except ValueError as e:
        print(f"Error parsing map '{label}': {e}")
        return
    
    print("=" * 60)
    print(f"📊 {label}")
    print("-" * 60)
    print("Original map:")
    print(render(grid))
    print()
    
    # BFS
    start_time = time.time()
    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    bfs_time = time.time() - start_time
    
    print("🔵 BFS (Queue-based):")
    print(f"  ✅ Path found: {path_bfs is not None}")
    print(f"  📏 Path length: {len(path_bfs) if path_bfs else 'N/A'}")
    print(f"  👀 Nodes visited: {len(visited_bfs)}")
    print(f"  ⏱️  Time: {bfs_time:.6f} seconds")
    print("  🗺️  Rendered map:")
    print(render(grid, path=path_bfs, visited=visited_bfs))
    print()
    
    # DFS
    start_time = time.time()
    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    dfs_time = time.time() - start_time
    
    print("🟢 DFS (Stack-based):")
    print(f"  ✅ Path found: {path_dfs is not None}")
    print(f"  📏 Path length: {len(path_dfs) if path_dfs else 'N/A'}")
    print(f"  👀 Nodes visited: {len(visited_dfs)}")
    print(f"  ⏱️  Time: {dfs_time:.6f} seconds")
    print("  🗺️  Rendered map:")
    print(render(grid, path=path_dfs, visited=visited_dfs))
    print()
    
    # Comparison if both found paths
    if path_bfs and path_dfs:
        print("📈 Comparison:")
        if len(path_bfs) < len(path_dfs):
            print(f"  ✓ BFS found SHORTER path (difference: {len(path_dfs) - len(path_bfs)} steps)")
        elif len(path_bfs) > len(path_dfs):
            print(f"  ⚠ DFS found SHORTER path (difference: {len(path_bfs) - len(path_dfs)} steps)")
        else:
            print("  📊 Both paths are the same length")
        
        visited_diff = len(visited_dfs) - len(visited_bfs)
        print(f"  🔍 DFS explored {abs(visited_diff)} {'more' if visited_diff > 0 else 'fewer'} nodes than BFS")
    print()


def game_loop() -> None:
    """
    Game: Monster Chase (Turn-Based)
    P = player, M = monster, G = exit, # = walls, . = floor
    """
    # Clear screen for better gameplay
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print_banner()
    print("\n" + "=" * 60)
    print("🎮 MONSTER CHASE - Turn Based Game")
    print("=" * 60)
    
    # Parse game map
    lines = [line for line in GAME_MAP.split('\n') if line.strip()]
    grid = [list(line) for line in lines]
    
    # Find player, monster, and goal positions
    player_pos = None
    monster_pos = None
    goal_pos = None
    
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'P':
                player_pos = (r, c)
                grid[r][c] = '.'  # Convert to floor
            elif cell == 'M':
                monster_pos = (r, c)
                grid[r][c] = '.'  # Convert to floor
            elif cell == 'G':
                goal_pos = (r, c)
                # Keep G as is
    
    # Verify all required elements are present
    if not player_pos:
        print("❌ Error: Could not find player (P) on map")
        print("Make sure the map contains exactly one 'P'")
        input("\nPress Enter to return to menu...")
        return
    
    if not monster_pos:
        print("❌ Error: Could not find monster (M) on map")
        print("Make sure the map contains exactly one 'M'")
        input("\nPress Enter to return to menu...")
        return
    
    if not goal_pos:
        print("❌ Error: Could not find goal (G) on map")
        print("Make sure the map contains exactly one 'G'")
        input("\nPress Enter to return to menu...")
        return
    
    # Game settings
    print("\nChoose monster AI:")
    print("  [B] BFS - Smart monster (always takes shortest path) - HARD MODE")
    print("  [D] DFS - Dumb monster (may wander aimlessly) - EASY MODE")
    
    choice = input("\nYour choice (B/D): ").strip().upper()
    mode = "BFS" if choice == 'B' else "DFS"
    
    print("\n" + "=" * 60)
    print(f"🤖 Monster AI: {mode}")
    print("\n🎮 Controls:")
    print("  W - Move Up")
    print("  A - Move Left")
    print("  S - Move Down")
    print("  D - Move Right")
    print("  Q - Quit game")
    print("=" * 60)
    
    turns = 0
    moves_made = 0
    
    while True:
        # Clear screen for each turn (optional)
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        # Render current state
        game_render = [row[:] for row in grid]
        pr, pc = player_pos
        mr, mc = monster_pos
        gr, gc = goal_pos
        
        game_render[pr][pc] = 'P'
        game_render[mr][mc] = 'M'
        game_render[gr][gc] = 'G'
        
        print(f"\n📊 Turn {turns} | Moves made: {moves_made}")
        print("─" * 40)
        for row in game_render:
            print(''.join(row))
        print("─" * 40)
        
        # Check win/lose conditions
        if player_pos == monster_pos:
            print("\n💀 GAME OVER - The monster caught you!")
            print(f"You survived {turns} turns and made {moves_made} moves.")
            break
        
        if player_pos == goal_pos:
            print("\n🏆 YOU WIN - You reached the exit safely!")
            print(f"Congratulations! You escaped in {turns} turns with {moves_made} moves.")
            break
        
        # Player move
        move = input("Your move (WASD): ").strip().lower()
        
        if move == 'q':
            print("\n👋 Game quit. Thanks for playing!")
            break
        
        # Calculate new player position
        dr, dc = player_pos
        if move == 'w':
            dr -= 1
        elif move == 's':
            dr += 1
        elif move == 'a':
            dc -= 1
        elif move == 'd':
            dc += 1
        else:
            print("❌ Invalid move! Use W, A, S, D or Q to quit.")
            continue
        
        new_pos = (dr, dc)
        
        # Check if move is valid
        if not (0 <= dr < len(grid) and 0 <= dc < len(grid[0])):
            print("❌ Can't move there - out of bounds!")
            continue
            
        if grid[dr][dc] == '#':
            print("❌ Can't move there - wall!")
            continue
            
        if new_pos == monster_pos:
            print("❌ Can't move there - the monster is there!")
            continue
        
        # Valid move
        player_pos = new_pos
        moves_made += 1
        
        # Monster move (using chosen algorithm)
        path_func = bfs_path if mode == "BFS" else dfs_path
        monster_path, _ = path_func(grid, monster_pos, player_pos)
        
        if monster_path and len(monster_path) > 1:
            monster_pos = monster_path[1]  # Move one step along path
        
        turns += 1
    
    input("\nPress Enter to return to main menu...")


def main() -> None:
    """Main entry point."""
    print_banner()
    
    while True:
        print("\n📌 MAIN MENU")
        print("=" * 60)
        print("1. 🧪 Run pathfinding demo on all maps")
        print("2. 🎮 Play Monster Chase game")
        print("3. ❌ Exit")
        print("=" * 60)
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            run_one("Example Map 1 (Simple)", EXAMPLE_MAP_1)
            run_one("Example Map 2 (Complex)", EXAMPLE_MAP_2)
            run_one("Example Map 3 (Maze-like)", EXAMPLE_MAP_3)
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            game_loop()
        
        elif choice == '3':
            print("\n👋 Thanks for playing MonsterChase!")
            print(f"⭐ Star us on GitHub: {REPO_URL}")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for playing MonsterChase!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue on GitHub:")
        print(f"{REPO_URL}/issues")