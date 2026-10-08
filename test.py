try:
    from maze_generator import Maze
    print("✅ maze_generator.py works!")
    
    maze = Maze(11, 11)
    print("✅ Maze creation works!")
    
except ImportError as e:
    print(f"❌ Error importing: {e}")
except Exception as e:
    print(f"❌ Error: {e}")