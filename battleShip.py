'''
    Project Name: battleship.py
    Name: Zixi Zhong
    Purpose: This program reads in two files to play the game. The program reads the first file for ship placements
    and places the ships on the battleship boards accordingly. Then it reads in a guesses file and responds to the ships
    on the board based on its effects.
'''

import sys


class GridPos:
    '''
        This class represents a grid position in the board.
        Parameters: self
                    position - grid coordinates
        Returns: none, sets value to self._position, self._occupied
                 and self._guessed
        Pre-condition: Board must be initialized to assign a grid
                       position object to that position
        Post-condition: this class will initialize 3 values to be
                        updated later
    '''
    def __init__(self, position):
        self._position = position
        self._occupied = None
        self._guessed = False


    def set_occupied(self, ship):
        '''
            This method sets the ship object to self._occupied.
            Parameters: self, ship object
            Returns: none
        '''
        self._occupied = ship


    def get_occupied(self):
        '''
            This method returns whether or not a ship occupies
            that gridpos object.
            Parameters: self
            Returns: self._occupied
        '''
        return self._occupied


    def set_guessed(self):
        '''
            This method sets self._guessed to True, as in that
            grid position has been guessed.
            Parameters: self
            Returns: none
        '''
        self._guessed = True


    def get_guessed(self):
        '''
            This method returns self._guessed.
            Parameters: self
            Returns: self._guessed
        '''
        return self._guessed


    def __str__(self):
        '''
            This method formats the GridPosition object to be
            easily printed.
            Parameters: self
            Returns: printable format for GridPosition
        '''
        return "{} : {}".format(self._position, self._occupied)



class Board:
    '''
        This class represents a grid as a battleship board.
        Parameters: self
        Returns: none, sets value to self._grid, and self._ships
        Pre-condition: Board is initialized with all None
                       GridPosition objects
        Post-condition: this class will initialize 2 values to be
                        updated later
    '''
    def __init__(self):
        grid = []

        # Makes a 10 X 10 grid to match the battleship standards
        for i in range(10):
            inner = []
            for j in range(10):
                coor = (i, j)  # Coordinates
                position = GridPos(coor)
                inner.append(position)
            grid.append(inner)

        self._grid = grid
        self._ships = {}


    def add_ship(self, name, ship, line):
        '''
            This method adds a ship onject to the ships
            dictionary.
            Parameters: self
                        name - name of ship
                        ship - ship object
                        line - line where ship is placed
            Returns: none, updates self._ships
            Pre-condition: ship objects must be initialized to
                           be added to the dictionary
            Post-condition: the ships dictionary will contain all
                            ships only once
        '''
        self._ships[name] = ship

        positions = ship.get_positions()

        for coors in positions:
            x = coors[0] # Coordinates of ship at a specific
            y = coors[1] # grid position
            grid_position = self._grid[x][y]

            if grid_position.get_occupied() == None: # Checks if ships
                grid_position.set_occupied(ship)     # overlap

            else:
                print("ERROR: overlapping ship: " + line)
                sys.exit()


    def get_grid(self):
        '''
            This method returns self._grid.
            Parameters: self
            Returns: self._grid
        '''
        return self._grid


    def get_ships(self):
        '''
            This method returns self._ships.
            Parameters: self
            Returns: self._ships
        '''
        return self._ships


    def __str__(self):
        '''
            This method formats the board object to be
            easily printed.
            Parameters: self
            Returns: printable format for Board
        '''
        return str(self._grid)



class Ship:
    '''
        This class represents a ship object.
        Parameters: self
                    name - name os ship
                    size - size of ship
                    positions - list of coordinate tuples
                    hits_left - how many hits the ship has left before
                                sinking
        Returns: none, sets value to self._name, and self._size,
                 self._positions, and self._hits
        Pre-condition: Ship object is initialized with all the information
                       in the file
        Post-condition: this class will make 5 ship objects
    '''
    def __init__(self, name, size, positions, hits_left):
        self._name = name
        self._size = size
        self._positions = positions
        self._hits = hits_left


    def get_name(self):
        '''
            This method returns self._name.
            Parameters: self
            Returns: self._name
        '''
        return self._name


    def get_positions(self):
        '''
            This method returns self._positions.
            Parameters: self
            Returns: self._positions
        '''
        return self._positions


    def update_hits(self):
        '''
            This method updates the hits a ship has left before sinking.
            Parameters: self
            Returns: none, subtracts 1 from the self._hits
        '''
        self._hits -= 1


    def get_hits(self):
        '''
            This method returns self._hits.
            Parameters: self
            Returns: self._hits
        '''
        return self._hits


    def __str__(self):
        '''
            This method formats the ship object to be
            easily printed.
            Parameters: self
            Returns: printable format for Ship
        '''
        return str(self._name)



def read_file():
    '''
        This function reads in files, checks if they can be read,
        sends them back if so, and quits and informs the user if not.
        Parameters: none
        Returns: read in file
        Pre-condition: A file must be sent in
        Post-condition: file is read in and sent back
    '''
    file = input()

    try:
        file = open(file)
    except:  # Checks if the file can be opened
        print("ERROR: Could not open file: " + file)
        sys.exit()
    return file



