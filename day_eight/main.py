from typing import List

def build_grid_from_file(input_filename: str) -> List[List[int]]:
    with open(input_filename, "r") as in_file:
        tree_grid = []
        for tree_row in in_file:
            current_row = [int(tree_height) for tree_height in list(str(tree_row.strip()))]
            tree_grid.append(current_row)
        return tree_grid

grid = build_grid_from_file("../inputs/day_eight.txt")

def trees_above_current_tree(grid: List[List[int]], row_number: int, column_number: int) -> List[int]:
    """
    Returns the heights of all trees above the current tree, starting with the tree closest to the current
    one.
    """
    trees = []
    for current_row_number, tree_row in enumerate(grid):
        if current_row_number < row_number:
            tree_to_evaluate = tree_row[column_number]
            trees.append(tree_to_evaluate)
    return reversed(trees)

def trees_below_current_tree(grid: List[List[int]], row_number: int, column_number: int) -> List[int]:
    """
    Returns the heights of all trees below the current tree, starting with the tree closest to the current
    one.
    """
    trees = []
    for current_row_number, tree_row in enumerate(grid):
        if current_row_number > row_number:
            tree_to_evaluate = tree_row[column_number]
            trees.append(tree_to_evaluate)
    return trees

def trees_left_of_current_tree(grid: List[List[int]], row_number: int, column_number: int) -> List[int]:
    """
    Returns the heights of all trees to the left of the current tree, starting with the tree closest to the current
    one.
    """
    return reversed(grid[row_number][0:column_number])

def trees_right_of_current_tree(grid: List[List[int]], row_number: int, column_number: int) -> List[int]:
    """
    Returns the heights of all trees to the right of the current tree, starting with the tree closest to the current
    one.
    """
    return grid[row_number][column_number+1:]

def get_scenic_score(current_tree_height: int, other_tree_heights: List[int]) -> int:
    scenic_score = 0
    for tree_height in other_tree_heights:
        scenic_score += 1
        if tree_height >= current_tree_height:
            break
    return scenic_score

num_trees_visible = 0

BACK_EDGE_ROW = 0
FRONT_EDGE_ROW = len(grid) - 1

def part_one():
    """
    How many trees are "visible"? (from any direction)
    """
    for row_number, tree_row in enumerate(grid):
        left_edge_column = 0
        right_edge_column = len(tree_row) - 1
        for column_number, tree_height in enumerate(tree_row):
            # Edge detection: Is the tree on an edge?
            if column_number in (left_edge_column, right_edge_column) or row_number in (BACK_EDGE_ROW, FRONT_EDGE_ROW):
                # Tree is visible from all directions - it's on an edge:
                num_trees_visible += 1
            else:
                # Get all trees above and below the current one:
                trees_above = trees_above_current_tree(grid, row_number, column_number)
                trees_below = trees_below_current_tree(grid, row_number, column_number)
                trees_left = trees_left_of_current_tree(grid, row_number, column_number)
                trees_right = trees_right_of_current_tree(grid, row_number, column_number)

                # A tree is "visible" from a direction if all trees in that direction are shorter
                # than it.
                visible_top = all(x < tree_height for x in trees_above)
                visible_bottom = all(x < tree_height for x in trees_below)
                visible_left = all(x < tree_height for x in trees_left)
                visible_right = all(x < tree_height for x in trees_right)

                if any([visible_top, visible_bottom, visible_left, visible_right]):
                    num_trees_visible += 1

    print(num_trees_visible)

def part_two():
    """
    What is the maximum scenic score you could achieve with the trees?
    """
    max_scenic_score = 1
    for row_number, tree_row in enumerate(grid):
        left_edge_column = 0
        right_edge_column = len(tree_row) - 1
        for column_number, tree_height in enumerate(tree_row):
            if column_number in (left_edge_column, right_edge_column) or row_number in (BACK_EDGE_ROW, FRONT_EDGE_ROW):
                # Ignore edges
                continue

            trees_above = trees_above_current_tree(grid, row_number, column_number)
            trees_below = trees_below_current_tree(grid, row_number, column_number)
            trees_left = trees_left_of_current_tree(grid, row_number, column_number)
            trees_right = trees_right_of_current_tree(grid, row_number, column_number)

            # Get the scenic score from each direction:
            scenic_left = get_scenic_score(tree_height, trees_left)
            scenic_right = get_scenic_score(tree_height, trees_right)
            scenic_top = get_scenic_score(tree_height, trees_above)
            scenic_below = get_scenic_score(tree_height, trees_below)

            scenic_score = scenic_left*scenic_right*scenic_top*scenic_below
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
    
    print(max_scenic_score)

part_two()
