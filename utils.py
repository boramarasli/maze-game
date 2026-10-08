
"""
Utility functions and helper classes for the Maze Challenge application
"""

import json
import time
import os
import math
from typing import List, Tuple, Dict, Any

def save_game_state(maze, player, filename="saved_game.json"):
    """Save current game state to file"""
    try:
        game_state = {
            'maze_width': maze.width,
            'maze_height': maze.height,
            'start_pos': maze.start_pos,
            'end_pos': maze.end_pos,
            'player_position': player.get_position(),
            'player_moves': player.get_moves_count(),
            'timestamp': time.time()
        }
        
        # Save maze grid state
        grid_state = []
        for row in range(maze.height):
            row_state = []
            for col in range(maze.width):
                cell = maze.grid[row][col]
                row_state.append(cell.cell_type.value)
            grid_state.append(row_state)
        
        game_state['grid_state'] = grid_state
        
        with open(filename, 'w') as f:
            json.dump(game_state, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving game state: {e}")
        return False

def load_game_state(filename="saved_game.json"):
    """Load game state from file"""
    try:
        if not os.path.exists(filename):
            return None
        
        with open(filename, 'r') as f:
            game_state = json.load(f)
        
        return game_state
    except Exception as e:
        print(f"Error loading game state: {e}")
        return None

def calculate_manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calculate_euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two positions"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_direction_from_positions(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> str:
    """Get direction string from two positions"""
    dr = to_pos[0] - from_pos[0]
    dc = to_pos[1] - from_pos[1]
    
    if dr == -1 and dc == 0:
        return 'up'
    elif dr == 1 and dc == 0:
        return 'down'
    elif dr == 0 and dc == -1:
        return 'left'
    elif dr == 0 and dc == 1:
        return 'right'
    else:
        return 'unknown'

def path_to_directions(path: List[Tuple[int, int]]) -> List[str]:
    """Convert a path of positions to a list of direction strings"""
    if len(path) < 2:
        return []
    
    directions = []
    for i in range(len(path) - 1):
        direction = get_direction_from_positions(path[i], path[i + 1])
        directions.append(direction)
    
    return directions

def validate_path(maze, path: List[Tuple[int, int]]) -> bool:
    """Validate if a path is valid for the given maze"""
    if not path:
        return False
    
    # Check if path starts at start position
    if path[0] != maze.start_pos:
        return False
    
    # Check if path ends at end position
    if path[-1] != maze.end_pos:
        return False
    
    # Check if each step is valid
    for i in range(len(path) - 1):
        current = path[i]
        next_pos = path[i + 1]
        
        # Check if positions are adjacent
        distance = calculate_manhattan_distance(current, next_pos)
        if distance != 1:
            return False
        
        # Check if next position is valid
        if not maze.is_valid_move(next_pos[0], next_pos[1]):
            return False
    
    return True

def optimize_path(path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Remove unnecessary steps from a path (basic optimization)"""
    if len(path) <= 2:
        return path
    
    optimized = [path[0]]
    
    for i in range(1, len(path) - 1):
        current = path[i]
        prev_pos = optimized[-1]
        next_pos = path[i + 1]
        
        # Check if we can skip current position (if it's in a straight line)
        if not is_collinear(prev_pos, current, next_pos):
            optimized.append(current)
    
    optimized.append(path[-1])
    return optimized

def is_collinear(pos1: Tuple[int, int], pos2: Tuple[int, int], pos3: Tuple[int, int]) -> bool:
    """Check if three positions are collinear (in a straight line)"""
    # For grid-based movement, positions are collinear if they form a straight line
    # horizontally or vertically
    return ((pos1[0] == pos2[0] == pos3[0]) or  # Same row
            (pos1[1] == pos2[1] == pos3[1]))    # Same column

def format_time(seconds: float) -> str:
    """Format time in seconds to human-readable string"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs:.1f}s"

def generate_maze_seed() -> int:
    """Generate a random seed for maze generation"""
    import random
    return random.randint(1, 1000000)

def set_maze_seed(seed: int):
    """Set the random seed for reproducible maze generation"""
    import random
    random.seed(seed)

class PerformanceProfiler:
    """Simple performance profiler for algorithm comparison"""
    
    def __init__(self):
        self.results = {}
    
    def profile_algorithm(self, algorithm_name: str, algorithm_func, *args, **kwargs):
        """Profile an algorithm and store results"""
        start_time = time.time()
        result = algorithm_func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        self.results[algorithm_name] = {
            'execution_time': execution_time,
            'result': result,
            'timestamp': time.time()
        }
        
        return result
    
    def get_performance_report(self) -> str:
        """Get formatted performance report"""
        if not self.results:
            return "No profiling data available"
        
        report = "Algorithm Performance Report\n"
        report += "=" * 40 + "\n"
        
        # Sort by execution time
        sorted_results = sorted(self.results.items(), 
                              key=lambda x: x[1]['execution_time'])
        
        for name, data in sorted_results:
            time_str = format_time(data['execution_time'])
            report += f"{name}: {time_str}\n"
        
        return report
    
    def clear_results(self):
        """Clear all profiling results"""
        self.results.clear()

class MazeStatistics:
    """Collect and analyze maze statistics"""
    
    def __init__(self):
        self.reset_stats()
    
    def reset_stats(self):
        """Reset all statistics"""
        self.total_cells = 0
        self.wall_cells = 0
        self.path_cells = 0
        self.dead_ends = 0
        self.longest_path = 0
        self.branching_factor = 0
    
    def analyze_maze(self, maze):
        """Analyze maze and collect statistics"""
        self.reset_stats()
        
        self.total_cells = maze.width * maze.height
        
        # Count cell types
        for row in range(maze.height):
            for col in range(maze.width):
                cell_type = maze.grid[row][col].cell_type
                if cell_type.value == 0:  # Wall
                    self.wall_cells += 1
                else:  # Path
                    self.path_cells += 1
        
        # Count dead ends
        self._count_dead_ends(maze)
        
        # Calculate other metrics
        self.branching_factor = self._calculate_branching_factor(maze)
    
    def _count_dead_ends(self, maze):
        """Count dead ends in the maze"""
        self.dead_ends = 0
        
        for row in range(maze.height):
            for col in range(maze.width):
                if maze.grid[row][col].cell_type.value != 0:  # Not a wall
                    neighbors = maze.get_neighbors_for_pathfinding(row, col)
                    if len(neighbors) == 1:  # Dead end has only one neighbor
                        self.dead_ends += 1
    
    def _calculate_branching_factor(self, maze):
        """Calculate average branching factor"""
        total_branches = 0
        junction_count = 0
        
        for row in range(maze.height):
            for col in range(maze.width):
                if maze.grid[row][col].cell_type.value != 0:  # Not a wall
                    neighbors = maze.get_neighbors_for_pathfinding(row, col)
                    if len(neighbors) > 2:  # Junction
                        total_branches += len(neighbors)
                        junction_count += 1
        
        return total_branches / junction_count if junction_count > 0 else 0
    
    def get_statistics_dict(self) -> Dict[str, Any]:
        """Get statistics as dictionary"""
        return {
            'total_cells': self.total_cells,
            'wall_cells': self.wall_cells,
            'path_cells': self.path_cells,
            'wall_percentage': (self.wall_cells / self.total_cells) * 100,
            'path_percentage': (self.path_cells / self.total_cells) * 100,
            'dead_ends': self.dead_ends,
            'branching_factor': round(self.branching_factor, 2)
        }

def export_maze_to_text(maze, filename="maze_export.txt"):
    """Export maze to text file"""
    try:
        from maze_generator import CellType
        
        symbols = {
            CellType.WALL: '██',
            CellType.PATH: '  ',
            CellType.START: 'S ',
            CellType.END: 'E ',
            CellType.VISITED: '··',
            CellType.SOLUTION: '**'
        }
        
        with open(filename, 'w') as f:
            f.write(f"Maze Export - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Size: {maze.width} x {maze.height}\n")
            f.write(f"Start: {maze.start_pos}\n")
            f.write(f"End: {maze.end_pos}\n")
            f.write("-" * 50 + "\n")
            
            for row in maze.grid:
                line = ''.join(symbols.get(cell.cell_type, '??') for cell in row)
                f.write(line + '\n')
        
        return True
    except Exception as e:
        print(f"Error exporting maze: {e}")
        return False