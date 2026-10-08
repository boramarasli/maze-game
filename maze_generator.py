import random
from enum import Enum

class CellType(Enum):
    WALL = 0
    PATH = 1
    START = 2
    END = 3
    VISITED = 4
    SOLUTION = 5

class Cell:
    """Represents a single cell in the maze"""
    def __init__(self, row, col, cell_type=CellType.WALL):
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

class Maze:
    """Main maze class that generates and manages the maze structure"""
    
    def __init__(self, width=21, height=21):
        # Ensure odd dimensions for proper maze generation
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid = []
        self.start_pos = (1, 1)
        self.end_pos = (self.height - 2, self.width - 2)
        self.solution_path = []
        self.generate_maze()
    
    def generate_maze(self):
        """Generate maze using recursive backtracking (DFS-based)"""
        # Initialize grid with walls
        self.grid = [[Cell(row, col, CellType.WALL) 
                     for col in range(self.width)] 
                     for row in range(self.height)]
        
        # Set all cells as walls initially
        for row in range(self.height):
            for col in range(self.width):
                if row % 2 == 1 and col % 2 == 1:
                    self.grid[row][col].cell_type = CellType.PATH
        
        # Start recursive backtracking from (1,1)
        self._recursive_backtrack(1, 1)
        
        # Set start and end positions
        self.grid[self.start_pos[0]][self.start_pos[1]].cell_type = CellType.START
        self.grid[self.end_pos[0]][self.end_pos[1]].cell_type = CellType.END
    
    def _recursive_backtrack(self, row, col):
        """Recursive backtracking algorithm for maze generation"""
        self.grid[row][col].visited = True
        
        # Get neighbors in random order
        neighbors = self._get_neighbors(row, col)
        random.shuffle(neighbors)
        
        for next_row, next_col in neighbors:
            if not self.grid[next_row][next_col].visited:
                # Remove wall between current cell and neighbor
                wall_row = row + (next_row - row) // 2
                wall_col = col + (next_col - col) // 2
                self.grid[wall_row][wall_col].cell_type = CellType.PATH
                
                # Recursively visit neighbor
                self._recursive_backtrack(next_row, next_col)
    
    def _get_neighbors(self, row, col):
        """Get valid neighboring cells for maze generation"""
        neighbors = []
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]  # Right, Left, Down, Up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 < new_row < self.height - 1 and 
                0 < new_col < self.width - 1):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def get_neighbors_for_pathfinding(self, row, col):
        """Get valid neighbors for pathfinding (adjacent cells)"""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.height and 
                0 <= new_col < self.width and
                self.grid[new_row][new_col].cell_type in [CellType.PATH, CellType.END]):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def is_valid_move(self, row, col):
        """Check if a move to the given position is valid"""
        if (0 <= row < self.height and 
            0 <= col < self.width):
            cell_type = self.grid[row][col].cell_type
            return cell_type in [CellType.PATH, CellType.START, CellType.END, CellType.VISITED]
        return False
    
    def reset_visited(self):
        """Reset visited status for pathfinding"""
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col].cell_type == CellType.VISITED:
                    self.grid[row][col].cell_type = CellType.PATH
                self.grid[row][col].visited = False
        self.solution_path = []
    
    def mark_solution_path(self, path):
        """Mark the solution path on the maze"""
        self.solution_path = path
        for row, col in path:
            if self.grid[row][col].cell_type == CellType.PATH:
                self.grid[row][col].cell_type = CellType.SOLUTION
    
    def clear_solution_path(self):
        """Clear the solution path visualization"""
        for row, col in self.solution_path:
            if self.grid[row][col].cell_type == CellType.SOLUTION:
                self.grid[row][col].cell_type = CellType.PATH
        self.solution_path = []
    
    def get_difficulty_size(self, difficulty):
        """Get maze size based on difficulty level"""
        sizes = {
            'Easy': (15, 15),
            'Medium': (25, 25), 
            'Hard': (35, 35)
        }
        return sizes.get(difficulty, (21, 21))
    
    def regenerate_maze(self, difficulty='Medium'):
        """Regenerate maze with new difficulty"""
        new_height, new_width = self.get_difficulty_size(difficulty)
        self.width = new_width if new_width % 2 == 1 else new_width + 1
        self.height = new_height if new_height % 2 == 1 else new_height + 1
        self.start_pos = (1, 1)
        self.end_pos = (self.height - 2, self.width - 2)
        self.solution_path = []
        self.generate_maze()
    
    def print_maze(self):
        """Print maze to console for debugging"""
        symbols = {
            CellType.WALL: '██',
            CellType.PATH: '  ',
            CellType.START: 'S ',
            CellType.END: 'E ',
            CellType.VISITED: '··',
            CellType.SOLUTION: '**'
        }
        
        for row in self.grid:
            print(''.join(symbols[cell.cell_type] for cell in row))
