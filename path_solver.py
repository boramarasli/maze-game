from collections import deque
import heapq
import math
from maze_generator import CellType

class PathSolver:
    """Implements various pathfinding algorithms for maze solving"""
    
    def __init__(self, maze):
        self.maze = maze
        self.algorithm_name = "BFS"
    
    def solve_bfs(self):
        """Breadth-First Search - guarantees shortest path"""
        self.algorithm_name = "BFS"
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            (row, col), path = queue.popleft()
            
            if (row, col) == end:
                return path
            
            # Mark as visited for visualization
            if self.maze.grid[row][col].cell_type == CellType.PATH:
                self.maze.grid[row][col].cell_type = CellType.VISITED
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in neighbors:
                if (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    new_path = path + [(next_row, next_col)]
                    queue.append(((next_row, next_col), new_path))
        
        return []  # No path found
    
    def solve_dfs(self):
        """Depth-First Search - may not find shortest path but faster"""
        self.algorithm_name = "DFS"
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (row, col), path = stack.pop()
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            
            if (row, col) == end:
                return path
            
            # Mark as visited for visualization
            if self.maze.grid[row][col].cell_type == CellType.PATH:
                self.maze.grid[row][col].cell_type = CellType.VISITED
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in neighbors:
                if (next_row, next_col) not in visited:
                    new_path = path + [(next_row, next_col)]
                    stack.append(((next_row, next_col), new_path))
        
        return []  # No path found
    
    def solve_astar(self):
        """A* Algorithm - optimal pathfinding with heuristic"""
        self.algorithm_name = "A*"
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        # Priority queue: (f_score, g_score, position, path)
        heap = [(0, 0, start, [start])]
        visited = set()
        g_scores = {start: 0}
        
        while heap:
            f_score, g_score, (row, col), path = heapq.heappop(heap)
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            
            if (row, col) == end:
                return path
            
            # Mark as visited for visualization
            if self.maze.grid[row][col].cell_type == CellType.PATH:
                self.maze.grid[row][col].cell_type = CellType.VISITED
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in neighbors:
                if (next_row, next_col) not in visited:
                    tentative_g = g_score + 1
                    
                    if ((next_row, next_col) not in g_scores or 
                        tentative_g < g_scores[(next_row, next_col)]):
                        
                        g_scores[(next_row, next_col)] = tentative_g
                        h_score = self._manhattan_distance((next_row, next_col), end)
                        f_score = tentative_g + h_score
                        new_path = path + [(next_row, next_col)]
                        
                        heapq.heappush(heap, (f_score, tentative_g, 
                                            (next_row, next_col), new_path))
        
        return []  # No path found
    
    def _manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance heuristic for A*"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def _euclidean_distance(self, pos1, pos2):
        """Calculate Euclidean distance heuristic (alternative for A*)"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def solve_maze(self, algorithm='BFS'):
        """Solve maze using specified algorithm"""
        # Reset maze state
        self.maze.reset_visited()
        
        if algorithm == 'BFS':
            path = self.solve_bfs()
        elif algorithm == 'DFS':
            path = self.solve_dfs()
        elif algorithm == 'A*':
            path = self.solve_astar()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        if path:
            # Mark solution path
            self.maze.mark_solution_path(path)
            return path
        else:
            print(f"No solution found using {algorithm}")
            return []
    
    def get_step_by_step_solution(self, algorithm='BFS'):
        """Get solution path step by step for animation"""
        # This is a modified version that returns each step
        self.maze.reset_visited()
        
        if algorithm == 'BFS':
            return self._bfs_step_by_step()
        elif algorithm == 'DFS':
            return self._dfs_step_by_step()
        elif algorithm == 'A*':
            return self._astar_step_by_step()
        else:
            return []
    
    def _bfs_step_by_step(self):
        """BFS that returns each step for animation"""
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        queue = deque([(start, [start])])
        visited = set([start])
        steps = []
        
        while queue:
            (row, col), path = queue.popleft()
            steps.append(('visit', row, col, len(path)))
            
            if (row, col) == end:
                steps.append(('solution', path))
                return steps
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in neighbors:
                if (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    new_path = path + [(next_row, next_col)]
                    queue.append(((next_row, next_col), new_path))
        
        return steps
    
    def _dfs_step_by_step(self):
        """DFS that returns each step for animation"""
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        stack = [(start, [start])]
        visited = set()
        steps = []
        
        while stack:
            (row, col), path = stack.pop()
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            steps.append(('visit', row, col, len(path)))
            
            if (row, col) == end:
                steps.append(('solution', path))
                return steps
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in reversed(neighbors):  # Reverse for consistent order
                if (next_row, next_col) not in visited:
                    new_path = path + [(next_row, next_col)]
                    stack.append(((next_row, next_col), new_path))
        
        return steps
    
    def _astar_step_by_step(self):
        """A* that returns each step for animation"""
        start = self.maze.start_pos
        end = self.maze.end_pos
        
        heap = [(0, 0, start, [start])]
        visited = set()
        g_scores = {start: 0}
        steps = []
        
        while heap:
            f_score, g_score, (row, col), path = heapq.heappop(heap)
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            steps.append(('visit', row, col, len(path)))
            
            if (row, col) == end:
                steps.append(('solution', path))
                return steps
            
            neighbors = self.maze.get_neighbors_for_pathfinding(row, col)
            for next_row, next_col in neighbors:
                if (next_row, next_col) not in visited:
                    tentative_g = g_score + 1
                    
                    if ((next_row, next_col) not in g_scores or 
                        tentative_g < g_scores[(next_row, next_col)]):
                        
                        g_scores[(next_row, next_col)] = tentative_g
                        h_score = self._manhattan_distance((next_row, next_col), end)
                        f_score = tentative_g + h_score
                        new_path = path + [(next_row, next_col)]
                        
                        heapq.heappush(heap, (f_score, tentative_g, 
                                            (next_row, next_col), new_path))
        
        return steps