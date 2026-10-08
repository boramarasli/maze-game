from maze_generator import CellType

class Player:
    """Handles player movement and position in the maze"""
    
    def __init__(self, maze):
        self.maze = maze
        self.row, self.col = maze.start_pos
        self.moves_count = 0
        self.move_history = [maze.start_pos]
        self.player_id = "Player"
    
    def reset_position(self):
        """Reset player to starting position"""
        self.row, self.col = self.maze.start_pos
        self.moves_count = 0
        self.move_history = [self.maze.start_pos]
    
    def move(self, direction):
        """Move player in specified direction if valid"""
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        
        if direction in directions:
            dr, dc = directions[direction]
            new_row = self.row + dr
            new_col = self.col + dc
            
            if self.maze.is_valid_move(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.moves_count += 1
                self.move_history.append((new_row, new_col))
                return True
        return False
    
    def get_position(self):
        """Get current player position"""
        return (self.row, self.col)
    
    def is_at_goal(self):
        """Check if player has reached the end"""
        return (self.row, self.col) == self.maze.end_pos
    
    def get_moves_count(self):
        """Get number of moves made"""
        return self.moves_count
    
    def get_move_history(self):
        """Get history of all moves"""
        return self.move_history.copy()

class AIPlayer(Player):
    """AI player that can follow a predetermined path"""
    
    def __init__(self, maze):
        super().__init__(maze)
        self.ai_path = []
        self.current_step = 0
        self.is_solving = False
    
    def set_path(self, path):
        """Set the path for AI to follow"""
        self.ai_path = path
        self.current_step = 0
        self.reset_position()
    
    def next_step(self):
        """Move AI to next step in path"""
        if self.current_step < len(self.ai_path) - 1:
            self.current_step += 1
            next_pos = self.ai_path[self.current_step]
            self.row, self.col = next_pos
            self.move_history.append(next_pos)
            self.moves_count += 1
            return True
        return False
    
    def is_path_complete(self):
        """Check if AI has completed its path"""
        return self.current_step >= len(self.ai_path) - 1
    
    def is_at_goal(self):
        """Check if AI has reached the goal"""
        return (self.row, self.col) == self.maze.end_pos

class MultiPlayer:
    """Handles two-player multiplayer mode"""
    
    def __init__(self, maze):
        self.maze = maze
        self.player1 = Player(maze)
        self.player2 = Player(maze)
        self.player1.player_id = "Player 1"
        self.player2.player_id = "Player 2"
        self.is_multiplayer_mode = False
        self.game_finished = False
        self.winner = None
        
        # Player 1 controls: WASD
        self.player1_controls = {
            'w': 'up', 'W': 'up',
            's': 'down', 'S': 'down', 
            'a': 'left', 'A': 'left',
            'd': 'right', 'D': 'right'
        }
        
        # Player 2 controls: Arrow keys
        self.player2_controls = {
            'Up': 'up',
            'Down': 'down',
            'Left': 'left', 
            'Right': 'right'
        }
    
    def start_multiplayer_game(self):
        """Start a new multiplayer game"""
        self.player1.reset_position()
        self.player2.reset_position()
        self.is_multiplayer_mode = True
        self.game_finished = False
        self.winner = None
    
    def stop_multiplayer_game(self):
        """Stop multiplayer mode"""
        self.is_multiplayer_mode = False
        self.game_finished = False
        self.winner = None
    
    def handle_key_press(self, key):
        """Handle key press for both players"""
        if not self.is_multiplayer_mode or self.game_finished:
            return False
        
        moved = False
        
        # Player 1 controls (WASD)
        if key in self.player1_controls:
            direction = self.player1_controls[key]
            if self.player1.move(direction):
                moved = True
                if self.player1.is_at_goal():
                    self.winner = "Player 1"
                    self.game_finished = True
        
        # Player 2 controls (Arrow keys)
        elif key in self.player2_controls:
            direction = self.player2_controls[key]
            if self.player2.move(direction):
                moved = True
                if self.player2.is_at_goal():
                    self.winner = "Player 2"
                    self.game_finished = True
        
        return moved
    
    def get_game_status(self):
        """Get current game status"""
        if self.game_finished:
            return f"{self.winner} Wins!"
        elif self.is_multiplayer_mode:
            return f"P1 Moves: {self.player1.get_moves_count()} | P2 Moves: {self.player2.get_moves_count()}"
        else:
            return "Single Player Mode"
    
    def get_both_positions(self):
        """Get positions of both players"""
        return self.player1.get_position(), self.player2.get_position()

class GameStats:
    """Track game statistics"""
    
    def __init__(self):
        self.reset_stats()
    
    def reset_stats(self):
        """Reset all statistics"""
        self.games_played = 0
        self.games_won = 0
        self.total_moves = 0
        self.best_score = float('inf')
        self.average_moves = 0
        
        # Multiplayer stats
        self.multiplayer_games = 0
        self.player1_wins = 0
        self.player2_wins = 0
    
    def start_game(self):
        """Start tracking a new game"""
        import time
        self.start_time = time.time()
    
    def end_game(self, moves, won=True):
        """End current game and update statistics"""
        self.games_played += 1
        if won:
            self.games_won += 1
            self.total_moves += moves
            if moves < self.best_score:
                self.best_score = moves
        
        if self.games_won > 0:
            self.average_moves = self.total_moves / self.games_won
    
    def end_multiplayer_game(self, winner, player1_moves, player2_moves):
        """End multiplayer game and update stats"""
        self.multiplayer_games += 1
        if winner == "Player 1":
            self.player1_wins += 1
        elif winner == "Player 2":
            self.player2_wins += 1
    
    def get_win_rate(self):
        """Calculate win percentage"""
        if self.games_played == 0:
            return 0
        return (self.games_won / self.games_played) * 100
    
    def get_multiplayer_stats(self):
        """Get multiplayer statistics"""
        if self.multiplayer_games == 0:
            return "No multiplayer games played"
        
        p1_rate = (self.player1_wins / self.multiplayer_games) * 100
        p2_rate = (self.player2_wins / self.multiplayer_games) * 100
        
        return f"Multiplayer: {self.multiplayer_games} games | P1: {p1_rate:.1f}% | P2: {p2_rate:.1f}%"
    
    def get_stats_dict(self):
        """Get statistics as dictionary"""
        return {
            'games_played': self.games_played,
            'games_won': self.games_won,
            'win_rate': self.get_win_rate(),
            'best_score': self.best_score if self.best_score != float('inf') else 0,
            'average_moves': round(self.average_moves, 1),
            'multiplayer_games': self.multiplayer_games,
            'player1_wins': self.player1_wins,
            'player2_wins': self.player2_wins
        }