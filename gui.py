import tkinter as tk
from tkinter import ttk, messagebox
import time
from maze_generator import Maze, CellType
from path_solver import PathSolver
from player import Player, AIPlayer, GameStats, MultiPlayer

class MazeGUI:
    """Main GUI class for the Maze Challenge application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Intelligent Maze Challenge")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Initialize game components
        self.maze = Maze(21, 21)
        self.solver = PathSolver(self.maze)
        self.player = Player(self.maze)
        self.ai_player = AIPlayer(self.maze)
        self.multiplayer = MultiPlayer(self.maze)  # Add multiplayer support
        self.stats = GameStats()
        
        # GUI variables
        self.cell_size = 20
        self.canvas_width = 600
        self.canvas_height = 600
        self.current_difficulty = 'Medium'
        self.current_algorithm = 'BFS'
        self.ai_mode = False
        self.multiplayer_mode = False  # Add multiplayer mode flag
        self.ai_speed = 200
        self.show_solution = False
        
        # Colors
        self.colors = {
            CellType.WALL: '#2C3E50',
            CellType.PATH: '#ECF0F1',
            CellType.START: '#27AE60',
            CellType.END: '#E74C3C',
            CellType.VISITED: '#F39C12',
            CellType.SOLUTION: '#9B59B6',
            'PLAYER': '#3498DB',
            'PLAYER1': '#FF6B6B',  # Red for Player 1
            'PLAYER2': '#4ECDC4'   # Teal for Player 2
        }
        
        self.setup_gui()
        self.update_canvas()
        self.stats.start_game()
        
        # Bind keyboard events
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()
    
    def setup_gui(self):
        """Setup the GUI layout and components"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel for maze canvas
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Canvas for maze
        self.canvas = tk.Canvas(left_frame, width=self.canvas_width, 
                               height=self.canvas_height, bg='white')
        self.canvas.pack(pady=10)
        
        # Right panel for controls
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        
        self.setup_control_panel(right_frame)
    
    def setup_control_panel(self, parent):
        """Setup the control panel with buttons and options"""
        # Title
        title_label = ttk.Label(parent, text="Maze Controls", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Game controls frame
        game_frame = ttk.LabelFrame(parent, text="Game Controls")
        game_frame.pack(fill='x', pady=5)
        
        # Start/Reset button
        self.start_button = ttk.Button(game_frame, text="New Game", 
                                      command=self.new_game)
        self.start_button.pack(fill='x', pady=2)
        
        # Reset button
        reset_button = ttk.Button(game_frame, text="Reset Position", 
                                 command=self.reset_player)
        reset_button.pack(fill='x', pady=2)
        
        # Difficulty frame
        diff_frame = ttk.LabelFrame(parent, text="Difficulty")
        diff_frame.pack(fill='x', pady=5)
        
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        difficulties = ['Easy', 'Medium', 'Hard']
        
        for diff in difficulties:
            ttk.Radiobutton(diff_frame, text=diff, variable=self.difficulty_var,
                           value=diff, command=self.change_difficulty).pack(anchor='w')
        
        # Multiplayer Controls frame
        multiplayer_frame = ttk.LabelFrame(parent, text="Multiplayer Mode")
        multiplayer_frame.pack(fill='x', pady=5)
        
        self.multiplayer_button = ttk.Button(multiplayer_frame, text="Start 2-Player", 
                                           command=self.toggle_multiplayer_mode)
        self.multiplayer_button.pack(fill='x', pady=2)
        
        # Multiplayer instructions
        mp_instructions = """Player 1: W A S D
Player 2: Arrow Keys
First to reach the end wins!"""
        ttk.Label(multiplayer_frame, text=mp_instructions, 
                 font=('Arial', 8), justify='left').pack(pady=2)
        
        # AI Controls frame
        ai_frame = ttk.LabelFrame(parent, text="AI Solver")
        ai_frame.pack(fill='x', pady=5)
        
        # Algorithm selection
        ttk.Label(ai_frame, text="Algorithm:").pack(anchor='w')
        self.algorithm_var = tk.StringVar(value=self.current_algorithm)
        algorithm_combo = ttk.Combobox(ai_frame, textvariable=self.algorithm_var,
                                      values=['BFS', 'DFS', 'A*'], state='readonly')
        algorithm_combo.pack(fill='x', pady=2)
        algorithm_combo.bind('<<ComboboxSelected>>', self.change_algorithm)
        
        # AI buttons
        self.solve_button = ttk.Button(ai_frame, text="Show Solution", 
                                      command=self.toggle_solution)
        self.solve_button.pack(fill='x', pady=2)
        
        self.ai_button = ttk.Button(ai_frame, text="Start AI", 
                                   command=self.toggle_ai_mode)
        self.ai_button.pack(fill='x', pady=2)
        
        # AI Speed
        ttk.Label(ai_frame, text="AI Speed:").pack(anchor='w', pady=(10,0))
        self.speed_var = tk.IntVar(value=self.ai_speed)
        speed_scale = ttk.Scale(ai_frame, from_=50, to=1000, 
                               orient='horizontal', variable=self.speed_var,
                               command=self.change_ai_speed)
        speed_scale.pack(fill='x', pady=2)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(parent, text="Statistics")
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=12, width=25, 
                                 font=('Courier', 9))
        self.stats_text.pack(fill='x', pady=2)
        
        # Instructions frame
        instr_frame = ttk.LabelFrame(parent, text="Instructions")
        instr_frame.pack(fill='x', pady=5)
        
        instructions = """SINGLE PLAYER:
Use Arrow Keys to move:
↑ ↓ ← → or WASD

MULTIPLAYER:
Player 1: W A S D
Player 2: Arrow Keys

Green = Start
Red = End
Blue = Single Player
Red Circle = Player 1
Teal Square = Player 2
Purple = Solution Path
Orange = AI Exploration

Goal: Reach the red end!"""
        
        ttk.Label(instr_frame, text=instructions, 
                 justify='left', font=('Arial', 9)).pack(pady=5)
        
        # Update stats initially
        self.update_stats_display()
    
    def update_canvas(self):
        """Update the maze display on canvas"""
        self.canvas.delete("all")
        
        # Calculate cell size based on canvas and maze size
        self.cell_size = min(self.canvas_width // self.maze.width,
                            self.canvas_height // self.maze.height)
        
        # Draw maze
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_type = self.maze.grid[row][col].cell_type
                color = self.colors[cell_type]
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                           fill=color, outline='gray', width=1)
        
        # Draw players based on current mode
        if self.multiplayer_mode:
            # Draw both multiplayer players
            p1_pos = self.multiplayer.player1.get_position()
            p2_pos = self.multiplayer.player2.get_position()
            
            # Player 1 (red circle)
            px1 = p1_pos[1] * self.cell_size + 2
            py1 = p1_pos[0] * self.cell_size + 2
            px2 = px1 + self.cell_size - 4
            py2 = py1 + self.cell_size - 4
            self.canvas.create_oval(px1, py1, px2, py2, 
                                  fill=self.colors['PLAYER1'], outline='white', width=2)
            
            # Player 2 (teal square)
            px1 = p2_pos[1] * self.cell_size + 4
            py1 = p2_pos[0] * self.cell_size + 4
            px2 = px1 + self.cell_size - 8
            py2 = py1 + self.cell_size - 8
            self.canvas.create_rectangle(px1, py1, px2, py2, 
                                       fill=self.colors['PLAYER2'], outline='white', width=2)
        else:
            # Draw single player
            player_row, player_col = self.player.get_position()
            px1 = player_col * self.cell_size + 2
            py1 = player_row * self.cell_size + 2
            px2 = px1 + self.cell_size - 4
            py2 = py1 + self.cell_size - 4
            
            self.canvas.create_oval(px1, py1, px2, py2, 
                                  fill=self.colors['PLAYER'], outline='white', width=2)
            
            # Draw AI player if in AI mode
            if self.ai_mode:
                ai_row, ai_col = self.ai_player.get_position()
                ax1 = ai_col * self.cell_size + 4
                ay1 = ai_row * self.cell_size + 4
                ax2 = ax1 + self.cell_size - 8
                ay2 = ay1 + self.cell_size - 8
                
                self.canvas.create_rectangle(ax1, ay1, ax2, ay2, 
                                           fill='red', outline='white', width=2)
    
    def on_key_press(self, event):
        """Handle keyboard input for player movement"""
        # Handle multiplayer mode
        if self.multiplayer_mode:
            if self.multiplayer.handle_key_press(event.keysym):
                self.update_canvas()
                self.update_stats_display()
                
                # Check if game is finished
                if self.multiplayer.game_finished:
                    self.handle_multiplayer_victory()
            return
        
        # Handle single player mode
        if self.ai_mode:
            return  # Don't allow manual control in AI mode
        
        key_map = {
            'Up': 'up', 'w': 'up', 'W': 'up',
            'Down': 'down', 's': 'down', 'S': 'down',
            'Left': 'left', 'a': 'left', 'A': 'left',
            'Right': 'right', 'd': 'right', 'D': 'right'
        }
        
        if event.keysym in key_map:
            direction = key_map[event.keysym]
            if self.player.move(direction):
                self.update_canvas()
                self.update_stats_display()
                
                # Check if player reached the goal
                if self.player.is_at_goal():
                    self.handle_victory()
    
    def new_game(self):
        """Start a new game with current difficulty"""
        self.maze.regenerate_maze(self.current_difficulty)
        self.solver = PathSolver(self.maze)
        self.player = Player(self.maze)
        self.ai_player = AIPlayer(self.maze)
        self.multiplayer = MultiPlayer(self.maze)  # Reset multiplayer
        self.ai_mode = False
        self.multiplayer_mode = False  # Reset multiplayer mode
        self.show_solution = False
        
        # Update button states
        self.ai_button.config(text="Start AI")
        self.solve_button.config(text="Show Solution")
        self.multiplayer_button.config(text="Start 2-Player")
        
        self.update_canvas()
        self.stats.start_game()
        self.update_stats_display()
    
    def reset_player(self):
        """Reset player to starting position"""
        if self.multiplayer_mode:
            self.multiplayer.player1.reset_position()
            self.multiplayer.player2.reset_position()
        else:
            self.player.reset_position()
            self.ai_player.reset_position()
        self.update_canvas()
        self.update_stats_display()
    
    def toggle_multiplayer_mode(self):
        """Toggle multiplayer mode"""
        if self.multiplayer_mode:
            self.stop_multiplayer_mode()
        else:
            self.start_multiplayer_mode()
    
    def start_multiplayer_mode(self):
        """Start multiplayer mode"""
        # Stop other modes first
        if self.ai_mode:
            self.stop_ai_solving()
        
        self.multiplayer_mode = True
        self.multiplayer.start_multiplayer_game()
        self.multiplayer_button.config(text="Stop Multiplayer")
        
        # Disable AI controls in multiplayer
        self.ai_button.config(state='disabled')
        self.solve_button.config(state='disabled')
        
        self.update_canvas()
        self.update_stats_display()
    
    def stop_multiplayer_mode(self):
        """Stop multiplayer mode"""
        self.multiplayer_mode = False
        self.multiplayer.stop_multiplayer_game()
        self.multiplayer_button.config(text="Start 2-Player")
        
        # Re-enable AI controls
        self.ai_button.config(state='normal')
        self.solve_button.config(state='normal')
        
        self.update_canvas()
        self.update_stats_display()
    
    def handle_multiplayer_victory(self):
        """Handle multiplayer game victory"""
        winner = self.multiplayer.winner
        p1_moves = self.multiplayer.player1.get_moves_count()
        p2_moves = self.multiplayer.player2.get_moves_count()
        
        self.stats.end_multiplayer_game(winner, p1_moves, p2_moves)
        
        message = f"🎉 {winner} Wins! 🎉\n\n"
        message += f"Player 1 moves: {p1_moves}\n"
        message += f"Player 2 moves: {p2_moves}\n\n"
        message += "Would you like to play again?"
        
        if messagebox.askyesno("Multiplayer Victory!", message):
            self.new_game()
        else:
            self.stop_multiplayer_mode()
        
        self.update_stats_display()
    
    def change_difficulty(self):
        """Change maze difficulty"""
        new_difficulty = self.difficulty_var.get()
        if new_difficulty != self.current_difficulty:
            self.current_difficulty = new_difficulty
            self.new_game()
    
    def change_algorithm(self, event=None):
        """Change pathfinding algorithm"""
        self.current_algorithm = self.algorithm_var.get()
        if self.show_solution:
            self.show_solution_path()
    
    def change_ai_speed(self, value):
        """Change AI movement speed"""
        self.ai_speed = int(float(value))
    
    def toggle_solution(self):
        """Toggle solution path display"""
        if self.show_solution:
            self.hide_solution_path()
        else:
            self.show_solution_path()
    
    def show_solution_path(self):
        """Show the solution path"""
        self.maze.clear_solution_path()
        path = self.solver.solve_maze(self.current_algorithm)
        
        if path:
            self.show_solution = True
            self.solve_button.config(text="Hide Solution")
            self.update_canvas()
        else:
            messagebox.showwarning("No Solution", "No solution found!")
    
    def hide_solution_path(self):
        """Hide the solution path"""
        self.maze.clear_solution_path()
        self.maze.reset_visited()
        self.show_solution = False
        self.solve_button.config(text="Show Solution")
        self.update_canvas()
    
    def toggle_ai_mode(self):
        """Toggle AI solving mode"""
        if self.ai_mode:
            self.stop_ai_solving()
        else:
            self.start_ai_solving()
    
    def start_ai_solving(self):
        """Start AI solving with animation"""
        # Get solution path
        self.maze.reset_visited()
        path = self.solver.solve_maze(self.current_algorithm)
        
        if not path:
            messagebox.showwarning("No Solution", "No solution found!")
            return
        
        self.ai_mode = True
        self.ai_player.set_path(path)
        self.ai_button.config(text="Stop AI")
        
        # Start AI animation
        self.animate_ai_solving()
    
    def stop_ai_solving(self):
        """Stop AI solving"""
        self.ai_mode = False
        self.ai_button.config(text="Start AI")
        self.ai_player.stop_solving()
    
    def animate_ai_solving(self):
        """Animate AI solving the maze"""
        if self.ai_mode and not self.ai_player.is_path_complete():
            if self.ai_player.next_step():
                self.update_canvas()
                self.update_stats_display()
                
                # Check if AI reached the goal
                if self.ai_player.is_at_goal():
                    self.handle_ai_victory()
                    return
                
                # Schedule next move
                self.root.after(self.ai_speed, self.animate_ai_solving)
            else:
                self.stop_ai_solving()
    
    def handle_victory(self):
        """Handle player victory"""
        moves = self.player.get_moves_count()
        self.stats.end_game(moves, True)
        
        message = f"Congratulations! You solved the maze!\n\n"
        message += f"Moves: {moves}\n"
        message += f"Algorithm used for solution: {self.current_algorithm}\n\n"
        message += "Would you like to play again?"
        
        if messagebox.askyesno("Victory!", message):
            self.new_game()
        
        self.update_stats_display()
    
    def handle_ai_victory(self):
        """Handle AI victory"""
        moves = self.ai_player.get_moves_count()
        message = f"AI solved the maze using {self.current_algorithm}!\n\n"
        message += f"Moves: {moves}\n"
        message += f"Speed: {self.ai_speed}ms per move"
        
        messagebox.showinfo("AI Victory!", message)
        self.stop_ai_solving()
    
    def update_stats_display(self):
        """Update the statistics display"""
        stats = self.stats.get_stats_dict()
        
        if self.multiplayer_mode:
            # Show multiplayer stats
            status = self.multiplayer.get_game_status()
            p1_pos = self.multiplayer.player1.get_position()
            p2_pos = self.multiplayer.player2.get_position()
            
            stats_text = f"""MULTIPLAYER MODE
Status: {status}

Player 1 (Red Circle):
Position: {p1_pos}
Moves: {self.multiplayer.player1.get_moves_count()}
Controls: W A S D

Player 2 (Teal Square):
Position: {p2_pos}
Moves: {self.multiplayer.player2.get_moves_count()}
Controls: Arrow Keys

{self.stats.get_multiplayer_stats()}

Current Settings:
Difficulty: {self.current_difficulty}"""
        else:
            # Show single player stats
            stats_text = f"""Current Game:
Moves: {self.player.get_moves_count()}
Position: {self.player.get_position()}

Overall Stats:
Games Played: {stats['games_played']}
Games Won: {stats['games_won']}
Win Rate: {stats['win_rate']:.1f}%
Best Score: {stats['best_score']}
Avg Moves: {stats['average_moves']}

{self.stats.get_multiplayer_stats()}

Current Settings:
Difficulty: {self.current_difficulty}
Algorithm: {self.current_algorithm}
AI Speed: {self.ai_speed}ms"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

# Bonus feature: Timer class for advanced statistics
class Timer:
    """Timer utility for tracking game duration"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False
    
    def start(self):
        """Start the timer"""
        self.start_time = time.time()
        self.is_running = True
    
    def stop(self):
        """Stop the timer"""
        if self.is_running:
            self.end_time = time.time()
            self.is_running = False
            return self.get_elapsed_time()
        return 0
    
    def get_elapsed_time(self):
        """Get elapsed time in seconds"""
        if self.start_time:
            end = self.end_time if self.end_time else time.time()
            return round(end - self.start_time, 2)
        return 0
    
    def reset(self):
        """Reset the timer"""
        self.start_time = None
        self.end_time = None
        self.is_running = False