from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

def build_filename(directory_stack: List[str], filename: str):
    # eliminate leading / from the root dir
    base_name = '/'.join(directory_stack)+f"/{filename}"
    return base_name[1:]

def size_per_directory(input_filename: str) -> Dict:
    """
    Using all commands given, will produce a "flat" directory listing with the size
    of each directory based on all files within it:
    e.g
        {
            "//b": 123,
            "//b/e: 44,
            "//c/d/e: 23
        }
    """
    directory_stack = ["/"]
    dir_map = defaultdict(lambda: 0)
    dir_map["//"] = 0

    with open(input_filename, "r") as in_file:
        for line in in_file:
            current_line = str(line.strip())
            if current_line[0] == "$":
                # shell command
                split_command = current_line.split(" ")
                if split_command[1] == "ls":
                    # listing directory contents
                    continue
                else:
                    dir_to_switch_to = split_command[2]
                    if dir_to_switch_to == "/":
                        directory_stack = ["/"]
                    elif dir_to_switch_to == "..":
                        # going up one
                        directory_stack.pop()
                    else:
                        # going down a level to a sub-directory
                        directory_stack.append(dir_to_switch_to)
            else:
                # It's a directory listing -- make note of what we find!
                size_or_dir, name = current_line.split(" ")
                if size_or_dir == "dir":
                    pass
                else:
                    # issa file:
                    current_directory = '/'.join(directory_stack)
                    dir_map[current_directory+'/'] += int(size_or_dir)

    return dir_map

dir_map = size_per_directory("../inputs/day_seven.txt")
print(dir_map)

# Update sums to include parent-child relationships:
for directory_path in dir_map:
    directory_total_size = sum([value for key, value in dir_map.items() if key.startswith(directory_path)])
    dir_map[directory_path] = directory_total_size

filtered_map_keys = list(filter(lambda directory: dir_map[directory] <= 100000, dir_map))

total_sum = 0
for directory_path in filtered_map_keys:
    print(f"Including {directory_path} with a size of {dir_map[directory_path]}")
    total_sum += dir_map[directory_path]

print(total_sum)