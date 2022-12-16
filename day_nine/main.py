from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Knot:
    x: int = 0
    y: int = 0

HORIZONTAL_MOVES = {
    "R": lambda x, y: (x+1, y),
    "L": lambda x, y: (x-1, y),
}

VERTICAL_MOVES = {
    "U": lambda x, y: (x, y+1),
    "D": lambda x, y: (x, y-1),
}

DIAGONAL_MOVES = {
    "UR": lambda x, y: (x+1, y+1),
    "UL": lambda x, y: (x-1, y+1),
    "DR": lambda x, y: (x+1, y-1),
    "DL": lambda x, y: (x-1, y-1)
}

POSSIBLE_MOVES = {**HORIZONTAL_MOVES, **VERTICAL_MOVES, **DIAGONAL_MOVES}

def tail_adjacent_to_head(head_x: int, head_y: int, tail_x: int, tail_y: int):
    """
    Is the tail adjacent to the head in 2D space? (touching diagonally
    counts as adjacency, so does overlapping)
    """

    if (head_x, head_y) == (tail_x, tail_y):
        # overlapping
        return True

    if ((tail_x + 1 == head_x) or (tail_x - 1 == head_x)) and (tail_y == head_y):
        # adjacent horizontally
        return True

    if ((tail_y + 1 == head_y) or (tail_y - 1 == head_y)) and (tail_x == head_x):
        # adjacent vertically
        return True

    if (tail_x + 1, tail_y + 1) == (head_x, head_y):
        # adjacent diagonally
        return True

    if (tail_x - 1, tail_y - 1) == (head_x, head_y):
        # adjacent diagonally
        return True

    if (tail_x + 1, tail_y - 1) == (head_x, head_y):
        # adjacent diagonally
        return True

    if (tail_x - 1, tail_y + 1) == (head_x, head_y):
        # adjacent diagonally
        return True

    return False

def find_adjacent_position(head_x: int, head_y: int, tail_x: int, tail_y: int) -> Tuple[int, int]:
    """
    Super naively try to figure out a new position for the tail that
    will make it adjacent to the head.
    """

    in_same_column = head_x == tail_x
    in_same_row = head_y == tail_y

    if in_same_row:
        allowed_moves = HORIZONTAL_MOVES
    elif in_same_column:
        allowed_moves = VERTICAL_MOVES
    else:
        allowed_moves = DIAGONAL_MOVES

    for move, mover in allowed_moves.items():
        new_tail_x, new_tail_y = mover(tail_x, tail_y)
        is_adjacent = tail_adjacent_to_head(head_x, head_y, new_tail_x, new_tail_y)

        if is_adjacent:
            return (new_tail_x, new_tail_y)
    
    # One of these should have made us adjacent. If we reach here, something happened:
    raise ValueError("There's no way to make the head and tail adjacent")


def build_moveset(input_filename: str) -> List[Tuple[str, int]]:
    """
    Builds all the moves the head will make. Will "flatten" moves, i.e.
    R 4 will become a sequence of (R, 1), (R, 1), (R, 1), (R, 1)
    """
    moveset = []
    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            direction, amount = current_line.split(" ")
            total_move_amount = int(amount)

            for _ in range(0, total_move_amount):
                moveset.append((direction, 1))
    return moveset


def part_one():
    """
    Assumes we have *one* knot (the tail) that follows the head.
    """
    all_head_moves = build_moveset("../inputs/day_nine.txt")

    head = Knot(x=0, y=0)
    tail = Knot(x=0, y=0)

    tail_history = set([(0,0)])

    print(head)
    for move, _ in all_head_moves:
        # Function that will return the new coordinates for the head:
        mover_method = POSSIBLE_MOVES[move]
        # Move the head:
        new_x, new_y = mover_method(head.x, head.y)
        head.x = new_x
        head.y = new_y

        # Now, make the tail try to chase the head!
        if not tail_adjacent_to_head(head.x, head.y, tail.x, tail.y):
            # Try out all possibilities
            new_tail_x, new_tail_y = find_adjacent_position(head.x, head.y, tail.x, tail.y)
            tail.x = new_tail_x
            tail.y = new_tail_y
            tail_history.add((tail.x, tail.y))

    print(tail)
    print(len(tail_history))

def part_two():
    """
    Assumes we have 9 knots that all follow the head in the same fashion, one
    after the other.
    """
    all_head_moves = build_moveset("../inputs/day_nine.txt")

    knots = [Knot(x=0, y=0) for _ in range(0, 10)]
    head_of_rope_index = 0
    tail_of_rope_index = 9

    tail_history = set([(0,0)])

    for move, _ in all_head_moves:
        head_index = 0
        tail_index = 1

        for i in range(0, 9):
            head = knots[head_index]
            tail = knots[tail_index]

            if head_index == head_of_rope_index:
                # Move the head of the rope if we're at the beginning:
                mover_method = POSSIBLE_MOVES[move]
                new_x, new_y = mover_method(head.x, head.y)
                head.x = new_x
                head.y = new_y

            # Check if the current tail is adjacent/overlapping the current head. If so,
            # nothing to do -- otherwise move it!
            # Now, make the tail try to chase the head!
            if not tail_adjacent_to_head(head.x, head.y, tail.x, tail.y):
                # Try out all possibilities
                new_tail_x, new_tail_y = find_adjacent_position(head.x, head.y, tail.x, tail.y)
                tail.x = new_tail_x
                tail.y = new_tail_y

            if tail_index == tail_of_rope_index:
                # At the final knot (the "true" tail) Here, we care about saving the position.
                tail_history.add((tail.x, tail.y))
            head_index += 1
            tail_index += 1
    
    print(len(tail_history))

part_two()