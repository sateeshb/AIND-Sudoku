assignments = []
rows = 'ABCDEFGHI'
columns = '123456789'
row_grids = 'ABC','DEF', 'GHI'
cols_grids = '123', '456', '789'
grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
grid2 = grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
max_values = '123456789'


def cross(A, B):
    return [a + b for a in A for b in B]


row_units = [cross(r, columns) for r in rows]
column_units = [cross(rows, c) for c in columns]
square_units = [cross(ros,colms) for ros in (row_grids) for colms in (cols_grids)]

boxes = cross(rows, columns)


#diagonal units
l = len(rows)
#['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
left_diagonal_unit = [rows[i]+columns[i] for i in range(l)]  
#['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
right_diagonal_unit =  [rows[l-1-i]+columns[i] for i in range(l-1,-1,-1)]           
#all diagonal units
diagonal_units = [left_diagonal_unit,
                 right_diagonal_unit]

unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def display(values):
    """
    Input: The sudoku in dictionary form
    Output: None
    Display the values as a grid.
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    empty_value = '.'
    default_values = '123456789'
    all_values = []
    
    for e in grid:
        if e is empty_value:
            all_values.append(default_values);
        elif e in default_values:
            all_values.append(e)
    assert len(grid) == 81
    return dict(zip(boxes, all_values))


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    sloved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in sloved_values:
        value = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(value, '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for digit in max_values:
            places = [box for box in unit if digit in values[box]]
            if len(places) == 1:
               values[places[0]] = digit
    return values


def assign_value(values, box, value):
    """
    use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """
    Go through all the units, and whenever there is a twins in a row and column 
    search for that twins in that row and column and remove those values from 
    that boxes.
    whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after removing each twins in each
    row and column.
    """
    for unit in column_units+row_units:
        #finding all the possible twins from the grid
        maybe_twins = [values[box] for box in unit if len(values[box]) == 2]
        
        #finding the actual twins in the unit
        twins = [check for n, check in enumerate(maybe_twins) if check in maybe_twins[:n]]
        # removing naked twins from peers
        for twin_value in twins:
            for peer in unit:  
                # removing digit from each peer and not the actual twins.
                if len(values[peer]) > 1 and values[peer] != twin_value:
                    for digit in twin_value:
                        values = assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')