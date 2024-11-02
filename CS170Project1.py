import copy

class Node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.child1 = None #child up
        self.child2 = None #child down
        self.child3 = None #child left
        self.child4 = None #child right
        self.heuristic_cost = 0
        self.depth = 0
        self.expanded = False #run moveset if false, nothing if true
    
def goal(puzzle_state): # takes in a puzzle state and compares to the goalstate 
    goal_state = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])
    return puzzle_state == goal_state

def main():
    print('Welcome to tmarw001, bfair007, apalu003, and ssann003\'s 8 puzzle solver.')

    mode_selection = input('Type “1” to use a default puzzle, or “2” to enter your own puzzle.\n') # grab mode from user input
    mode_number = int(mode_selection) # cast mode selection to integer for comparison

    if mode_number == 1: # default puzzle setup
        puzzle = (['1', '2', '3'], ['4', '0', '6'], ['7', '5', '8'])
    elif mode_number == 2: # custom puzzle setup
        print('Enter your puzzle, use a zero to represent the blank.')
        row1 = input('Enter the first row, use space or tabs between numbers: ')
        row2 = input('Enter the second row, use space or tabs between numbers: ')
        row3 = input('Enter the third row, use space or tabs between numbers: ')
        print('\n')
        # setup rows from user input by splitting with space as delimitter
        row1 = row1.split()
        row2 = row2.split()
        row3 = row3.split()
        puzzle = row1, row2, row3 # concat input list into final puzzle
    algorithm_selection = input('Enter your choice of algorithm\n1. Uniform Cost Search\n2. A* with the Misplaced Tile heuristic.\n3. A* with the Euclidean distance heuristic.\n') # grab algo from user input
    algorithm_number = int(algorithm_selection) # cast mode selection to integer for comparison

    print(graph_search(puzzle, algorithm_number))


def node_expand(curr_node, traversed_states):  # take node and branch each direction based on location of the blank tile
    blank_tile_row, blank_tile_column = next(
        (i, j) for i in range(len(curr_node.puzzle)) for j in range(len(curr_node.puzzle)) if int(curr_node.puzzle[i][j]) == 0
    )

    moveset = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # every movement option for the blank tile
    for direction_row, direction_column in moveset:
        new_blank_tile_row, new_blank_tile_column = blank_tile_row + direction_row, blank_tile_column + direction_column
        if 0 <= new_blank_tile_row < len(curr_node.puzzle) and 0 <= new_blank_tile_column < len(curr_node.puzzle):  # if the movement is valid and keeps within the bounds of the puzzle
            # REASON FOR DEEPCOPY
            # each puzzle is a nested list that we need to make sure is maintained throughout states, hence why we ensure the outer and inner lists are both copied as well as attributes
            new_puzzle = copy.deepcopy(curr_node.puzzle)  # new puzzle copied from previous puzzle state
            # put blank tile into the proper spot of the new puzzle, post move
            new_puzzle[blank_tile_row][blank_tile_column], new_puzzle[new_blank_tile_row][new_blank_tile_column] = new_puzzle[new_blank_tile_row][new_blank_tile_column], new_puzzle[blank_tile_row][blank_tile_column]
            if new_puzzle not in traversed_states:  # avoid repeated states
                new_child = Node(new_puzzle)
                # EACH DIRECTION HAS DISTINCT STATE PRIORITY TO AVOID REPLACING A CHILD NODE ACCIDENTALLY
                if direction_row == -1 and direction_column == 0:
                    curr_node.child1 = new_child
                elif direction_row == 1 and direction_column == 0:
                    curr_node.child2 = new_child
                elif direction_row == 0 and direction_column == -1:
                    curr_node.child3 = new_child
                elif direction_row == 0 and direction_column == 1:
                    curr_node.child4 = new_child
                print('Generated new state:\n' + '\n'.join([' '.join(row).replace('0', 'b') for row in new_puzzle]) + '\n') # show new puzzle board replacing 0 with b for clarity

    return curr_node # new curr node with children

def custom_sort_key(node):
    return (node.depth + node.heuristic_cost, node.depth)