def read_player1(file, board):
    '''
        This function accepts a file the player 1 placements and makes
        sure all the placements and ships are legal. If so, it initializes
        a ship object for every line and adds it to the Board object
        collection of ships. Initializes a ship counter to count how
        many ships remain in the game.
        Parameters: file, Board object
        Returns: ship_counter
        Pre-condition: player 1 placements must be read in first
        Post-condition: the board object is filled with updated GridPos
                        objects, who contain ship objects
    '''
    # Dict of legal ships and their sizes
    proper_ships = {"A": 5, "B": 4, "S": 3, "D": 3, "P": 2}

    for placement in file: #
        line = placement.split()

        name = line[0]
        x1 = int(line[1])
        y1 = int(line[2])
        x2 = int(line[3])
        y2 = int(line[4])

        # Checks that the ship is within the grid bounds
        if ((x1 >= 0 and x1 <= 9) and (y1 >= 0 and y1 <= 9)
            and (x2 >= 0 and x2 <= 9) and (y2 >= 0 and y2 <= 9)):

            positions = []  # list of positions occupied by the ship
            if x1 == x2: # Checks that ship is vertical
                start = min(y1, y2)
                end = max(y1, y2)
                orientation = "vertical"

            elif y1 == y2: # Checks that ship is horizontal
                start = min(x1, x2)
                end = max(x1, x2)
                orientation = "horizontal"

            else: # Tells user and quits if  ship isn't vert. or horiz.
                print("ERROR: ship not horizontal or vertical: " + placement)
                sys.exit()


            size = abs(start - end) + 1
            if size != proper_ships[name]:
                print("ERROR: incorrect ship size: " + placement)
                sys.exit()


            # Sets coordinates to positions list depending on if
            # the ship is vertical or horizontal
            for i in range(start, end + 1):
                if orientation == "vertical":
                    coor = (x1, i)
                else:
                    coor = (i, y1)
                positions.append(coor)

            hits_left = size

            # Quits if ship is out of bounds
            if name in board.get_ships():
                print("ERROR: fleet composition incorrect")
                sys.exit()
            else:  # initializes ship object and adds to board if not
                ship = Ship(name, size, positions, hits_left)
                board.add_ship(name, ship, placement)


        else:  # Quits if ship is out of bounds
            print("ERROR: ship out-of-bounds: " + placement)
            sys.exit()


    if len(board.get_ships()) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit()

    # Sets ship_counter to the size of the ship collection in board
    ship_counter = len(board.get_ships())
    return ship_counter



def read_player2(file, board, ship_counter):
    '''
        This function accepts the file of player 2 guesses and affects the
        ships in the board object accordingly. Program terminates either
        when there are no more guesses left or all ships have been sunken.
        Parameters: file, Board object, ship_counter
        Returns: none, plays and finishes the game
        Pre-condition: player 1 placements must be read in first, and all
                       objects must be initialized
        Post-condition: the program will play the game out and end it
    '''
    for guess in file:
        guess = guess.split()

        x = int(guess[0])
        y = int(guess[1])

        # Checks that guesses are legal
        if (x >= 0 and x <= 9) and (y >= 0 and y <= 9):
            pos = board.get_grid()[x][y]  # GridPos object at [x][y]
            ship = pos.get_occupied()  # Ship/None object in Grid Pos
            guessed = pos.get_guessed()  # Whether or not the position
                                         # has been guessed before
            # Checks is a ship is in that position
            if ship == None:
                if guessed == False: # Checks if the position has been
                    print("miss")    # guessed before
                    pos.set_guessed() # Sets guessed to True
                else:  # Has been guessed before and missed
                    print("miss (again)")

            else: # Ship is in that position
                num_hits = ship.get_hits() # Hits left for that ship

                # Position has not been guessed before and there are more
                # than 1 positions that havent been hit on the ship
                if guessed == False and num_hits > 1:
                    print("hit")
                    ship.update_hits()
                    pos.set_guessed()

                # Position has not been guessed before and there is only
                # one position on the ship that hasn't been hit
                elif guessed == False and num_hits <= 1:
                    print("{} sunk".format(ship.get_name()))
                    ship_counter -= 1
                    pos.set_guessed()

                else:
                    print("hit (again)")

        else: # Guess was not legal
            print("illegal guess")

        if ship_counter <= 0: # Checks if all the ships have been sunk
            print("all ships sunk: game over")
            sys.exit()



def main():
    '''
        This function initializes a board object, reads in a player1
        file, processes the file into player1 moves, reads in a
        player 2 file, and affects the player1 ships accordingly.
        Parameters: None
        Returns: None
        Pre-condition: none
        Post-condition: files will be processed and the game will end.
    '''
    board = Board()

    p1_file = read_file()
    ship_counter = read_player1(p1_file, board)  # Reads placements

    p2_file = read_file()
    read_player2(p2_file, board, ship_counter)  # Reads guesses



main()