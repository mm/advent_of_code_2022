from typing import Generator, Optional

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
PRIORITIES = {}
i = 0
for letter in ALPHABET:
    i += 1
    PRIORITIES[letter] = i

def input_lines(input_filename: str) -> Generator[Optional[str], None, None]:
    """
    Successively returns strings from the input file. Blank lines return as None.
    """
    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            if current_line == "":
                yield None
            else:
                yield current_line


def part_one():
    priority_sum = 0
    for rucksack_string in input_lines('../inputs/day_three.txt'):
        rucksack = list(rucksack_string)
        rucksack_size = len(rucksack)
        first_compartment = set(rucksack[0:(rucksack_size//2)])
        second_compartment = set(rucksack[(rucksack_size//2):])
        # What's common in both?
        intersection = first_compartment.intersection(second_compartment)

        for intersected_element in intersection:
            # get priority:
            priority = PRIORITIES[intersected_element]
            priority_sum += priority

    print(priority_sum)

def part_two():
    # Build rucksack "groups":
    current_rucksack_group = []
    i = 0
    priority_sum = 0
    for rucksack_string in input_lines('../inputs/day_three.txt'):
        current_rucksack_group.append(rucksack_string)
        if i == 2:
            # If it's the 3rd rucksack we're seeing, evaluate the group of rucksacks we have.
            # Evaluate what's common between the three rucksacks we have in the group:
            group_one, group_two, group_three = [set(rucksack) for rucksack in current_rucksack_group]
            three_way_intersection = group_one.intersection(group_two).intersection(group_three)
            # There should only be one intersection, but hey why not:
            for intersection in three_way_intersection:
                priority = PRIORITIES[intersection]
                priority_sum += priority
            # Get ready to start building up a list of rucksacks again
            i = 0
            current_rucksack_group = []
        else:
            i += 1

    print(priority_sum)

part_one()
part_two()
    