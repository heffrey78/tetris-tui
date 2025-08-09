#!/usr/bin/env python3
"""
Tetris Terminal UI Game

A fully functional Tetris game implemented in Python using the curses library.
Features classic Tetris gameplay with all 7 tetromino pieces, line clearing,
level progression, and color themes.

Controls:
    Arrow keys: Move and rotate pieces
    Space: Hard drop
    P: Pause/unpause
    R: Restart
    T: Toggle color theme
    Q: Quit

Author: Claude (Anthropic)
"""

import curses
import random
import time
from enum import Enum
from typing import List, Optional

class ColorTheme(Enum):
    GREEN = "green"
    AMBER = "amber"

class Tetromino:
    """Represents a single tetromino piece with rotation capabilities.
    
    Each tetromino has a type (I, O, T, S, Z, J, L), position (x, y),
    and rotation state. Handles shape definitions and rotation logic.
    """
    SHAPES = {
        'I': [
            ['....', 'IIII', '....', '....'],
            ['..I.', '..I.', '..I.', '..I.'],
            ['....', '....', 'IIII', '....'],
            ['.I..', '.I..', '.I..', '.I..']
        ],
        'O': [
            ['OO', 'OO']
        ],
        'T': [
            ['.T.', 'TTT', '...'],
            ['.T.', '.TT', '.T.'],
            ['...', 'TTT', '.T.'],
            ['.T.', 'TT.', '.T.']
        ],
        'S': [
            ['.SS', 'SS.', '...'],
            ['.S.', '.SS', '..S']
        ],
        'Z': [
            ['ZZ.', '.ZZ', '...'],
            ['..Z', '.ZZ', '.Z.']
        ],
        'J': [
            ['J..', 'JJJ', '...'],
            ['.JJ', '.J.', '.J.'],
            ['...', 'JJJ', '..J'],
            ['.J.', '.J.', 'JJ.']
        ],
        'L': [
            ['..L', 'LLL', '...'],
            ['.L.', '.L.', '.LL'],
            ['...', 'LLL', 'L..'],
            ['LL.', '.L.', '.L.']
        ]
    }
    
    def __init__(self, shape_type: str):
        """Initialize a new tetromino piece.
        
        Args:
            shape_type: One of 'I', 'O', 'T', 'S', 'Z', 'J', 'L'
        """
        self.type = shape_type
        self.rotation = 0
        self.x = 4
        self.y = 0
        self.shape = self.SHAPES[shape_type]
    
    def get_current_shape(self) -> List[str]:
        """Get the current shape based on rotation state.
        
        Returns:
            List of strings representing the current rotated shape
        """
        return self.shape[self.rotation % len(self.shape)]
    
    def rotate(self) -> 'Tetromino':
        """Create a new tetromino rotated 90 degrees clockwise.
        
        Returns:
            New Tetromino instance with incremented rotation
        """
        new_piece = Tetromino(self.type)
        new_piece.rotation = (self.rotation + 1) % len(self.shape)
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece

class Board:
    """Game board that handles piece placement, collision detection, and line clearing.
    
    The board is a 2D grid where '.' represents empty space and any other
    character represents a placed piece.
    """
    def __init__(self, width: int = 10, height: int = 20):
        """Initialize a new game board.
        
        Args:
            width: Board width in blocks (default 10)
            height: Board height in blocks (default 20)
        """
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, piece: Tetromino, dx: int = 0, dy: int = 0) -> bool:
        """Check if a piece can be placed at the given offset.
        
        Args:
            piece: The tetromino to check
            dx: X offset from piece's current position
            dy: Y offset from piece's current position
            
        Returns:
            True if position is valid, False otherwise
        """
        shape = piece.get_current_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    new_x = piece.x + col_idx + dx
                    new_y = piece.y + row_idx + dy
                    
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height or 
                        (new_y >= 0 and self.grid[new_y][new_x] != '.')):
                        return False
        return True
    
    def place_piece(self, piece: Tetromino):
        """Place a piece permanently on the board.
        
        Args:
            piece: The tetromino to place
        """
        shape = piece.get_current_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    x = piece.x + col_idx
                    y = piece.y + row_idx
                    if y >= 0:
                        self.grid[y][x] = cell
    
    def clear_lines(self) -> int:
        """Remove completed lines and return count.
        
        Returns:
            Number of lines cleared
        """
        lines_cleared = 0
        new_grid = []
        
        for row in self.grid:
            if '.' in row:
                new_grid.append(row)
            else:
                lines_cleared += 1
        
        while len(new_grid) < self.height:
            new_grid.insert(0, ['.' for _ in range(self.width)])
        
        self.grid = new_grid
        return lines_cleared
    
    def is_game_over(self) -> bool:
        return any(cell != '.' for cell in self.grid[0])

