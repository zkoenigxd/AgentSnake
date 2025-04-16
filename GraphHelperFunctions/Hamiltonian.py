def base_cycle(top, bottom, left, right):
    """
    Construct a Hamiltonian cycle for a 2 x k or k x 2 solid grid.
    We assume here that the subgrid has at least 2 rows and 2 columns.
    """
    R = bottom - top + 1
    C = right - left + 1
    cycle = []
    # Case 1: exactly 2 rows.
    if R == 2:
        # Top row: left -> right
        for j in range(left, right + 1):
            cycle.append((top, j))
        # Bottom row: right -> left
        for j in range(right, left - 1, -1):
            cycle.append((bottom, j))
        return cycle
    # Case 2: exactly 2 columns.
    if C == 2:
        # Left column: top -> bottom
        for i in range(top, bottom + 1):
            cycle.append((i, left))
        # Right column: bottom -> top
        for i in range(bottom, top - 1, -1):
            cycle.append((i, right))
        return cycle

    # Fallback (should not normally happen for a solid subgrid)
    # Simply do the boundary cycle.
    cycle = []
    for j in range(left, right + 1):
        cycle.append((top, j))
    for i in range(top + 1, bottom + 1):
        cycle.append((i, right))
    for j in range(right - 1, left - 1, -1):
        cycle.append((bottom, j))
    for i in range(bottom - 1, top, -1):
        cycle.append((i, left))
    return cycle

def find_hamiltonian_cycle_in_grid(n, m):
    """
    Given grid dimensions n x m (n rows, m columns), returns a Hamiltonian cycle
    covering all cells (as a list of (row, col) tuples) if one exists.
    Assumes that n * m is even (a necessary condition) and that the grid is solid.
    """
    if (n * m) % 2 != 0:
        return None  # No cycle if the grid has an odd number of cells.
    return construct_cycle(0, n - 1, 0, m - 1)

def find_splice_indices(outer, top):
    """
    Find a pair of consecutive vertices in the outer cycle that lie on the top row.
    Because the outer cycle is constructed by listing the top row first,
    such a pair is guaranteed when the subgrid has at least 3 columns.
    Returns a tuple (ui, vi) which are indices into the list 'outer'.
    """
    for idx in range(len(outer) - 1):
        u = outer[idx]
        v = outer[idx + 1]
        if u[0] == top and v[0] == top:
            return idx, idx + 1
    # In the unlikely event no such pair is found, fall back to the first pair.
    return 0, 1

def construct_cycle(top, bottom, left, right):
    """
    Recursively constructs a Hamiltonian cycle on the rectangular subgrid defined by
    rows top..bottom and columns left..right.
    """
    R = bottom - top + 1
    C = right - left + 1

    # Base case: if one dimension is 2, then build a simple cycle.
    if R == 2 or C == 2:
        return base_cycle(top, bottom, left, right)

    # Step 1: Build the outer boundary cycle.
    outer = []

    # Top row: from left to right.
    for j in range(left, right + 1):
        outer.append((top, j))
    # Right column: from top+1 to bottom.
    for i in range(top + 1, bottom + 1):
        outer.append((i, right))
    # Bottom row: from right-1 downto left.
    for j in range(right - 1, left - 1, -1):
        outer.append((bottom, j))
    # Left column: from bottom-1 downto top+1.
    for i in range(bottom - 1, top, -1):
        outer.append((i, left))
    # At this point, 'outer' is the cycle around the boundary.

    # Step 2: Recurse on the inner grid.
    # The inner grid is rows top+1 to bottom-1 and columns left+1 to right-1.
    if top + 1 > bottom - 1 or left + 1 > right - 1:
        return outer

    inner = construct_cycle(top + 1, bottom - 1, left + 1, right - 1)

    # Step 3: Splice the inner cycle into the outer cycle.
    # Instead of hard-coding splice points, we now search for two consecutive vertices
    # in the outer cycle that lie on the top row.
    ui, vi = find_splice_indices(outer, top)
    u = outer[ui]
    v = outer[vi]

    # For the inner cycle, we want to designate two vertices on its top boundary.
    # Because inner was built on the subgrid (top+1, left+1) to (bottom-1, right-1),
    # its outer boundary starts with the top row.
    target_start = (top + 1, left + 1)
    target_end = (top + 1, left + 2)

    # Rotate the inner cycle so that the first element is target_start.
    # (If target_start is not in inner, then our subgrid was built differently; in practice,
    # for a solid grid it should be present.)
    while inner[0] != target_start:
        inner = inner[1:] + [inner[0]]
    # Rotate until the last element is target_end.
    while inner[-1] != target_end:
        inner = [inner[-1]] + inner[:-1]

    # Now, remove the edge (u, v) from the outer cycle and splice in the inner cycle.
    # We construct the new cycle as:
    #    outer[0:ui+1] + inner + outer[vi:]
    new_cycle = outer[:ui + 1] + inner + outer[vi:]
    return new_cycle
