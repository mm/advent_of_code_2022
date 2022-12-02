from typing import Generator, Optional

def input_lines(input_filename: str) -> Generator[Optional[int], None, None]:
    """
    Successively returns integers from the input file. Blank lines return as None.
    """
    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            if current_line == "":
                yield None
            else:
                yield int(current_line)


# Index 0 = total food for elf #1
# Index 1 = total calories for elf #2
elf_food_supply = []
running_total = 0
for line in input_lines("input.txt"):
    if line is None:
        elf_food_supply.append(running_total)
        running_total = 0
    else:
        running_total += line

# Now that we have calorie totals for all the elves, we can just sort the list:
sorted_food_supplies = sorted(elf_food_supply, reverse=True)

top_elf_supply = sorted_food_supplies[0]
top_three_total = sum(sorted_food_supplies[0:3])

print(f"Top elf supply: {top_elf_supply}")
print(f"Top three total: {top_three_total}")