def graph_search(puzzle, algorithm_number):
    # traversal queue and visited states tracking
    queue = []
    visited_states = []
    # set node count and max to -1 (makes indexing easier as size = index)
    node_count = -1 
    max_queue_size = -1
    queue_size = 0

    # set heuristic value based on algo selection
    heuristic_value = 0 if algorithm_number == 1 else misplaced(puzzle) if algorithm_number == 2 else euclidean(puzzle)

    initial_node = Node(puzzle) # create initial puzzle state instance

    # set initial node attributes based on algo_selection
    initial_node.heuristic_cost = heuristic_value
    initial_node.depth = 0

    # add to queue and increment sizes
    queue.append(initial_node)
    visited_states.append(initial_node.puzzle)
    queue_size += 1
    max_queue_size += 1

    while True: # MAIN TRAVERSAL LOOP, KEEP GOING TILL ALL NODES EXPENDED OR GOAL FOUND
        
        if algorithm_number != 1: # if anything but uniform traversal, sort by depth + heuristic cost
            # sort key generates tuple of (totalcost, depth). sort priority is totalcost with node depth as tiebreaker
            queue.sort(key=custom_sort_key)

        if len(queue) == 0: # all nodes expended, no goal found, ABORT!
            return 'Failed to find goalstate'

        current_node = queue.pop(0) # grab queue top
        if not current_node.expanded: # if this node hasnt been expanded, then do so
            current_node.expanded = True
            node_count += 1
        queue_size -= 1

        if goal(current_node.puzzle):
            return ('Goal!!!\n\nTo solve this problem the search algorithm expanded a total of ' +
                    str(node_count) + ' nodes.\nThe maximum number of nodes in the queue at any one time: '
                    + str(max_queue_size) + '.\nThe depth of the goal node was ' + str(current_node.depth) + '.')

        if node_count != 0:
            print('The best state to expand with g(n) = ' + str(current_node.depth) + ' and h(n) = ' + str(current_node.heuristic_cost) + ' is…')
        else:
            print('\nExpanding state:')
        
        print('\n'.join([' '.join(row).replace('0', 'b') for row in current_node.puzzle]), '\n')

        expanded_node = node_expand(current_node, visited_states)

        for child_node in [expanded_node.child1, expanded_node.child2, expanded_node.child3, expanded_node.child4]: # for every child of the expanded node (run moveset tests)
            if child_node is not None: # for created children, add them with a depth +1 from the node they expanded from
                child_node.heuristic_cost = misplaced(child_node.puzzle) if algorithm_number == 2 else euclidean(child_node.puzzle)
                child_node.depth = current_node.depth + 1
                queue.append(child_node)
                visited_states.append(child_node.puzzle)
                queue_size += 1

        if queue_size > max_queue_size: # set queue max based on current size
            max_queue_size = queue_size


def euclidean(current_puzzle):
    goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    total_distance = 0  # accumulate distance

    for tile in range(1, 9):
        for row in range(len(current_puzzle)):
            for column in range(len(current_puzzle)):
                if int(current_puzzle[row][column]) == tile: # does the current tile match the iterated tile
                    current_row, current_column = row, column  # current tile pos
                    goal_row, goal_column = divmod(tile - 1, 3)  # goal tile pos
                    # divmod gives the quotient remainder as a tuple, which helps with finding where the curr tile is in the final puzzle
                    # ex: divmod(7-1, 3) is divmod(6,3) which is 2,0. this corresponds to row 2 column 0, hence the location of tile 7 that we want
                    total_distance += ((goal_row - current_row) ** 2 + (goal_column - current_column) ** 2) ** 0.5 # eucl distance formula using current tile pos and the position of the same tile in the goalstate

    return total_distance  # return total eucl distance

def misplaced(current_puzzle):
    goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    misplaced_tile_count = 0 # accumulate misplaced tiles

    for row in range(len(current_puzzle)):
        for column in range(len(current_puzzle)):
            if int(current_puzzle[row][column]) != goal_puzzle[row][column] and int(current_puzzle[row][column]) != 0: # if the current tile doesnt match our goal, and its not the blank tile
                misplaced_tile_count += 1  # increment count for misplaced tiles

    return misplaced_tile_count  # return the count of misplaced tiles

if __name__ == "__main__":
    main()
