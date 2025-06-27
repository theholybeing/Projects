import chess
import chess.polyglot
import random
from typing import Optional, List, Tuple
from constants import OPENING_BOOK_PATH

class OpeningBook:
    def __init__(self):
        self.book_path = OPENING_BOOK_PATH
        self.enabled = True
        try:
            with chess.polyglot.open_reader(self.book_path) as reader:
                pass
        except Exception as e:
            print(f"Warning: Opening book not found or invalid at {self.book_path}")
            print(f"Error: {e}")
            self.enabled = False

    def get_book_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Gets a move from the opening book."""
        if not self.enabled:
            return None

        try:
            moves = self._get_weighted_moves(board)
            if not moves:
                return None

            # Select move based on weights
            total_weight = sum(weight for _, weight in moves)
            choice = random.uniform(0, total_weight)
            current_sum = 0

            for move, weight in moves:
                current_sum += weight
                if current_sum > choice:
                    return move

            return moves[0][0]  # Fallback to first move
        except Exception as e:
            print(f"Opening book error: {e}")
            return None

    def _get_weighted_moves(self, board: chess.Board) -> List[Tuple[chess.Move, int]]:
        """Gets all possible book moves with their weights."""
        moves = []
        try:
            with chess.polyglot.open_reader(self.book_path) as reader:
                for entry in reader.find_all(board):
                    moves.append((entry.move, entry.weight))
        except Exception:
            return []
        return moves

    def get_opening_name(self, board: chess.Board) -> Optional[str]:
        """Gets the name of the current opening if available."""
        if not self.enabled:
            return None

        try:
            with chess.polyglot.open_reader(self.book_path) as reader:
                entry = reader.find(board)
                return entry.learn if entry else None
        except Exception:
            return None
