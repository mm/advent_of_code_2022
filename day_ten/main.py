from dataclasses import dataclass
from typing import Optional, Deque, Tuple
from collections import deque

@dataclass
class Instruction:
    command: str
    cycles: int = 1
    value: Optional[int] = None

def build_instruction_queue(input_filename: str) -> Tuple[Deque[Instruction], int]:
    """
    Builds a queue of instructions to execute. Also returns the total
    amount of CPU cycles to execute all of them, under the assumption that:
    - addx <V> takes two cycles to complete
    - noop takes one cycle to complete
    """
    cycle_count = 0
    instructions = deque()
    with open(input_filename, "r") as in_file:
        i = 0
        for line in in_file:
            split_instruction = line.strip().split(" ")
            if split_instruction[0] == "noop":
                instructions.append(Instruction(command="noop"))
                cycle_count += 1
            else:
                instructions.append(
                    Instruction(command=split_instruction[0], cycles=2, value=int(split_instruction[1]))
                )
                cycle_count += 2

    return instructions, cycle_count

instruction_queue, total_cycles = build_instruction_queue("../inputs/day_ten.txt")
x_register = 1
signal_strengths = []

for cycle in range(1, total_cycles+1):
    current_instruction = instruction_queue[0]

    if cycle == 20 or (cycle % 40 == 20):
        # The 20th cycle, or every 40 cycles after that is an "interesting value" to note,
        # and where we want to collect signal strength (cycle # * X register)
        signal_strengths.append(cycle * x_register)

    if current_instruction.command == "addx" and current_instruction.cycles == 1:
        # If we're running an add command and we only have a cycle left, this is the last cycle.
        # Make sure to actually modify the X register:
        x_register += current_instruction.value

    current_instruction.cycles -= 1
    if current_instruction.cycles == 0:
        # If this was our last cycle for this instruction, pop it off so we move on to the next
        # instruction in the queue on the next iteration.
        instruction_queue.popleft()

print(sum(signal_strengths))


