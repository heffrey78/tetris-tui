# Tetris Terminal UI Game

A fully functional Tetris game implemented in Python using the curses library for terminal-based gameplay. Features robust game mechanics, clean code architecture, and comprehensive error handling.

## ✨ Features

- **🎮 Classic Tetris gameplay** with all 7 standard tetromino pieces (I, O, T, S, Z, J, L)
- **🎯 Precise controls** with smooth piece movement and rotation
- **🏆 Scoring system** with proper line clearing rewards (40/100/300/1200 points)
- **📈 Progressive difficulty** with 20 levels and increasing speed
- **📊 Information panel** displaying:
  - Current score and level
  - Lines cleared count
  - Next piece preview
  - Complete controls reference
  - Current theme indicator
- **🎨 Dual color themes**: Classic terminal green and retro amber
- **⏸️ Game controls**:
  - Arrow keys for movement and rotation
  - Space bar for hard drop
  - Pause/unpause, restart, and theme switching

## 🛠️ Technical Features

- **Type-safe Python** with comprehensive type hints
- **Robust error handling** with curses exception management
- **Clean architecture** with separated concerns
- **Comprehensive documentation** with detailed docstrings
- **Unit testing** suite for core game mechanics
- **Cross-platform compatibility** (Linux, macOS, Windows with proper terminal)

## 📋 Requirements

- **Python 3.6+** (recommended 3.8+)
- **Terminal with color support** (most modern terminals)
- **Curses library** (included with Python on Unix-like systems)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/heffrey78/tetris-tui.git
cd tetris-tui

# Run the game
python3 tetris.py

# Run tests (optional)
python3 test_tetris.py
```

## 🎮 Controls

| Key | Action | Description |
|-----|--------|-------------|
| ← / → | Move | Move piece horizontally |
| ↓ | Soft Drop | Move piece down faster (+1 point per cell) |
| ↑ | Rotate | Rotate piece 90° clockwise |
| Space | Hard Drop | Instantly drop piece (+2 points per cell) |
| P | Pause/Unpause | Toggle game pause state |
| R | Restart | Start a new game |
| T | Theme Toggle | Switch between green and amber themes |
| Q | Quit | Exit the game |

## 🏗️ Game Mechanics

### Scoring System
- **Line Clears**: 40/100/300/1200 points × (level + 1)
- **Soft Drop**: 1 point per cell moved down
- **Hard Drop**: 2 points per cell dropped

### Level Progression
- Level increases every 10 lines cleared
- Drop speed increases with each level (max level 20)
- More challenging gameplay at higher levels

### Standard Tetris Rules
- 10×20 playing field
- All 7 classic tetromino shapes with standard rotations
- Line clearing when rows are completely filled
- Game over when pieces reach the top

## 🧪 Testing

Comprehensive test suite covering:

```bash
python3 test_tetris.py
```

- ✅ Tetromino shapes and rotations
- ✅ Board collision detection  
- ✅ Line clearing mechanics
- ✅ Game state management
- ✅ Control functions

## 🏛️ Architecture

Clean, modular design with separated responsibilities:

```
├── Tetromino      # Individual pieces with rotation logic
├── Board          # Game field with collision detection
├── TetrisGame     # Core game logic and state management
└── TetrisUI       # Terminal interface with curses
```

### Key Design Principles
- **Single Responsibility**: Each class has a clear, focused purpose
- **Type Safety**: Comprehensive type hints and null checking
- **Error Resilience**: Graceful handling of terminal edge cases
- **Maintainability**: Well-documented code with clear interfaces

## 🎨 Themes

- **🟢 Classic Green**: Traditional terminal aesthetic
- **🟡 Retro Amber**: Vintage computer monitor style

Switch themes anytime during gameplay with the `T` key.

## 🤝 Contributing

This is a complete, standalone implementation. The code serves as an excellent example of:
- Clean Python architecture
- Curses library usage
- Game development patterns
- Terminal UI best practices

## 📄 License

Open source - feel free to learn from, modify, and share!

---

**Enjoy playing Tetris in your terminal! 🎮**