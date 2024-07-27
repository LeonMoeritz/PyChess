import chess
import chess.engine
import os

def get_best_move(fen, turn):
    stockfish_path = 'C:/Users/leonm/Desktop/stockfish/stockfish-windows-x86-64-avx2.exe'

    if not os.path.isfile(stockfish_path):
        raise FileNotFoundError(f"Stockfish executable not found at {stockfish_path}")

    board = chess.Board(fen)

    # Store the current turn from the original FEN
    current_turn = board.turn

    try:
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            print(f"Current board:\n{board}")
            result = engine.play(board, chess.engine.Limit(time=5.0))
            best_move = result.move
            print(f"Move found: {best_move}")
            
            # Apply the best move to the board
            board.push(best_move)
        
            # Return both the best move and the new FEN
            new_fen = board.fen()
            print(f"New FEN (before adjustment): {new_fen}")

            # Ensure the FEN has the same turn as the original
            new_fen = new_fen.replace(' w ', ' w ')
            new_fen = new_fen.replace(' b ', ' w ')

            print(f"Adjusted New FEN: {new_fen}")
            return best_move, new_fen

    except chess.engine.EngineTerminatedError as e:
        print(f"Stockfish engine terminated unexpectedly: {e}")
        return None, fen
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, fen