class TetrisGame:
    """Main game logic controller for Tetris.
    
    Manages game state, piece spawning, movement, scoring, and level progression.
    Handles all game mechanics including line clearing and collision detection.
    """
    # Scoring constants for line clears
    LINE_CLEAR_SCORES = [0, 40, 100, 300, 1200]  # 0, single, double, triple, tetris
    HARD_DROP_POINTS = 2
    SOFT_DROP_POINTS = 1
    
    def __init__(self):
        self.board = Board()
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.paused = False
        self.game_over = False
        self.theme = ColorTheme.GREEN
        self.last_drop_time = time.time()
        self.drop_interval = 1.0
        
        self.spawn_new_piece()
        self.spawn_new_piece()
    
    def _calculate_score(self, lines_cleared: int) -> int:
        """Calculate score for line clears with bounds checking"""
        if lines_cleared < 0 or lines_cleared >= len(self.LINE_CLEAR_SCORES):
            return 0
        return self.LINE_CLEAR_SCORES[lines_cleared] * (self.level + 1)
    
    def spawn_new_piece(self):
        """Spawn a new tetromino piece and generate the next piece.
        
        Sets current_piece to next_piece and generates a new next_piece.
        If the new piece can't be placed, triggers game over.
        """
        if self.next_piece is None:
            shape_type = random.choice(list(Tetromino.SHAPES.keys()))
            self.next_piece = Tetromino(shape_type)
        
        self.current_piece = self.next_piece
        self.current_piece.x = 4
        self.current_piece.y = 0
        
        shape_type = random.choice(list(Tetromino.SHAPES.keys()))
        self.next_piece = Tetromino(shape_type)
        
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """Move the current piece by dx, dy if the move is valid"""
        if self.current_piece is None:
            return False
        if self.board.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self) -> bool:
        """Rotate the current piece if the rotation is valid"""
        if self.current_piece is None:
            return False
        rotated = self.current_piece.rotate()
        if self.board.is_valid_position(rotated):
            self.current_piece = rotated
            return True
        return False
    
    def hard_drop(self):
        """Drop the current piece to the bottom instantly"""
        if self.current_piece is None:
            return
        while self.move_piece(0, 1):
            self.score += self.HARD_DROP_POINTS
        self.lock_piece()
    
    def lock_piece(self):
        """Lock the current piece in place and handle line clearing"""
        if self.current_piece is None:
            return
        self.board.place_piece(self.current_piece)
        lines = self.board.clear_lines()
        
        if lines > 0:
            self.lines_cleared += lines
            self.score += self._calculate_score(lines)
            self.level = min(20, self.lines_cleared // 10 + 1)
            self.drop_interval = max(0.05, 1.0 - (self.level - 1) * 0.05)
        
        self.spawn_new_piece()
    
    def update(self):
        """Update game state - handle automatic piece dropping.
        
        Called every game loop iteration to handle time-based piece movement.
        """
        if self.paused or self.game_over:
            return
        
        current_time = time.time()
        if current_time - self.last_drop_time >= self.drop_interval:
            if not self.move_piece(0, 1):
                self.lock_piece()
            self.last_drop_time = current_time
    
    def toggle_pause(self):
        """Toggle the game pause state."""
        self.paused = not self.paused
    
    def restart(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.paused = False
        self.game_over = False
        self.last_drop_time = time.time()
        self.drop_interval = 1.0
        
        self.spawn_new_piece()
        self.spawn_new_piece()
    
    def toggle_theme(self):
        """Switch between green and amber color themes."""
        self.theme = ColorTheme.AMBER if self.theme == ColorTheme.GREEN else ColorTheme.GREEN

class TetrisUI:
    """Terminal user interface for the Tetris game using curses.
    
    Handles all display rendering, color management, and user input processing.
    Manages the game board display and information panel.
    """
    def __init__(self, stdscr):
        """Initialize the terminal UI.
        
        Args:
            stdscr: The curses standard screen object
        """
        self.stdscr = stdscr
        self.game = TetrisGame()
        self.setup_colors()
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(50)
    
    def setup_colors(self):
        """Initialize color pairs for both green and amber themes."""
        curses.start_color()
        curses.use_default_colors()
        
        # Green theme
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # Main text
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)  # Filled blocks
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Border
        
        # Amber theme
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Main text
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)  # Filled blocks
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # Border
    
    def get_color_pair(self, is_filled: bool = False, is_border: bool = False) -> int:
        """Get the appropriate color pair for the current theme.
        
        Args:
            is_filled: True for filled blocks, False for text
            is_border: True for border elements
            
        Returns:
            Color pair number for curses
        """
        if self.game.theme == ColorTheme.GREEN:
            if is_border:
                return 5
            return 2 if is_filled else 1
        else:
            if is_border:
                return 6
            return 4 if is_filled else 3
    
    def draw_board(self):
        """Draw the game board, border, and current piece."""
        start_y, start_x = 2, 2
        
        # Draw border
        border_color = self.get_color_pair(is_border=True)
        for y in range(self.game.board.height + 2):
            for x in range(self.game.board.width + 2):
                if y == 0 or y == self.game.board.height + 1 or x == 0 or x == self.game.board.width + 1:
                    try:
                        self.stdscr.addstr(start_y + y, start_x + x * 2, '[]', curses.color_pair(border_color))
                    except curses.error:
                        pass
        
        # Draw board content
        for y in range(self.game.board.height):
            for x in range(self.game.board.width):
                cell = self.game.board.grid[y][x]
                screen_y = start_y + y + 1
                screen_x = start_x + (x + 1) * 2
                
                try:
                    if cell != '.':
                        color = self.get_color_pair(True)
                        self.stdscr.addstr(screen_y, screen_x, '[]', curses.color_pair(color))
                    else:
                        color = self.get_color_pair()
                        self.stdscr.addstr(screen_y, screen_x, '  ', curses.color_pair(color))
                except curses.error:
                    pass
        
        # Draw current piece
        if self.game.current_piece:
            shape = self.game.current_piece.get_current_shape()
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    if cell != '.':
                        screen_y = start_y + self.game.current_piece.y + row_idx + 1
                        screen_x = start_x + (self.game.current_piece.x + col_idx + 1) * 2
                        if (0 <= screen_y < curses.LINES and 0 <= screen_x < curses.COLS - 1):
                            try:
                                color = self.get_color_pair(True)
                                self.stdscr.addstr(screen_y, screen_x, '[]', curses.color_pair(color))
                            except curses.error:
                                pass
    
    def draw_info_panel(self):
        """Draw the information panel with score, level, next piece, and controls."""
        panel_x = 28
        color = self.get_color_pair()
        
        # Title
        self.stdscr.addstr(2, panel_x, "TETRIS", curses.color_pair(color) | curses.A_BOLD)
        
        # Score, Level, Lines
        self.stdscr.addstr(4, panel_x, f"Score: {self.game.score}", curses.color_pair(color))
        self.stdscr.addstr(5, panel_x, f"Level: {self.game.level}", curses.color_pair(color))
        self.stdscr.addstr(6, panel_x, f"Lines: {self.game.lines_cleared}", curses.color_pair(color))
        
        # Next piece
        self.stdscr.addstr(8, panel_x, "Next:", curses.color_pair(color))
        if self.game.next_piece:
            shape = self.game.next_piece.get_current_shape()
            for row_idx, row in enumerate(shape):
                for col_idx, cell in enumerate(row):
                    screen_y = 10 + row_idx
                    screen_x = panel_x + col_idx * 2
                    if cell != '.':
                        if screen_y < curses.LINES and screen_x < curses.COLS - 1:
                            try:
                                color_filled = self.get_color_pair(True)
                                self.stdscr.addstr(screen_y, screen_x, '[]', curses.color_pair(color_filled))
                            except curses.error:
                                pass
        
        # Controls
        controls_y = 15
        self.stdscr.addstr(controls_y, panel_x, "Controls:", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 1, panel_x, "Arrow keys: Move", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 2, panel_x, "Up: Rotate", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 3, panel_x, "Space: Hard drop", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 4, panel_x, "P: Pause", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 5, panel_x, "R: Restart", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 6, panel_x, "T: Toggle theme", curses.color_pair(color))
        self.stdscr.addstr(controls_y + 7, panel_x, "Q: Quit", curses.color_pair(color))
        
        # Theme
        theme_name = "Green" if self.game.theme == ColorTheme.GREEN else "Amber"
        self.stdscr.addstr(controls_y + 9, panel_x, f"Theme: {theme_name}", curses.color_pair(color))
        
        # Status
        if self.game.game_over:
            self.stdscr.addstr(1, panel_x, "GAME OVER", curses.color_pair(color) | curses.A_BOLD)
        elif self.game.paused:
            self.stdscr.addstr(1, panel_x, "PAUSED", curses.color_pair(color) | curses.A_BOLD)
    
    def handle_input(self):
        """Process keyboard input and update game state.
        
        Returns:
            False if user wants to quit, True otherwise
        """
        try:
            key = self.stdscr.getch()
        except:
            return True
        
        if key == ord('q') or key == ord('Q'):
            return False
        elif key == ord('p') or key == ord('P'):
            self.game.toggle_pause()
        elif key == ord('r') or key == ord('R'):
            self.game.restart()
        elif key == ord('t') or key == ord('T'):
            self.game.toggle_theme()
        elif not self.game.paused and not self.game.game_over:
            if key == curses.KEY_LEFT:
                self.game.move_piece(-1, 0)
            elif key == curses.KEY_RIGHT:
                self.game.move_piece(1, 0)
            elif key == curses.KEY_DOWN:
                if self.game.move_piece(0, 1):
                    self.game.score += 1
            elif key == curses.KEY_UP:
                self.game.rotate_piece()
            elif key == ord(' '):
                self.game.hard_drop()
        
        return True
    
    def run(self):
        """Main game loop - handles display updates and input processing."""
        while True:
            self.stdscr.clear()
            
            self.game.update()
            self.draw_board()
            self.draw_info_panel()
            
            if not self.handle_input():
                break
            
            self.stdscr.refresh()

def main(stdscr):
    """Entry point for curses wrapper.
    
    Args:
        stdscr: The curses standard screen object
    """
    ui = TetrisUI(stdscr)
    ui.run()

if __name__ == "__main__":
    curses.wrapper(main)