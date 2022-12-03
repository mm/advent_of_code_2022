from typing import Generator, Optional
from dataclasses import dataclass

@dataclass
class Round:
    opponent_choice: str
    my_choice: str
    desired_outcome: str

OUTCOME_WIN = "win"
OUTCOME_LOSE = "lose"
OUTCOME_DRAW = "draw"
ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

# For part 2:
LETTER_TO_OUTCOME = {
    "X": OUTCOME_LOSE,
    "Y": OUTCOME_DRAW,
    "Z": OUTCOME_WIN,
}

LETTER_TO_SHAPE = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

SHAPE_SCORES = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

OUTCOME_SCORE_MAP = {
    OUTCOME_LOSE: 0,
    OUTCOME_DRAW: 3,
    OUTCOME_WIN: 6
}

CHOICE_OUTCOME_MAP = {
    # You pick:
    ROCK: {
        # They pick:
        ROCK: OUTCOME_DRAW,
        PAPER: OUTCOME_LOSE,
        SCISSORS: OUTCOME_WIN
    },
    PAPER: {
        ROCK: OUTCOME_WIN,
        PAPER: OUTCOME_DRAW,
        SCISSORS: OUTCOME_LOSE
    },
    SCISSORS: {
        ROCK: OUTCOME_LOSE,
        PAPER: OUTCOME_WIN,
        SCISSORS: OUTCOME_DRAW
    }
}

OPPONENT_OUTCOME_MAP = {
    # If you want to win:
    OUTCOME_WIN: {
        # If they play rock, you play paper:
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK
    },
    OUTCOME_LOSE: {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER
    },
    OUTCOME_DRAW: {
        ROCK: ROCK,
        PAPER: PAPER,
        SCISSORS: SCISSORS
    }
}

def score_round(opponent_shape: str, my_shape: str) -> int:
    # Outcome based on your choice and theirs:
    outcome = CHOICE_OUTCOME_MAP[my_shape][opponent_shape]

    # Score based on the outcome:
    outcome_score = OUTCOME_SCORE_MAP[outcome]

    # Score adder based on the shape you pick:
    additional_score = SHAPE_SCORES[my_shape]

    return outcome_score + additional_score


def input_lines(input_filename: str) -> Generator[Optional[Round], None, None]:
    """
    Successively returns rounds from the input file.
    """
    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            if current_line == "":
                yield None
            else:
                # Break up into two:
                opponent, me = current_line.split(" ")
                # For part 2: determine desired outcome (now that we know what this means)
                outcome = LETTER_TO_OUTCOME[me]
                yield Round(
                    opponent_choice=opponent,
                    my_choice=me,
                    desired_outcome=outcome
                )

# Part 1: Assume the second input on the line is actually the shape you play:
total_score = 0
for rps_round in input_lines("../inputs/day_two.txt"):
    opponent_shape = LETTER_TO_SHAPE[rps_round.opponent_choice]
    my_shape = LETTER_TO_SHAPE[rps_round.my_choice]
    score = score_round(opponent_shape, my_shape)
    total_score += score

print(f"Total score, part 1: {total_score}")

# Part 2: Assume the second input on the line is the way the game needs to end:
total_score = 0
for rps_round in input_lines("../inputs/day_two.txt"):
    # Now, we know what we need to pick:
    opponent_shape = LETTER_TO_SHAPE[rps_round.opponent_choice]
    desired_choice = OPPONENT_OUTCOME_MAP[rps_round.desired_outcome][opponent_shape]
    score = score_round(opponent_shape, desired_choice)
    total_score += score

print(f"Total score, part 2: {total_score}")