def parse_fen(fen):
    parts = fen.split()
    board_part = parts[0]
    rows = board_part.split('/')
    board = []
    for row in rows:
        board_row = []
        for c in row:
            if c.isdigit():
                board_row.extend(['.'] * int(c))
            else:
                board_row.append(c)
        board.append(board_row)
    active_color = parts[1]
    castling_rights = parts[2] if len(parts) > 2 else 'KQkq'
    en_passant = parts[3] if len(parts) > 3 else '-'
    return board, active_color, castling_rights, en_passant

def is_attacked(pos, board, color):
    row, col = pos
    enemy_color = 'b' if color == 'w' else 'w'
    # Check pawn attacks
    if color == 'w':
        if row < 7:
            if col > 0 and board[row+1][col-1] == 'p':
                return True
            if col < 7 and board[row+1][col+1] == 'p':
                return True
    else:
        if row > 0:
            if col > 0 and board[row-1][col-1] == 'P':
                return True
            if col < 7 and board[row-1][col+1] == 'P':
                return True
    # Check knight attacks
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        r = row + dr
        c = col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            piece = board[r][c]
            if (enemy_color == 'b' and piece == 'n') or (enemy_color == 'w' and piece == 'N'):
                return True
    # Check sliding pieces (bishop, rook, queen) and king
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row, col
        while True:
            r += dr
            c += dc
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            piece = board[r][c]
            if piece == '.':
                continue
            if (enemy_color == 'w' and piece.isupper()) or (enemy_color == 'b' and piece.islower()):
                if (dr == 0 or dc == 0):  # Rook or Queen in straight line
                    if piece.lower() in ['r', 'q']:
                        return True
                else:  # Bishop or Queen in diagonal
                    if piece.lower() in ['b', 'q']:
                        return True
                # King check (distance 1)
                if piece.lower() == 'k' and abs(r - row) <= 1 and abs(c - col) <= 1:
                    return True
                break
            else:
                break
    return False

def generate_pawn_moves(board, row, col, active_color, en_passant):
    moves = []
    if active_color == 'w':
        direction = -1
        start_row = 6
        promotion_row = 0
    else:
        direction = 1
        start_row = 1
        promotion_row = 7
    new_row = row + direction
    if 0 <= new_row < 8:
        # Forward moves
        if board[new_row][col] == '.':
            if new_row == promotion_row:
                for promo in ['Q', 'R', 'B', 'N']:
                    moves.append(((row, col), (new_row, col), promo))
            else:
                moves.append(((row, col), (new_row, col), None))
            # Two-square move
            if row == start_row:
                new_row2 = row + 2 * direction
                if board[new_row2][col] == '.':
                    moves.append(((row, col), (new_row2, col), None))
        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target != '.' and ((active_color == 'w' and target.islower()) or (active_color == 'b' and target.isupper())):
                    if new_row == promotion_row:
                        for promo in ['Q', 'R', 'B', 'N']:
                            moves.append(((row, col), (new_row, new_col), promo))
                    else:
                        moves.append(((row, col), (new_row, new_col), None))
                # En passant
                elif en_passant != '-':
                    ep_row = 8 - int(en_passant[1])
                    ep_col = ord(en_passant[0]) - ord('a')
                    if active_color == 'w' and row == 3 and new_row == ep_row and new_col == ep_col:
                        moves.append(((row, col), (ep_row, ep_col), None))
                    elif active_color == 'b' and row == 4 and new_row == ep_row and new_col == ep_col:
                        moves.append(((row, col), (ep_row, ep_col), None))
    return moves

def generate_knight_moves(board, row, col, active_color):
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in knight_moves:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == '.' or (active_color == 'w' and target.islower()) or (active_color == 'b' and target.isupper()):
                moves.append(((row, col), (new_row, new_col), None))
    return moves

