from stockfish import Stockfish

dir = r".\stockfish\stockfish-windows-x86-64-avx2.exe"

stockfish = Stockfish(path = dir)

stockfish.set_position(["e2e4", "e7e6"])

print(stockfish.get_best_move())



