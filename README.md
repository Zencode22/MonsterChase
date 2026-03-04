# 🏃 MonsterChase - BFS vs DFS Pathfinding Showdown

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/MonsterChase?style=social)](https://github.com/yourusername/MonsterChase)

**MonsterChase** is an educational Python project that demonstrates the fundamental differences between Breadth-First Search (BFS) and Depth-First Search (DFS) pathfinding algorithms through interactive examples and a turn-based game.

## 🎯 Learning Objectives

- Implement BFS using a queue (`collections.deque`)
- Implement DFS using an explicit stack (no recursion)
- Understand path reconstruction using parent pointers
- Compare algorithm behavior: shortest-path guarantee vs exploration patterns
- See theoretical concepts in action through a playable game

## ✨ Features

- 📊 **Interactive Demo Mode**: Run BFS and DFS on multiple pre-built maps
- 🎮 **Monster Chase Game**: Turn-based strategy where monster uses either BFS or DFS
- 🗺️ **Multiple Maps**: From simple corridors to complex mazes
- 🔍 **Visual Output**: Paths marked with `*`, visited nodes with `·`
- 📈 **Performance Metrics**: Compare path lengths, visited nodes, and execution time

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/MonsterChase.git
cd MonsterChase

# Run the program
python pathfinding.py