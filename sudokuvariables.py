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
#['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
diagonal1 = [a[0]+a[1] for a in zip(rows, columns)]
#['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
diagonal2 = [a[0]+a[1] for a in zip(rows, columns[::-1])]          
#all diagonal units
diag_unitlist = [diagonal1, diagonal2] 

unit_list = row_units + column_units + square_units + diag_unitlist
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)