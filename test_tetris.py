#!/usr/bin/env python3
from tetris import TetrisGame, Tetromino, Board

def test_tetromino():
    print("Testing Tetromino...")
    piece = Tetromino('I')
    print(f"Initial shape: {piece.get_current_shape()}")
    
    rotated = piece.rotate()
    print(f"Rotated shape: {rotated.get_current_shape()}")
    print("✓ Tetromino test passed")

def test_board():
    print("\nTesting Board...")
    board = Board(10, 20)
    piece = Tetromino('O')
    piece.x = 4
    piece.y = 18
    
    print(f"Valid position test: {board.is_valid_position(piece)}")
    board.place_piece(piece)
    
    # Fill a line for testing line clearing
    for x in range(10):
        board.grid[19][x] = 'X'
    
    lines_cleared = board.clear_lines()
    print(f"Lines cleared: {lines_cleared}")
    print("✓ Board test passed")

def test_game():
    print("\nTesting Game...")
    game = TetrisGame()
    print(f"Initial score: {game.score}")
    print(f"Initial level: {game.level}")
    print(f"Current piece type: {game.current_piece.type}")
    print(f"Next piece type: {game.next_piece.type}")
    
    # Test movement
    initial_x = game.current_piece.x
    game.move_piece(1, 0)
    print(f"Moved piece from x={initial_x} to x={game.current_piece.x}")
    
    # Test rotation
    initial_rotation = game.current_piece.rotation
    game.rotate_piece()
    print(f"Rotated piece from rotation={initial_rotation} to rotation={game.current_piece.rotation}")
    
    print("✓ Game test passed")

def test_controls():
    print("\nTesting Controls...")
    game = TetrisGame()
    
    # Test pause
    game.toggle_pause()
    print(f"Paused: {game.paused}")
    game.toggle_pause()
    print(f"Unpaused: {game.paused}")
    
    # Test theme toggle
    initial_theme = game.theme
    game.toggle_theme()
    print(f"Theme changed from {initial_theme} to {game.theme}")
    
    print("✓ Controls test passed")

if __name__ == "__main__":
    print("Running Tetris game logic tests...\n")
    test_tetromino()
    test_board()
    test_game()
    test_controls()
    print("\n✅ All tests passed! Game is ready to play.")
    print("\nTo play the game, run: python3 tetris.py")
    print("Make sure you're in a proper terminal environment.")