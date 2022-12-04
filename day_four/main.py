from typing import Generator, Optional, Tuple
from dataclasses import dataclass

@dataclass
class AssignmentPair:
    first_elf: Tuple[int, int]
    second_elf: Tuple[int, int]


def input_lines(input_filename: str) -> Generator[Optional[AssignmentPair], None, None]:
    """
    Successively returns integers from the input file. Blank lines return as None.
    """
    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            if current_line == "":
                yield None
            else:
                first_pair, second_pair = current_line.split(',')
                first_pair_start, first_pair_end = first_pair.split('-')
                second_pair_start, second_pair_end = second_pair.split('-')
                yield AssignmentPair(
                    first_elf=(int(first_pair_start), int(first_pair_end)),
                    second_elf=(int(second_pair_start), int(second_pair_end))
                )

number_fully_contains = 0
number_with_any_overlap = 0

for assignment_pair in input_lines('../inputs/day_four.txt'):
    first_elf_start, first_elf_end = assignment_pair.first_elf
    second_elf_start, second_elf_end = assignment_pair.second_elf

    first_elf_set = set(range(first_elf_start, first_elf_end+1))
    second_elf_set = set(range(second_elf_start, second_elf_end+1))

    overlap = first_elf_set.intersection(second_elf_set)

    # Does the overlap equal one of our ranges?
    if overlap:
        number_with_any_overlap += 1
        beginning = min(overlap)
        end = max(overlap)
        
        if (beginning, end) == assignment_pair.first_elf or (beginning, end) == assignment_pair.second_elf:
            number_fully_contains += 1

print(number_fully_contains)
print(number_with_any_overlap)