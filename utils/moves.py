from enum import Enum, auto
# Supporting class

class Moves(Enum):
    JUMP_UP = auto()
    ROLL_UNDER = auto()
    STOP = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    SHOOT = auto()
    PICK_FLAG = auto()
    DROP_FLAG = auto()
    DEFAULT = auto()
        
    
MOVE_LABELS = { ##### Temp rn only to show on cam what it is
    Moves.JUMP_UP: "Jump Up!",
    Moves.ROLL_UNDER:"Roll Under!",
    Moves.STOP: "Stop!",
    Moves.TURN_LEFT: "Turn Left!",
    Moves.TURN_RIGHT:"Turn Right!",
    Moves.SHOOT: "Shoot!",
    Moves.PICK_FLAG: "Pick Flag!",
    Moves.DROP_FLAG: "Drop Flag!",
}
def makeStr(move) -> str:
    return MOVE_LABELS[move]