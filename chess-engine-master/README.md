# Chess Engine

A Python-based chess engine with GUI implementation featuring AI gameplay and opening book support.

## Features

- Graphical user interface using Pygame
- AI opponent with configurable difficulty
- Opening book support
- Sound effects for moves and game events
- Two-player mode
- Visual move highlighting
- Game state detection (checkmate, stalemate, etc.)
- Move validation and legal move highlighting
- Pawn promotion interface

## Requirements

- Python 3.7+
- pygame
- python-chess

## Project Structure

```
chess-engine/
├── assets/
│   ├── chess_pieces/     # PNG images for chess pieces
│   ├── sounds/           # Sound effect files
│   └── books/           # Opening book files
├── chess_engine.py      # AI and move calculation
├── chess_gui.py        # Graphical interface
├── constants.py        # Game constants and settings
├── evaluation.py       # Position evaluation logic
├── main.py            # Entry point
├── menu.py            # Game mode selection menu
├── opening_book.py    # Opening book handling
├── popup_manager.py   # In-game popup messages
└── sound_manager.py   # Sound effect handling
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chess-engine.git
```

2. Install dependencies:
```bash
pip install pygame python-chess
```

3. Ensure all required assets are present:
- Place chess piece images in `assets/chess_pieces/`
- Place sound files in `assets/sounds/`
- Place opening book file in `assets/books/`

## Usage

Run the game:
```bash
python main.py
```

Select game mode:
- Play against AI
- Play against friend

## Controls

- Left click to select pieces and make moves
- For pawn promotion, click desired promotion piece
- Close window to exit game

## AI Features

- Iterative deepening search
- Alpha-beta pruning
- Move ordering optimization
- Opening book integration
- Position evaluation considering:
  - Material balance
  - Piece positions
  - King safety
  - Pawn structure
  - Mobility
  - Center control

## Sound Effects

The game includes sound effects for:
- Regular moves
- Captures
- Castle moves
- Checkmate
- Draw

## Credits

- Chess piece images: Standard chess piece set
- Opening book: Performance.bin (optional)
- Sound effects: [Source credits]

## License

[Your chosen license]