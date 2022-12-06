from typing import List


def build_datastream(input_filename: str) -> List[str]:
    """
    Returns a "datastream" (a list of characters)
    """
    with open(input_filename, "r") as in_file:
        datastream = []
        for line in in_file:
            current_line = str(line.strip())
            datastream.extend(list(current_line))
        return datastream

def is_unique_sequence(list_of_characters: List[str]) -> bool:
    """
    Determines if the list of characters passed in are all unique
    """
    # if there are any duplicates, they'll be excluded by the set check:
    return len(set(list_of_characters)) == len(list_of_characters)

datastream = build_datastream("../inputs/day_six.txt")
datastream_length = len(datastream)

start_of_marker = 0
end_of_marker = 3  # can revise this to 13 for the part 2 of this problem

while end_of_marker <= datastream_length:
    marker = datastream[start_of_marker:end_of_marker+1]

    # Does this potential marker have all unique characters?
    is_unique = is_unique_sequence(marker)

    if is_unique:
        # If so, we want to print out the number of characters that need to be processed
        # before this marker is detected (you'd need to process all the characters in the sequence
        # to know this, so this would be the end of the marker range). We increment by 1 here because
        # the datastream list of characters is 0-indexed.
        print(end_of_marker+1)
        break
    start_of_marker += 1
    end_of_marker += 1