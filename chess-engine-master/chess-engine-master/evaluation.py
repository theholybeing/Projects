import chess
from typing import Dict, List

class ChessEvaluator:
    def __init__(self):
        # Reset material values to standard centipawn values
        self.PIECE_VALUES = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 310,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # Adjusted positional tables with only positive values
        self.PAWN_TABLE = [
            100, 100, 100, 100, 100, 100, 100, 100,
            150, 150, 150, 150, 150, 150, 150, 150,
            110, 110, 120, 130, 130, 120, 110, 110,
            105, 105, 110, 125, 125, 110, 105, 105,
            100, 100, 100, 120, 120, 100, 100, 100,
            105,  95,  90, 100, 100,  90,  95, 105,
            105, 110, 110,  80,  80, 110, 110, 105,
            100, 100, 100, 100, 100, 100, 100, 100
        ]
        
        self.KNIGHT_TABLE = [
            50,  60,  70,  70,  70,  70,  60,  50,
            60,  80, 100, 100, 100, 100,  80,  60,
            70, 100, 110, 115, 115, 110, 100,  70,
            70, 105, 115, 120, 120, 115, 105,  70,
            70, 100, 115, 120, 120, 115, 100,  70,
            70, 105, 110, 115, 115, 110, 105,  70,
            60,  80, 100, 105, 105, 100,  80,  60,
            50,  60,  70,  70,  70,  70,  60,  50
        ]
        
        self.BISHOP_TABLE = [
            80,  90,  90,  90,  90,  90,  90,  80,
            90, 100, 100, 100, 100, 100, 100,  90,
            90, 100, 105, 110, 110, 105, 100,  90,
            90, 105, 105, 110, 110, 105, 105,  90,
            90, 100, 110, 110, 110, 110, 100,  90,
            90, 110, 110, 110, 110, 110, 110,  90,
            90, 105, 100, 100, 100, 100, 105,  90,
            80,  90,  90,  90,  90,  90,  90,  80
        ]
        
        self.ROOK_TABLE = [
            100, 100, 100, 105, 105, 100, 100, 100,
             95, 100, 100, 100, 100, 100, 100,  95,
             95, 100, 100, 100, 100, 100, 100,  95,
             95, 100, 100, 100, 100, 100, 100,  95,
             95, 100, 100, 100, 100, 100, 100,  95,
             95, 100, 100, 100, 100, 100, 100,  95,
            105, 110, 110, 110, 110, 110, 110, 105,
            100, 100, 100, 100, 100, 100, 100, 100
        ]
        
        self.QUEEN_TABLE = [
            80,  90,  90,  95,  95,  90,  90,  80,
            90, 100, 100, 100, 100, 100, 100,  90,
            90, 100, 105, 105, 105, 105, 100,  90,
            95, 100, 105, 105, 105, 105, 100,  95,
            100, 100, 105, 105, 105, 105, 100,  95,
            90, 105, 105, 105, 105, 105, 100,  90,
            90, 100, 105, 100, 100, 100, 100,  90,
            80,  90,  90,  95,  95,  90,  90,  80
        ]
        
        self.KING_MIDDLEGAME_TABLE = [
            70,  60,  60,  50,  50,  60,  60,  70,
            70,  60,  60,  50,  50,  60,  60,  70,
            70,  60,  60,  50,  50,  60,  60,  70,
            70,  60,  60,  50,  50,  60,  60,  70,
            80,  70,  70,  60,  60,  70,  70,  80,
            90,  80,  80,  80,  80,  80,  80,  90,
            120, 120, 100, 100, 100, 100, 120, 120,
            120, 130, 110, 100, 100, 110, 130, 120
        ]
        
        self.KING_ENDGAME_TABLE = [
            50,  60,  70,  80,  80,  70,  60,  50,
            70,  80,  90, 100, 100,  90,  80,  70,
            70,  90, 120, 130, 130, 120,  90,  70,
            70,  90, 130, 140, 140, 130,  90,  70,
            70,  90, 130, 140, 140, 130,  90,  70,
            70,  90, 120, 130, 130, 120,  90,  70,
            70,  70, 100, 100, 100, 100,  70,  70,
            50,  70,  70,  70,  70,  70,  70,  50
        ]

        self.PIECE_POSITION_SCORES = {
            chess.PAWN: self.PAWN_TABLE,
            chess.KNIGHT: self.KNIGHT_TABLE,
            chess.BISHOP: self.BISHOP_TABLE,
            chess.ROOK: self.ROOK_TABLE,
            chess.QUEEN: self.QUEEN_TABLE,
            chess.KING: self.KING_MIDDLEGAME_TABLE
        }

        # Normalize weights to prevent score explosion
        self.KING_SAFETY_WEIGHT = 0.5
        self.MOBILITY_WEIGHT = 0.1
        self.PAWN_STRUCTURE_WEIGHT = 0.3
        self.CENTER_CONTROL_WEIGHT = 0.4
        self.PIECE_ACTIVITY_WEIGHT = 0.2
        self.KING_ATTACK_WEIGHT = 0.3
        self.PIECE_COORDINATION_WEIGHT = 0.2
        
        # Center squares for quick reference
        self.CENTER_SQUARES = {chess.E4, chess.E5, chess.D4, chess.D5}
        self.EXTENDED_CENTER = {chess.C3, chess.D3, chess.E3, chess.F3,
                              chess.C4, chess.D4, chess.E4, chess.F4,
                              chess.C5, chess.D5, chess.E5, chess.F5,
                              chess.C6, chess.D6, chess.E6, chess.F6}

        # Add opening-specific penalties
        self.EARLY_KING_MOVE_PENALTY = 300  # Penalty for moving king early
        self.EARLY_QUEEN_MOVE_PENALTY = 50   # Small penalty for early queen moves

        # Add mobility bonuses
        self.MOBILITY_BONUS = {
            chess.KNIGHT: 4,
            chess.BISHOP: 5,
            chess.ROOK: 2,
            chess.QUEEN: 1
        }
        
        # Add piece-square tables for endgame
        self.PAWN_ENDGAME_TABLE = [
            # More aggressive pawn advancement in endgame
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            40, 40, 40, 40, 40, 40, 40, 40,
            30, 30, 30, 30, 30, 30, 30, 30,
            20, 20, 20, 20, 20, 20, 20, 20,
            10, 10, 10, 10, 10, 10, 10, 10,
            5,  5,  5,  5,  5,  5,  5,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

    def evaluate(self, board: chess.Board) -> float:
        """Evaluation function with score reset."""
        # Early exit conditions
        if board.is_checkmate():
            return -20000 if board.turn else 20000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        # Start with fresh score
        score = 0.0
        
        # Calculate material score (base evaluation)
        score = self._evaluate_material_and_position(board)
        
        # Get game phase once
        is_endgame = self._is_endgame(board)
        
        # Add weighted positional factors
        if not is_endgame:
            # Middlegame evaluation
            position_score = (
                self._evaluate_king_safety(board) * self.KING_SAFETY_WEIGHT +
                self._evaluate_piece_activity(board) * self.PIECE_ACTIVITY_WEIGHT +
                self._evaluate_center_control(board) * self.CENTER_CONTROL_WEIGHT +
                self._evaluate_piece_coordination(board) * self.PIECE_COORDINATION_WEIGHT
            )
            score += position_score * 0.01  # Scale down positional contribution
        else:
            # Endgame evaluation
            endgame_score = (
                self._evaluate_king_centralization(board) * 0.3 +
                self._evaluate_passed_pawns(board) * 0.4
            )
            score += endgame_score * 0.01  # Scale down endgame contribution

        # Always evaluate mobility and pawn structure
        score += (
            self._evaluate_mobility_new(board) * self.MOBILITY_WEIGHT +
            self._evaluate_pawn_structure(board) * self.PAWN_STRUCTURE_WEIGHT
        ) * 0.01  # Scale down these contributions

        # Clamp final score
        score = max(min(score, 15000), -15000)
        
        return score if board.turn else -score

    def _is_endgame(self, board: chess.Board) -> bool:
        """More accurate endgame detection"""
        # Count material for both sides
        white_material = sum(len(board.pieces(piece_type, chess.WHITE)) * self.PIECE_VALUES[piece_type] 
                           for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT])
        black_material = sum(len(board.pieces(piece_type, chess.BLACK)) * self.PIECE_VALUES[piece_type] 
                           for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT])
        
        # Consider it endgame if:
        # 1. Both sides have no queens, or
        # 2. The side with a queen has less than a rook in other pieces
        queens = len(list(board.pieces(chess.QUEEN, chess.WHITE))) + len(list(board.pieces(chess.QUEEN, chess.BLACK)))
        return queens == 0 or (white_material < 500 or black_material < 500)

    def _evaluate_material_and_position(self, board: chess.Board) -> float:
        """Material evaluation with fresh score."""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
                
            # Get base piece value
            value = self.PIECE_VALUES[piece.piece_type]
            
            # Add scaled positional bonus
            if piece.piece_type in self.PIECE_POSITION_SCORES:
                table = self.PIECE_POSITION_SCORES[piece.piece_type]
                position = square if piece.color else chess.square_mirror(square)
                value += table[position] * 0.01  # Minimal positional influence
                
            score += value if piece.color else -value
            
        return score

    def _get_position_value(self, piece: chess.Piece, square: int) -> float:
        """Gets positional value for a piece and scales it down"""
        if piece.piece_type in self.PIECE_POSITION_SCORES:
            table = self.PIECE_POSITION_SCORES[piece.piece_type]
            position = square if piece.color else chess.square_mirror(square)
            # Scale down the positional values to be less significant compared to material
            return table[position] * 0.01  # Convert to small decimal values
        return 0.0

    def _evaluate_king_safety(self, board: chess.Board) -> float:
        """Evaluates king safety including pawn shield and attacking pieces"""
        score = 0.0
        
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            if king_square is None:
                continue
                
            # Pawn shield
            shield_value = self._evaluate_pawn_shield(board, king_square, color)
            
            # King attackers
            attacker_value = self._evaluate_king_attackers(board, king_square, color)
            
            # Open files near king
            open_files_penalty = self._evaluate_king_open_files(board, king_square, color)
            
            # Combine scores with color perspective
            king_safety = shield_value - attacker_value - open_files_penalty
            score += king_safety if color else -king_safety
            
        return score

    def _evaluate_pawn_shield(self, board: chess.Board, king_square: int, color: bool) -> float:
        """Evaluates pawn protection in front of king"""
        score = 0.0
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        
        # Check pawns in front of king
        shield_ranks = range(king_rank + (1 if color else -1), 
                           king_rank + (3 if color else -3), 
                           1 if color else -1)
        
        for file in range(max(0, king_file - 1), min(8, king_file + 2)):
            for rank in shield_ranks:
                if 0 <= rank < 8:
                    square = chess.square(file, rank)
                    piece = board.piece_at(square)
                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        score += 10
                        # Bonus for pawns directly in front of king
                        if file == king_file:
                            score += 5
                            
        return score

    def _evaluate_king_attackers(self, board: chess.Board, king_square: int, king_color: bool) -> float:
        """Evaluates pieces attacking squares around the king"""
        attacker_value = 0.0
        
        # Define king zone
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        king_zone = set()
        
        # Add squares around king to king zone
        for f in range(max(0, king_file - 1), min(8, king_file + 2)):
            for r in range(max(0, king_rank - 1), min(8, king_rank + 2)):
                king_zone.add(chess.square(f, r))
                
        # Count attackers and their value
        attacking_color = not king_color
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == attacking_color:
                for zone_square in king_zone:
                    if board.is_attacked_by(attacking_color, zone_square):
                        attacker_value += self.PIECE_VALUES[piece.piece_type] * 0.1
                        break
                        
        return attacker_value
    
    def _evaluate_king_open_files(self, board: chess.Board, king_square: int, color: bool) -> float:
        """Penalizes open files near the king"""
        penalty = 0.0
        king_file = chess.square_file(king_square)
        
        # Check files around king
        for file in range(max(0, king_file - 1), min(8, king_file + 2)):
            has_friendly_pawn = False
            has_enemy_pawn = False
            
            # Check for pawns on the file
            for rank in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color == color:
                        has_friendly_pawn = True
                    else:
                        has_enemy_pawn = True
            
            # Penalize open and half-open files
            if not has_friendly_pawn:
                penalty += 20
                if not has_enemy_pawn:  # Completely open file
                    penalty += 10
                    
        return penalty

    def _evaluate_mobility(self, board: chess.Board) -> float:
        """Evaluates piece mobility"""
        score = 0.0
        
        # Store original turn
        original_turn = board.turn
        
        # Evaluate mobility for both sides
        for color in [chess.WHITE, chess.BLACK]:
            board.turn = color
            mobility = 0
            
            # Count legal moves for each piece
            for move in board.legal_moves:
                piece = board.piece_at(move.from_square)
                if piece:
                    # Weight moves differently based on piece type
                    if piece.piece_type == chess.PAWN:
                        mobility += 1
                    elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                        mobility += 2
                    elif piece.piece_type == chess.ROOK:
                        mobility += 3
                    elif piece.piece_type == chess.QUEEN:
                        mobility += 4
                        
            score += mobility if color else -mobility
            
        # Restore original turn
        board.turn = original_turn
        return score

    def _evaluate_center_control(self, board: chess.Board) -> float:
        """Evaluates control of central squares"""
        score = 0.0
        
        # Evaluate center squares control
        for square in self.CENTER_SQUARES:
            white_control = len(list(board.attackers(chess.WHITE, square)))
            black_control = len(list(board.attackers(chess.BLACK, square)))
            score += (white_control - black_control) * 10
            
            # Bonus for pieces in center
            piece = board.piece_at(square)
            if piece:
                value = 15 if piece.piece_type == chess.PAWN else 10
                score += value if piece.color else -value
                
        # Evaluate extended center control
        for square in self.EXTENDED_CENTER:
            white_control = len(list(board.attackers(chess.WHITE, square)))
            black_control = len(list(board.attackers(chess.BLACK, square)))
            score += (white_control - black_control) * 5
            
            piece = board.piece_at(square)
            if piece:
                value = 7 if piece.piece_type == chess.PAWN else 5
                score += value if piece.color else -value
                
        return score

    def _evaluate_piece_activity(self, board: chess.Board) -> float:
        """Evaluates piece activity and development"""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
                
            # Evaluate piece development in opening/middlegame
            if not self._is_endgame(board):
                if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                    # Development bonus for minor pieces
                    if piece.color == chess.WHITE:
                        if chess.square_rank(square) > 1:
                            score += 10
                    else:
                        if chess.square_rank(square) < 6:
                            score -= 10
                            
            # Evaluate piece activity
            attacks = len(list(board.attacks(square)))
            piece_activity = attacks * 2
            
            # Additional bonus for attacking center
            for center_square in self.CENTER_SQUARES:
                if board.is_attacked_by(piece.color, center_square):
                    piece_activity += 5
                    
            score += piece_activity if piece.color else -piece_activity
            
        return score

    def _evaluate_king_attack(self, board: chess.Board) -> float:
        """Evaluates attacking potential against enemy king"""
        score = 0.0
        
        for color in [chess.WHITE, chess.BLACK]:
            enemy_king_square = board.king(not color)
            if enemy_king_square is None:
                continue
                
            attack_value = 0
            attacker_count = 0
            
            # Count pieces participating in the attack
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece and piece.color == color:
                    # Check if piece is attacking king's zone
                    if self._is_attacking_king_zone(board, square, enemy_king_square):
                        attacker_count += 1
                        attack_value += self._get_attack_weight(piece.piece_type)
            
            # Apply multiplier based on number of attackers
            if attacker_count > 1:
                attack_value *= (attacker_count * 1.5)
                
            score += attack_value if color else -attack_value
            
        return score

    def _is_attacking_king_zone(self, board: chess.Board, square: int, king_square: int) -> bool:
        """Checks if a piece is attacking the king's zone"""
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        
        # Define king zone
        for f in range(max(0, king_file - 1), min(8, king_file + 2)):
            for r in range(max(0, king_rank - 1), min(8, king_rank + 2)):
                target = chess.square(f, r)
                if board.is_attacked_by(board.piece_at(square).color, target):
                    return True
        return False

    def _get_attack_weight(self, piece_type: chess.PieceType) -> float:
        """Returns the attack weight for different piece types"""
        return {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }.get(piece_type, 0)

    def _evaluate_piece_coordination(self, board: chess.Board) -> float:
        """Evaluates how well pieces work together"""
        score = 0.0
        
        # Evaluate piece pairs and coordination
        score += self._evaluate_bishop_pair(board)
        score += self._evaluate_rook_coordination(board)
        score += self._evaluate_piece_protection(board)
        
        return score

    def _evaluate_bishop_pair(self, board: chess.Board) -> float:
        """Bonus for having the bishop pair"""
        score = 0.0
        
        white_bishops = len(list(board.pieces(chess.BISHOP, chess.WHITE)))
        black_bishops = len(list(board.pieces(chess.BISHOP, chess.BLACK)))
        
        if white_bishops >= 2:
            score += 50
        if black_bishops >= 2:
            score -= 50
            
        return score

    def _evaluate_rook_coordination(self, board: chess.Board) -> float:
        """Evaluates rook coordination"""
        score = 0.0
        
        for color in [chess.WHITE, chess.BLACK]:
            rook_squares = list(board.pieces(chess.ROOK, color))
            
            if len(rook_squares) >= 2:
                # Bonus for rooks on same rank
                if any(chess.square_rank(r1) == chess.square_rank(r2) 
                      for r1 in rook_squares for r2 in rook_squares if r1 != r2):
                    score += 20 if color else -20
                    
                # Bonus for rooks on open files
                for rook_square in rook_squares:
                    if self._is_open_file(board, chess.square_file(rook_square)):
                        score += 15 if color else -15
                        
        return score

    def _is_open_file(self, board: chess.Board, file: int) -> bool:
        """Checks if a file is open (no pawns)"""
        for rank in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                return False
        return True

    def _evaluate_piece_protection(self, board: chess.Board) -> float:
        """Evaluates how well pieces protect each other"""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
                
            # Count how many pieces are protecting this piece
            defenders = len(list(board.attackers(piece.color, square)))
            if defenders > 0:
                protection_value = defenders * 5
                score += protection_value if piece.color else -protection_value
                
        return score

    def _evaluate_king_centralization(self, board: chess.Board) -> float:
        """Evaluates king centralization (especially important in endgame)"""
        score = 0.0
        
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            if king_square is None:
                continue
                
            # Calculate distance from center
            file = chess.square_file(king_square)
            rank = chess.square_rank(king_square)
            
            # Distance from center files (e, d) and ranks (4, 5)
            file_distance = min(abs(file - 3), abs(file - 4))
            rank_distance = min(abs(rank - 3), abs(rank - 4))
            
            # Closer to center is better in endgame
            centralization = 7 - (file_distance + rank_distance)
            score += centralization if color else -centralization
            
        return score

    def _evaluate_passed_pawns(self, board: chess.Board) -> float:
        """Evaluates passed pawns"""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece or piece.piece_type != chess.PAWN:
                continue
                
            if self._is_passed_pawn(board, square, piece.color):
                rank = chess.square_rank(square)
                # Higher bonus for more advanced pawns
                bonus = 50 + (rank if piece.color else 7 - rank) * 10
                score += bonus if piece.color else -bonus
                
        return score

    def _is_passed_pawn(self, board: chess.Board, square: int, color: bool) -> bool:
        """Checks if a pawn is passed"""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Direction of pawn movement
        direction = 1 if color else -1
        
        # Check for opposing pawns in front of this pawn
        for r in range(rank + direction, 8 if direction == 1 else -1, direction):
            for f in range(max(0, file - 1), min(8, file + 2)):
                check_square = chess.square(f, r)
                piece = board.piece_at(check_square)
                if piece and piece.piece_type == chess.PAWN and piece.color != color:
                    return False
                    
        return True

    def _evaluate_pawn_structure(self, board: chess.Board) -> float:
        """Evaluates pawn structure"""
        score = 0.0
        
        # Evaluate different pawn structure aspects
        score += self._evaluate_pawn_chains(board)
        score += self._evaluate_isolated_pawns(board)
        score += self._evaluate_doubled_pawns(board)
        
        return score
    
    def _evaluate_pawn_chains(self, board: chess.Board) -> float:
        """Evaluates pawn chains"""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece or piece.piece_type != chess.PAWN:
                continue
                
            # Check for pawns protecting each other
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            
            for f in [file - 1, file + 1]:
                if 0 <= f < 8:
                    protect_rank = rank - 1 if piece.color else rank + 1
                    if 0 <= protect_rank < 8:
                        protect_square = chess.square(f, protect_rank)
                        protector = board.piece_at(protect_square)
                        if protector and protector.piece_type == chess.PAWN and protector.color == piece.color:
                            score += 10 if piece.color else -10
                            
        return score

    def _evaluate_isolated_pawns(self, board: chess.Board) -> float:
        """Evaluates isolated pawns"""
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece or piece.piece_type != chess.PAWN:
                continue
                
            file = chess.square_file(square)
            isolated = True
            
            # Check adjacent files for friendly pawns
            for f in [file - 1, file + 1]:
                if 0 <= f < 8:
                    for r in range(8):
                        check_square = chess.square(f, r)
                        check_piece = board.piece_at(check_square)
                        if check_piece and check_piece.piece_type == chess.PAWN and check_piece.color == piece.color:
                            isolated = False
                            break
                            
            if isolated:
                score -= 20 if piece.color else 20
                
        return score

    def _evaluate_doubled_pawns(self, board: chess.Board) -> float:
        """Evaluates doubled pawns"""
        score = 0.0
        
        # Count pawns on each file
        for file in range(8):
            white_pawns = 0
            black_pawns = 0
            
            for rank in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color:
                        white_pawns += 1
                    else:
                        black_pawns += 1
                        
            # Penalty for doubled pawns
            if white_pawns > 1:
                score -= (white_pawns - 1) * 15
            if black_pawns > 1:
                score += (black_pawns - 1) * 15
                
        return score

    def _evaluate_mobility_new(self, board: chess.Board) -> float:
        """Normalized mobility evaluation"""
        score = 0
        original_turn = board.turn
        
        for color in [chess.WHITE, chess.BLACK]:
            board.turn = color
            mobility = 0
            for piece_type, bonus in self.MOBILITY_BONUS.items():
                for square in board.pieces(piece_type, color):
                    moves = len([move for move in board.legal_moves 
                               if move.from_square == square])
                    mobility += moves * bonus
            # Normalize mobility score
            score += (mobility * 0.1) if color else -(mobility * 0.1)
                    
        board.turn = original_turn
        return score