def generate_slider_moves(board, row, col, active_color, directions):
    moves = []
    for dr, dc in directions:
        new_row, new_col = row, col
        while True:
            new_row += dr
            new_col += dc
            if not (0 <= new_row < 8 and 0 <= new_col < 8):
                break
            target = board[new_row][new_col]
            if target == '.':
                moves.append(((row, col), (new_row, new_col), None))
            else:
                if (active_color == 'w' and target.islower()) or (active_color == 'b' and target.isupper()):
                    moves.append(((row, col), (new_row, new_col), None))
                break
    return moves

def generate_bishop_moves(board, row, col, active_color):
    return generate_slider_moves(board, row, col, active_color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

def generate_rook_moves(board, row, col, active_color):
    return generate_slider_moves(board, row, col, active_color, [(-1, 0), (1, 0), (0, -1), (0, 1)])

def generate_queen_moves(board, row, col, active_color):
    return generate_rook_moves(board, row, col, active_color) + generate_bishop_moves(board, row, col, active_color)

def generate_king_moves(board, row, col, active_color, castling_rights):
    moves = []
    king_moves = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_moves:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == '.' or (active_color == 'w' and target.islower()) or (active_color == 'b' and target.isupper()):
                moves.append(((row, col), (new_row, new_col), None))
    # Castling
    if active_color == 'w':
        if 'K' in castling_rights and board[7][5] == '.' and board[7][6] == '.' and board[7][4] == 'K' and board[7][7] == 'R':
            if not is_attacked((7,4), board, 'w') and not is_attacked((7,5), board, 'w') and not is_attacked((7,6), board, 'w'):
                moves.append(((7,4), (7,6), None))
        if 'Q' in castling_rights and board[7][1] == '.' and board[7][2] == '.' and board[7][3] == '.' and board[7][4] == 'K' and board[7][0] == 'R':
            if not is_attacked((7,4), board, 'w') and not is_attacked((7,3), board, 'w') and not is_attacked((7,2), board, 'w'):
                moves.append(((7,4), (7,2), None))
    else:
        if 'k' in castling_rights and board[0][5] == '.' and board[0][6] == '.' and board[0][4] == 'k' and board[0][7] == 'r':
            if not is_attacked((0,4), board, 'b') and not is_attacked((0,5), board, 'b') and not is_attacked((0,6), board, 'b'):
                moves.append(((0,4), (0,6), None))
        if 'q' in castling_rights and board[0][1] == '.' and board[0][2] == '.' and board[0][3] == '.' and board[0][4] == 'k' and board[0][0] == 'r':
            if not is_attacked((0,4), board, 'b') and not is_attacked((0,3), board, 'b') and not is_attacked((0,2), board, 'b'):
                moves.append(((0,4), (0,2), None))
    return moves

def generate_pseudo_legal_moves(board, active_color, castling_rights, en_passant):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (active_color == 'w' and piece.isupper()) or (active_color == 'b' and piece.islower()):
                if piece.lower() == 'p':
                    moves += generate_pawn_moves(board, row, col, active_color, en_passant)
                elif piece.lower() == 'n':
                    moves += generate_knight_moves(board, row, col, active_color)
                elif piece.lower() == 'b':
                    moves += generate_bishop_moves(board, row, col, active_color)
                elif piece.lower() == 'r':
                    moves += generate_rook_moves(board, row, col, active_color)
                elif piece.lower() == 'q':
                    moves += generate_queen_moves(board, row, col, active_color)
                elif piece.lower() == 'k':
                    moves += generate_king_moves(board, row, col, active_color, castling_rights)
    return moves

def validate_move(move, board, active_color):
    temp_board = [row.copy() for row in board]
    (start_row, start_col), (end_row, end_col), promo = move
    piece = temp_board[start_row][start_col]
    # Handle castling
    if piece.lower() == 'k' and abs(start_col - end_col) == 2:
        if end_col == 6:  # Kingside
            rook_col = 7
            new_rook_col = 5
        else:  # Queenside
            rook_col = 0
            new_rook_col = 3
        temp_board[start_row][new_rook_col] = temp_board[start_row][rook_col]
        temp_board[start_row][rook_col] = '.'
    # Handle en passant
    elif piece.lower() == 'p' and (end_col != start_col) and temp_board[end_row][end_col] == '.':
        if active_color == 'w':
            captured_row = end_row + 1
        else:
            captured_row = end_row - 1
        temp_board[captured_row][end_col] = '.'
    # Update the board
    temp_board[end_row][end_col] = piece
    temp_board[start_row][start_col] = '.'
    if promo:
        temp_board[end_row][end_col] = promo if active_color == 'w' else promo.lower()
    # Find the king's position
    king_pos = None
    for r in range(8):
        for c in range(8):
            p = temp_board[r][c]
            if p.lower() == 'k' and ((active_color == 'w' and p == 'K') or (active_color == 'b' and p == 'k')):
                king_pos = (r, c)
                break
        if king_pos:
            break
    # Check if the king is attacked
    return not is_attacked(king_pos, temp_board, active_color)

def generate_legal_moves(fen):
    board, active_color, castling_rights, en_passant = parse_fen(fen)
    pseudo_legal = generate_pseudo_legal_moves(board, active_color, castling_rights, en_passant)
    legal_moves = []
    for move in pseudo_legal:
        if validate_move(move, board, active_color):
            legal_moves.append(move)
    return legal_moves

def move_to_san(move, board, active_color):
    (start_row, start_col), (end_row, end_col), promo = move
    piece = board[start_row][start_col]
    # Castling
    if piece.lower() == 'k' and abs(start_col - end_col) == 2:
        return 'O-O' if end_col == 6 else 'O-O-O'
    # Pawn moves
    san = ''
    piece_type = piece.upper()
    if piece.lower() == 'p':
        capture = board[end_row][end_col] != '.' or (start_col != end_col and board[end_row][end_col] == '.' and en_passant != '-')
        if capture:
            san = f"{chr(start_col + ord('a'))}x{chr(end_col + ord('a'))}{8 - end_row}"
        else:
            san = f"{chr(end_col + ord('a'))}{8 - end_row}"
        if promo:
            san += f'={promo.upper()}'
        return san
    # Other pieces
    san = piece_type
    # Find ambiguous moves
    same_piece_moves = []
    for r in range(8):
        for c in range(8):
            if (r, c) == (start_row, start_col):
                continue
            p = board[r][c]
            if p.lower() == piece.lower() and ((active_color == 'w' and p.isupper()) or (active_color == 'b' and p.islower())):
                temp_moves = []
                if p.lower() == 'n':
                    temp_moves = generate_knight_moves(board, r, c, active_color)
                elif p.lower() == 'b':
                    temp_moves = generate_bishop_moves(board, r, c, active_color)
                elif p.lower() == 'r':
                    temp_moves = generate_rook_moves(board, r, c, active_color)
                elif p.lower() == 'q':
                    temp_moves = generate_queen_moves(board, r, c, active_color)
                elif p.lower() == 'k':
                    temp_moves = generate_king_moves(board, r, c, active_color, castling_rights)
                for m in temp_moves:
                    if m[1][0] == end_row and m[1][1] == end_col:
                        same_piece_moves.append((r, c))
                        break
    # Add disambiguation
    if same_piece_moves:
        same_file = any(c == start_col for (r, c) in same_piece_moves)
        same_rank = any(r == start_row for (r, c) in same_piece_moves)
        if same_file or same_rank:
            if same_file and same_rank:
                san += f"{chr(start_col + ord('a'))}{8 - start_row}"
            elif same_file:
                san += f"{8 - start_row}"
            else:
                san += f"{chr(start_col + ord('a'))}"
        else:
            san += f"{chr(start_col + ord('a'))}"
    # Capture
    if board[end_row][end_col] != '.':
        san += 'x'
    # Destination
    san += f"{chr(end_col + ord('a'))}{8 - end_row}"
    # Promotion
    if promo:
        san += f'={promo.upper()}'
    return san

def get_legal_moves(fen):
    legal_moves = generate_legal_moves(fen)
    board, active_color, _, _ = parse_fen(fen)
    san_moves = []
    for move in legal_moves:
        san = move_to_san(move, board, active_color)
        san_moves.append(san)
    return sorted(san_moves)

# Example usage:
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
print(get_legal_moves(fen))