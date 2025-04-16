def are_adjacent(a, b):
    """Return True if a and b (each a (row, col) tuple) are adjacent."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def rotate_cycle_to_close(cycle):
    """
    Rotate the cycle (a list of nodes) so that the first and last nodes become adjacent.
    Since the cycle is cyclic, if some rotation yields endpoints that are neighbors, we return that.
    """
    n = len(cycle)
    for k in range(n):
        rotated = cycle[k:] + cycle[:k]
        if are_adjacent(rotated[0], rotated[-1]):
            return rotated
    return cycle

def find_hamiltonian_cycle(m, n):
    """
    Construct a Hamiltonian cycle on an m x n grid (with m*n even)
    using one reserved boundary (either a row or a column) to connect the two ends.
    
    If m is even, we reserve the top row (row 0) and zig-zag through columns over the remaining rows.
    The interior zig-zag is arranged so that it always starts and ends in row 1.
    
    If m is odd but n is even, we reserve the leftmost column (col 0) and zig-zag through rows over the remaining columns.
    The interior zig-zag is arranged so that it always starts and ends in column 1.
    
    Otherwise (both m and n are odd) there is no Hamiltonian cycle (returns None).
    """
    # Use the provided selection strategy.
    if n % 2 == 0:
        # Reserve the top row.
        reserved_row = 0
        interior_rows = list(range(1, m))
        # Build reserved connector: all nodes in the reserved row (from left to right).
        connector = [(reserved_row, j) for j in range(n-1, -1, -1)]
        
        # Now build a zig-zag path over the interior block of rows 1 .. m-1, iterating by columns.
        # The idea is to go down each column when the column index is even,
        # and go up when it is odd, so that the top cell (row 1) is always reached first.
        interior = []
        for j in range(n):
            if j % 2 == 0:
                # Even column: traverse interior rows top-to-bottom.
                for i in interior_rows:
                    interior.append((i, j))
            else:
                # Odd column: traverse interior rows bottom-to-top.
                for i in reversed(interior_rows):
                    interior.append((i, j))
        # At this point the interior path should start at (1, 0).
        # For the zig-zag to end at the top (row 1), we require that the last column (j = n-1)
        # is odd; that is, n must be even.
        # Combine the connector (reserved row) with the interior zig-zag.
        cycle = connector + interior
        cycle.append((0 ,n - 1))
        
    elif m % 2 == 0:
        # m is odd but n is even.
        # Reserve the leftmost column.
        reserved_col = 0
        interior_cols = list(range(1, n))
        # Build reserved connector: all nodes in the reserved column (from top to bottom).
        connector = [(i, reserved_col) for i in range(m)]
        
        # Now build a zig-zag path over the interior block of columns 1 .. n-1, iterating by rows.
        # For each row, if the row index is even, traverse the interior columns left-to-right;
        # if odd, traverse right-to-left so that the leftmost interior column (col 1) is encountered at both ends.
        interior = []
        for i in range(m):
            if i % 2 == 0:
                for j in interior_cols:
                    interior.append((i, j))
            else:
                for j in reversed(interior_cols):
                    interior.append((i, j))
        # Now the interior path should start at (0, 1) and end at (m-1, 1) provided that m is even.
        # Since m is odd here, the pattern is arranged to keep the connection on column 1.
        cycle = connector + interior
        
    else:
        # Both m and n are odd -> odd total number of nodes; no Hamiltonian cycle exists.
        return None
    
    # Finally, validate that every consecutive pair (including last->first) is adjacent.
    for idx in range(len(cycle)):
        a = cycle[idx]
        b = cycle[(idx + 1) % len(cycle)]
        if not are_adjacent(a, b):
            print("Adjacency error between", a, "and", b)
            return cycle
    return cycle