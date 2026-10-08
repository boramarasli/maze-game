#!/usr/bin/env python3
"""
Intelligent Maze Challenge
Main entry point for the maze game application

This application demonstrates:
- Python programming fundamentals
- Object-Oriented Programming (OOP)
- Data structures and algorithms (BFS, DFS, A*)
- GUI development with Tkinter
- Modular code design

Authors: Vivienne Josephine Hoffmann, Yelizaveta Selivanova, Bora Marasli
Date: 2024
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import MazeGUI
    from maze_generator import Maze, CellType
    from path_solver import PathSolver
    from player import Player, AIPlayer, GameStats
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required files are in the same directory:")
    print("- main.py")
    print("- maze_generator.py")
    print("- path_solver.py") 
    print("- player.py")
    print("- gui.py")
    print("- utils.py (optional)")
    sys.exit(1)

def main():
    """Main function to start the maze game"""
    print("=" * 50)
    print("Welcome to the Intelligent Maze Challenge!")
    print("=" * 50)
    print("Loading game components...")
    
    try:
        # Test maze generation
        print("✓ Testing maze generation...")
        test_maze = Maze(15, 15)
        
        # Test pathfinding
        print("✓ Testing pathfinding algorithms...")
        test_solver = PathSolver(test_maze)
        bfs_path = test_solver.solve_maze('BFS')
        test_maze.reset_visited()
        dfs_path = test_solver.solve_maze('DFS')
        test_maze.reset_visited()
        astar_path = test_solver.solve_maze('A*')
        
        print(f"  - BFS found path of length: {len(bfs_path)}")
        print(f"  - DFS found path of length: {len(dfs_path)}")
        print(f"  - A* found path of length: {len(astar_path)}")
        
        # Test player controls
        print("✓ Testing player controls...")
        test_player = Player(test_maze)
        test_ai = AIPlayer(test_maze)
        test_stats = GameStats()
        
        print("✓ All components loaded successfully!")
        print("\nStarting GUI...")
        
        # Start the GUI application
        app = MazeGUI()
        app.run()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def run_console_demo():
    """Run a console-based demo of the maze solver"""
    print("\n" + "=" * 50)
    print("Console Demo Mode")
    print("=" * 50)
    
    # Create a smaller maze for console display
    maze = Maze(15, 15)
    solver = PathSolver(maze)
    
    print("\nGenerated Maze:")
    maze.print_maze()
    
    print(f"\nStart: {maze.start_pos}")
    print(f"End: {maze.end_pos}")
    
    # Test all algorithms
    algorithms = ['BFS', 'DFS', 'A*']
    for algorithm in algorithms:
        print(f"\nSolving with {algorithm}...")
        maze.reset_visited()
        path = solver.solve_maze(algorithm)
        
        if path:
            print(f"✓ {algorithm} found solution with {len(path)} steps")
            print("Solution path:")
            maze.print_maze()
            maze.clear_solution_path()
        else:
            print(f"❌ {algorithm} could not find solution")

def print_usage():
    """Print usage information"""
    print("Intelligent Maze Challenge")
    print("Usage: python main.py [option]")
    print("\nOptions:")
    print("  (no args)  - Start GUI application (default)")
    print("  --demo     - Run console demo")
    print("  --help     - Show this help message")
    print("  --test     - Run component tests")

def run_tests():
    """Run basic component tests"""
    print("Running component tests...")
    
    # Test maze generation
    print("\n1. Testing Maze Generation:")
    try:
        maze = Maze(21, 21)
        assert maze.width == 21
        assert maze.height == 21
        assert maze.start_pos == (1, 1)
        assert maze.end_pos == (19, 19)
        print("✓ Maze generation test passed")
    except Exception as e:
        print(f"❌ Maze generation test failed: {e}")
    
    # Test pathfinding
    print("\n2. Testing Pathfinding:")
    try:
        solver = PathSolver(maze)
        path = solver.solve_maze('BFS')
        assert len(path) > 0
        assert path[0] == maze.start_pos
        assert path[-1] == maze.end_pos
        print("✓ Pathfinding test passed")
    except Exception as e:
        print(f"❌ Pathfinding test failed: {e}")
    
    # Test player movement
    print("\n3. Testing Player Movement:")
    try:
        player = Player(maze)
        initial_pos = player.get_position()
        assert initial_pos == maze.start_pos
        
        # Test valid moves
        valid_moves = player.get_valid_moves()
        assert len(valid_moves) > 0
        print("✓ Player movement test passed")
    except Exception as e:
        print(f"❌ Player movement test failed: {e}")
    
    # Test AI player
    print("\n4. Testing AI Player:")
    try:
        ai = AIPlayer(maze)
        ai.set_path(path)
        assert ai.ai_path == path
        print("✓ AI player test passed")
    except Exception as e:
        print(f"❌ AI player test failed: {e}")
    
    print("\n✓ All tests completed!")

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--help', '-h']:
            print_usage()
        elif arg in ['--demo', '-d']:
            run_console_demo()
        elif arg in ['--test', '-t']:
            run_tests()
        else:
            print(f"Unknown argument: {arg}")
            print_usage()
    else:
        # Default: start GUI application
        main()