"""
Chess Engine Implementation
--------------------------
A chess engine that uses alpha-beta pruning with various enhancements:
- Iterative deepening
- Quiescence search
- Move ordering
- Transposition tables
- Null move pruning
- Late move reduction
- Killer moves heuristic

The engine evaluates positions using both material and positional factors,
and includes opening book support for the early game.
"""

import chess
import time
from typing import Optional, Tuple, List
from evaluation import ChessEvaluator
from opening_book import OpeningBook

class ChessEngine:
    """
    Main chess engine class implementing search and move generation.
    
    Attributes:
        depth (int): Maximum search depth
        time_limit (float): Maximum time allowed for a move in seconds
        quiescence_depth (int): Maximum depth for quiescence search
        aspiration_window (int): Window size for aspiration search
        null_move_R (int): Reduction factor for null move pruning
        futility_margin (int): Margin for futility pruning
        late_move_reduction (int): Depth reduction for late moves
    """
    
    def __init__(self, depth: int = 8, time_limit: float = 6.0):
        """
        Initialize the chess engine with search parameters.
        
        Args:
            depth: Maximum search depth
            time_limit: Time limit per move in seconds
        """
        self.depth = depth
        self.time_limit = time_limit  # Time limit in seconds
        self.evaluator = ChessEvaluator()
        self.start_time = 0
        self.position_history = {}  # Track position repetitions
        self.opening_book = OpeningBook()
        self.initial_material = None  # Add this line
        self.quiescence_depth = 16  # Increased for better tactical awareness
        self.hash_table = {}       # Simple transposition table
        self.killer_moves = [[None] * 2 for _ in range(64)]  # Store killer moves per ply
        self.aspiration_window = 25  # Reduced for more accurate searching
        self.null_move_R = 2        # Null move reduction
        self.futility_margin = 200  # Increased for aggressive pruning
        self.late_move_reduction = 2 # LMR reduction

    def is_time_up(self) -> bool:
        """Checks if we've exceeded our time limit."""
        current_time = time.time()
        return current_time - self.start_time > self.time_limit
        
    def order_moves(self, board: chess.Board, moves: List[chess.Move], ply: int = 0) -> List[chess.Move]:
        """
        Orders moves to improve alpha-beta pruning efficiency.
        
        Priorities:
        1. Hash table moves
        2. Captures (MVV-LVA ordering)
        3. Killer moves
        4. History moves
        
        Args:
            board: Current board position
            moves: List of legal moves
            ply: Current ply from root
            
        Returns:
            Sorted list of moves
        """
        move_scores = []
        
        # Get hash move if available
        hash_move = self.hash_table.get(board.fen().split(' ')[0], None)
        
        for move in moves:
            score = 0
            
            # Hash move gets highest priority
            if hash_move and move == hash_move:
                score = 30000
                
            # Killer moves get high priority
            elif move in self.killer_moves[ply]:
                score = 20000
                
            else:
                moving_piece = board.piece_at(move.from_square)
                captured_piece = board.piece_at(move.to_square)
                
                # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                if captured_piece:
                    score = 10000 + (captured_piece.piece_type * 100 - moving_piece.piece_type)
                    
                # Promotion scoring
                if move.promotion:
                    score += 15000 + move.promotion
                    
                # Check threat bonus
                board.push(move)
                if board.is_check():
                    score += 9000
                board.pop()
                
             
            move_scores.append((move, score))
            
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]

    def quiescence_search(self, board: chess.Board, alpha: float, beta: float, depth: int) -> float:
        """
        Quiescence search to evaluate tactical positions.
        Only considers captures and checks to reach a quiet position.
        
        Args:
            board: Current board position
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            depth: Maximum quiescence depth
            
        Returns:
            Evaluation score of the position
        """
        # Early exit for checkmate/stalemate
        if board.is_checkmate():
            return -20000 if board.turn else 20000
        if board.is_stalemate():
            return 0
            
        # Stand-pat evaluation
        stand_pat = self.evaluator.evaluate(board)
        
        if depth == 0:
            return stand_pat
            
        if stand_pat >= beta:
            return beta
            
        alpha = max(alpha, stand_pat)
        
        # Consider checks in quiescence search
        if depth >= 4:
            moves = list(board.legal_moves)
        else:
            moves = list(board.generate_legal_captures())
            
        # Use move ordering even in quiescence
        for move in self.order_moves(board, moves):
            if not board.is_capture(move) and not board.gives_check(move):
                continue
                
            board.push(move)
            score = -self.quiescence_search(board, -beta, -alpha, depth - 1)
            board.pop()
            
            if score >= beta:
                return beta
            alpha = max(alpha, score)
            
        return alpha

    def alpha_beta(self, board: chess.Board, depth: int, alpha: float, beta: float, 
                  maximizing_player: bool, ply: int = 0, can_null: bool = True) -> Tuple[float, Optional[chess.Move]]:
        """
        Enhanced alpha-beta search with pruning techniques.
        
        Args:
            board: Current board position
            depth: Remaining depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: True if maximizing, False if minimizing
            ply: Current ply (half-move) from root
            can_null: Whether null move is allowed
            
        Returns:
            Tuple of (evaluation score, best move)
        """
        # Early exit conditions
        if self.is_time_up():
            raise TimeoutError

        # alpha_orig = alpha

        # Transposition table lookup for previously searched positions
        board_hash = board.fen().split(' ')[0]
        if board_hash in self.hash_table and depth > 0:
            return self.hash_table[board_hash], None

        # At leaf nodes, perform quiescence search
        if depth <= 0:
            return self.quiescence_search(board, alpha, beta, self.quiescence_depth), None

        # Null move pruning to skip obviously bad positions
        if can_null and depth >= 3 and not board.is_check():
            board.push(chess.Move.null())
            null_value = -self.alpha_beta(board, depth - 1 - self.null_move_R, 
                                        -beta, -beta + 1, not maximizing_player, 
                                        ply + 1, False)[0]
            board.pop()
            if null_value >= beta:
                return beta, None

        # Get and sort legal moves
        moves = list(board.legal_moves)
        if not moves:
            if board.is_check():
                return 20000 + ply, None  # Prefer shorter mate
            return 0, None  # Stalemate

        # Internal iterative deepening
        if depth >= 4 and board_hash not in self.hash_table:
            _, move = self.alpha_beta(board, depth - 2, alpha, beta, 
                                    maximizing_player, ply, False)
            if move:
                moves.insert(0, moves.pop(moves.index(move)))

        # Main move search loop
        best_move = None
        best_value = float('-inf') if maximizing_player else float('inf')
        moves_searched = 0

        for move in self.order_moves(board, moves, ply):
            moves_searched += 1
            is_capture = board.is_capture(move)
            gives_check = board.gives_check(move)
            
            # Futility pruning
            if depth <= 2 and not (is_capture or gives_check or board.is_check()):
                if maximizing_player and best_value > -float('inf'):
                    if best_value + self.futility_margin <= alpha:
                        continue
                elif not maximizing_player and best_value < float('inf'):
                    if best_value - self.futility_margin >= beta:
                        continue

            # Late move reduction
            new_depth = depth - 1
            if (depth >= 3 and 
                moves_searched >= 3 and 
                not is_capture and 
                not gives_check and 
                not board.is_check()):
                new_depth -= self.late_move_reduction

            board.push(move)
            value, _ = self.alpha_beta(board, new_depth, -beta, -alpha, 
                                     not maximizing_player, ply + 1)
            value = -value
            board.pop()

            if maximizing_player:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)

            if beta <= alpha:
                if not board.is_capture(move):
                    self.killer_moves[ply][1] = self.killer_moves[ply][0]
                    self.killer_moves[ply][0] = move
                break

        # Store result in transposition table
        self.hash_table[board_hash] = best_value

        return best_value, best_move

    def iterative_deepening(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Iterative deepening search framework.
        Progressively increases search depth until time runs out.
        
        Args:
            board: Current board position
            
        Returns:
            Best move found within time limit
        """
        best_move = None
        best_value = 0
        current_depth = 1
        
        try:
            while current_depth <= self.depth and not self.is_time_up():
                alpha = -float('inf')
                beta = float('inf')
                
                if current_depth >= 4:
                    alpha = best_value - self.aspiration_window
                    beta = best_value + self.aspiration_window
                
                try:
                    value, move = self.alpha_beta(board, current_depth, alpha, beta, True)
                    if move:
                        best_move = move
                        best_value = value
                    #print(f"Depth {current_depth}: {value}")
                except ValueError:
                    # Aspiration window failed, retry with full window
                    value, move = self.alpha_beta(board, current_depth, 
                                                -float('inf'), float('inf'), True)
                    if move:
                        best_move = move
                        best_value = value
                
                current_depth += 1
                
        except TimeoutError:
            pass
            
        return best_move

    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Enhanced get_best_move with clearing of search structures.
        
        Args:
            board: Current board position
            
        Returns:
            Best move found
        """
        # Clear search structures
        self.hash_table.clear()
        self.killer_moves = [[None] * 2 for _ in range(64)]
        
        # Try opening book first
        if book_move := self.opening_book.get_book_move(board):
            print("Book move played")
            return book_move

        # Reset initial material before new search
        self.initial_material = None
        self.start_time = time.time()
        self.position_history = {}
        best_move = self.iterative_deepening(board)
        end_time = time.time()
        print(f"Search move found in {end_time - self.start_time:.2f}s")
        return best_move

    def _count_material(self, board: chess.Board) -> int:
        """
        Counts total material value for the side to move.
        
        Args:
            board: Current board position
            
        Returns:
            Total material value
        """
        material = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            material += len(board.pieces(piece_type, board.turn)) * self.evaluator.PIECE_VALUES[piece_type]
        return material
