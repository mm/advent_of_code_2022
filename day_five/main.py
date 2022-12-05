from typing import Generator, Optional, List
from dataclasses import dataclass

@dataclass
class Instruction:
    amount: int
    target: int
    destination: int

def input_instructions(input_filename: str, start_at_line: int) -> Generator[Optional[Instruction], None, None]:
    """
    Successively returns instructions from the input file. Blank lines return as None.
    """
    with open(input_filename, "r") as in_file:
        i = 0
        for line in in_file:
            current_line = str(line.strip())
            if i >= start_at_line:
                if current_line == "":
                    yield None
                else:
                    split_instruction = current_line.split(' ')
                    amount, target, destination = [int(instruction) for instruction in split_instruction if instruction.isnumeric()]
                    yield Instruction(
                        amount=amount,
                        target=target,
                        destination=destination
                    )
            i += 1

def build_crate_stacks(input_filename: str) -> List[List[str]]:
    list_of_stacks = []

    raw_strings = []
    with open(input_filename, "r") as in_file:
        for line in in_file:
            if line == '\n':
                break
            raw_strings.append(line)
    
    # Now, read the stack descriptions in reverse:
    stack_numbers = [int(number) for number in raw_strings[-1].strip().split(' ') if number != '']
    number_of_stacks = max(stack_numbers) - 1

    list_of_stacks = [[] for _ in range(0, number_of_stacks+1)]
    
    stack_number = 0
    # Starting at the end of the crate description (above the 1...9 listing)
    # iterate through each row of crates.
    for raw_stack_desc in raw_strings[-2::-1]:
        stack_without_brackets = list(raw_stack_desc)
        
        i = 1
        # Every 4 characters (starting at the 2nd), we check to see if the "space"
        # for a crate stack actually has a crate.
        for i in range(i, len(stack_without_brackets)+1, 4):
            crate = stack_without_brackets[i]
            if crate.isalpha():
                # Add the crate into the list of stacks:
                list_of_stacks[stack_number].append(crate)
            # The next iteration of this loop will check the next stack:
            stack_number += 1
        
        # We're done looking through this "slice" of all stacks, so go back to stack 0:
        stack_number = 0
    
    return list_of_stacks



all_crate_stacks = build_crate_stacks("../inputs/day_five.txt")

def crate_mover_9000(crate_stacks: List[List[str]]):
    for instruction in input_instructions("../inputs/day_five.txt", start_at_line=10):
        # Execute the crane moving instructions to move crates from one stack to another.
        actual_target = instruction.target - 1
        actual_destination = instruction.destination - 1
        # Since these are stacks, the "moves" are just pops off the top, sequentially:
        if instruction.amount >= 1:
            for _ in range(0, instruction.amount):
                crate_popped = crate_stacks[actual_target].pop()
                crate_stacks[actual_destination].append(crate_popped)
    
    print(''.join([stack[-1] for stack in all_crate_stacks]))

def crate_mover_9001(crate_stacks: List[List[str]]):
    for instruction in input_instructions("../inputs/day_five.txt", start_at_line=10):
        # Execute the crane moving instructions to move crates from one stack to another.
        actual_target = instruction.target - 1
        actual_destination = instruction.destination - 1
        if instruction.amount >= 1:
            # In this case, we aren't just popping off the top and adding. Rather, we want to preserve
            # the order of the crates we're adding and adding them as a group -- so we create a list of
            # crates to add and add them in reverse order.
            crates_to_add = []
            for _ in range(0, instruction.amount):
                crate_popped = crate_stacks[actual_target].pop()
                crates_to_add.append(crate_popped)
            crate_stacks[actual_destination].extend(reversed(crates_to_add))
    
    print(''.join([stack[-1] for stack in all_crate_stacks]))

# crate_mover_9000(all_crate_stacks)
crate_mover_9001(all_crate_stacks)