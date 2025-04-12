import networkx as nx
from Games.SnakeGameLogic import BlockState

def array_to_graph(state_arr):
    """
    Convert a 2D array representing the snake game state into a networkx graph.
    
    Args:
        state_arr: 2D array where each cell represents a block state (Empty, Snake, Food, Obstacle)
        
    Returns:
        networkx.Graph: A graph where nodes represent empty cells and edges represent valid moves
    """
    rows, cols = len(state_arr), len(state_arr[0])
    G = nx.Graph()
    
    # Create nodes for empty cells
    for i in range(rows):
        for j in range(cols):
            if state_arr[i][j] == BlockState.Empty:
                G.add_node((i, j))
    
    # Add edges between adjacent empty cells
    for i in range(rows):
        for j in range(cols):
            if state_arr[i][j] == BlockState.Empty:
                # Check all four directions (up, down, left, right)
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    # Check if the neighbor is within bounds and is an empty cell
                    if (0 <= ni < rows and 0 <= nj < cols and 
                        state_arr[ni][nj] == BlockState.Empty):
                        G.add_edge((i, j), (ni, nj))
    
    return G

def get_valid_moves(state_arr, position):
    """
    Get valid moves from a given position in the game state.
    
    Args:
        state_arr: 2D array representing the game state
        position: Tuple (row, col) representing the current position
        
    Returns:
        list: List of valid move positions as (row, col) tuples
    """
    rows, cols = len(state_arr), len(state_arr[0])
    i, j = position
    valid_moves = []
    
    # Check all four directions
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        # Check if the move is within bounds and leads to an empty cell
        if (0 <= ni < rows and 0 <= nj < cols and 
            state_arr[ni][nj] == BlockState.Empty):
            valid_moves.append((ni, nj))
    
    return valid_moves

def update_graph_for_snake_movement(G, state_arr, old_head_pos, new_head_pos, tail_positions):
    """
    Update an existing graph to reflect changes in the snake's position.
    
    Args:
        G: Existing networkx graph
        state_arr: Current 2D array representing the game state
        old_head_pos: Previous position of the snake's head (row, col)
        new_head_pos: New position of the snake's head (row, col)
        tail_positions: List of positions occupied by the snake's tail
        
    Returns:
        networkx.Graph: Updated graph with nodes and edges adjusted for the new snake position
    """
    rows, cols = len(state_arr), len(state_arr[0])
    
    # Remove the old tail position from the graph (if it's now empty)
    if old_head_pos in G:
        # Remove all edges connected to the old head position
        G.remove_node(old_head_pos)
    
    # Add the new head position to the graph
    if state_arr[new_head_pos[0]][new_head_pos[1]] == BlockState.Empty:
        G.add_node(new_head_pos)
        
        # Add edges to adjacent empty cells
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = new_head_pos[0] + di, new_head_pos[1] + dj
            if (0 <= ni < rows and 0 <= nj < cols and 
                state_arr[ni][nj] == BlockState.Empty):
                G.add_edge(new_head_pos, (ni, nj))
    
    # If the tail moved (snake didn't eat food), add the new empty cell
    if tail_positions and tail_positions[0] != old_head_pos:
        tail_end = tail_positions[0]
        if state_arr[tail_end[0]][tail_end[1]] == BlockState.Empty:
            G.add_node(tail_end)
            
            # Add edges to adjacent empty cells
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = tail_end[0] + di, tail_end[1] + dj
                if (0 <= ni < rows and 0 <= nj < cols and 
                    state_arr[ni][nj] == BlockState.Empty):
                    G.add_edge(tail_end, (ni, nj))
    
    return G

def update_graph_for_food(G, state_arr, old_food_pos, new_food_pos):
    """
    Update an existing graph to reflect changes in the food's position.
    
    Args:
        G: Existing networkx graph
        state_arr: Current 2D array representing the game state
        old_food_pos: Previous position of the food (row, col)
        new_food_pos: New position of the food (row, col)
        
    Returns:
        networkx.Graph: Updated graph with nodes and edges adjusted for the new food position
    """
    rows, cols = len(state_arr), len(state_arr[0])
    
    # If the old food position is now empty, add it to the graph
    if old_food_pos and state_arr[old_food_pos[0]][old_food_pos[1]] == BlockState.Empty:
        G.add_node(old_food_pos)
        
        # Add edges to adjacent empty cells
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = old_food_pos[0] + di, old_food_pos[1] + dj
            if (0 <= ni < rows and 0 <= nj < cols and 
                state_arr[ni][nj] == BlockState.Empty):
                G.add_edge(old_food_pos, (ni, nj))
    
    # If the new food position was previously empty, remove it from the graph
    if new_food_pos in G:
        G.remove_node(new_food_pos)
    
    return G
