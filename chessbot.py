currentplayer = 'white'
def get_best_move():
    global currentplayer
    print("get_best_move")
    if currentplayer=='white':
        return "e2e4"
    else:
        return "e7e5"

def make_moves_from_current_position(move):
    global currentplayer
    #print("move saved")
    print("make_moves_from_current_position")
    if currentplayer == 'white':
        currentplayer = 'black'
    else:
        currentplayer = 'white'