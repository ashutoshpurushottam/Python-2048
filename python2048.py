import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def zero_to_right(line):

    """ Helper function for merge() that put all non-zero term
    to the left with no space. i.e. zero's to the right"""

    length = len(line)
    result = [0] * length
    idx = 0
    for num in line:
        if num != 0:
            result[idx] = num
            idx += 1

    return result



def next_occ(seq, idx):
    """find the index of next value that is the same and to the right of current index """

    if seq[idx + 1:].count(seq[idx]) > 0:
         new_idx = seq[idx + 1:].index(seq[idx])
         return new_idx + idx + 1

    else:
        return -9999


def check_gap(seq, idx1, idx2):
    """check if there are any non-zero entries in between idx1 and idx2"""


    for num in range(idx1 + 1, idx2):
        if seq[num] != 0:
            return True

    return False



def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """

    result_list = [0] * len(line)
    #keep track of indexes which are not to be merged
    merged = []

    for num in range(len(line)):
        second_occurence = next_occ(line, num)
        first_bool = not(check_gap(line, num, second_occurence))
        second_bool =  not(num in merged)
        #element will merge if it occurs again there are no non-zeros in between or
        #it was not created by merge itself
        if second_occurence != -9999 and first_bool and second_bool:

            result_list[second_occurence] = 2 * line[num]
            merged.append(second_occurence)
        elif second_bool:
            result_list[num] = line[num]


    return zero_to_right(result_list)

############################################################################

###### helper function for new_tile to choose a random zero tile ####

def choose(lst, height, width):
    """choose a random zero tile"""
    while True:
        row = random.randrange(height)
        col = random.randrange(width)
        if lst[row][col] == 0:
            return row, col

#####################################################################

################### helper functions for move ########################

def insert_row(seq, des_row, row):
    """
    insert a row to a given destination row number in the sequence that represent the grid
    return the new modified grid representation
    """
    seq[des_row] = row
    return seq

def insert_col(seq, des_col, col):
    """
    insert a column to a given destination column number in the sequence that represent the grid
    return the new modified grid representation
    """

    num = 0

    for row in seq:
        row[des_col] = col[num]
        num += 1

    return seq

def init_tiles(seq, direction):
    """
    return a list of indices of tiles whose value will be first passed into the merged function
    with respect to the direction chosen.
    """
    row = len(seq)
    col = len(seq[0])
    dir_dict = {UP: [[0, i] for i in range(col)],
             DOWN: [[row - 1, i] for i in range(col)],
             LEFT:[[i, 0] for i in range(row)],
             RIGHT:[[i, col - 1] for i in range(row)]}
    return dir_dict[direction]


def lines_for_insert(seq, direction):
    """
    to determine all the lines of values that are to be inserted into the grid
    """
    #this is a list of list that contains list of lines
    lines = []
    initial = init_tiles(seq, direction)
    offsets = OFFSETS[direction]

    if direction == UP or direction == DOWN:
        line_len = len(seq)
    elif direction == LEFT or direction == RIGHT:
        line_len = len(seq[0])

    for tile in initial:
        #this is a list of value of one single individual line
        line = []
        for num in range(line_len):
            row = tile[0] + num* offsets[0]
            col = tile[1] + num* offsets[1]
            line.append(seq[row][col])

        lines.append(line)

    return lines


def apply_move(seq, direction):
    """
    this helper function will exercute the move method in place of the class below
    """
    grid = seq[:]
    idx = 0
    lines = lines_for_insert(grid, direction)
    for line in lines:
        if direction == UP:
            insert_col(grid, idx, merge(line))

        elif direction == DOWN:
            insert_col(grid, idx, merge(line)[::-1])

        elif direction == LEFT:
            insert_row(grid, idx, merge(line))

        elif direction == RIGHT:
            insert_row(grid, idx, merge(line)[::-1])

        idx += 1

    return grid





class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        initializing grid board
        """
        self._height = grid_height
        self._width = grid_width

        self._board_config = [[0] * self._width] * self._height


        self.init_tile = {UP:[(0, i) for i in range(self._width)],
                          DOWN:[(self._height - 1, i) for i in range(self._width)],
                          LEFT:[(i, 0) for i in range(self._height)],
                          RIGHT:[(i, self._width - 1) for i in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self._board_config = [[0] * self._width] * self._height

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board_config)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        #state of game before a move
        before_move = [row[:] for row in self._board_config]
        #apply a move
        self._board_config = apply_move(self._board_config, direction)
        #state of game after a move
        after_move = [row[:] for row in self._board_config]
        #check if before and after differ, if yes, generate a new tile
        if before_move != after_move:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zero_tile = choose(self._board_config, self.get_grid_height(), self.get_grid_width())
        possible_tile = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        val = random.choice(possible_tile)
        row = zero_tile[0]
        col = zero_tile[1]
        self.set_tile (row, col, val)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # make a copy of the corresponding row
        chosen_row = self._board_config[row][:]
        #mutate the corresponding col in that copied row
        chosen_row[col] = value
        #set the original row to be the mutated row
        self._board_config[row] = chosen_row



    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board_config[row][col]


    def count_zero_tile(self):
        """
        Return count of zero tiles in the grid
        """
        total = 0
        for row in self._board_config:
            for val in row:
                if val == 0:
                    total += 1
        return total



poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
