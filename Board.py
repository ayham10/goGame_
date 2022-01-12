import numpy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Color = (205, 92, 92)

class Stone(object):
    def __init__(self, board, point, color):
        """Create and initialize a stone.

        Arguments:
        board -- the board which the stone resides on
        point -- location of the stone as a tuple, e.g. (3, 3)
                 represents the upper left hoshi
        color -- color of the stone

        """
        self.board = board
        self.point = point
        self.color = color

    def remove(self):
        print("removeeeee999")
        """Remove the entire Stone."""

        del self



class Board(object):
    def __init__(self):
        """Create and initialize an empty board."""
        self.groups = []
        self.next = BLACK
        self.black=0
        self.white=0
        self.ToatalRounds = 0

        self.CapturedWite=0
        self.CapturedBlack = 0

        self.whiteEaten = 0
        self.blackEaten = 0

        self.mat = numpy.zeros((21, 21), dtype=int)

    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

    def AddBlack(self):
       self.black+= 1
    def AddWhite(self):
        self.white+= 1
    def AddRound(self):
        # print("added round")
        self.ToatalRounds+=1
    def search(self, point=None, points=[]):
        """Search the board for a stone.
        The board is searched in a linear fashion, looking for either a
        stone in a single point (which the method will immediately
        return if found) or all stones within a group of points.

        Arguments:
        point -- a single point (tuple) to look for
        points -- a list of points to be searched
        """
        stones = []
        for group in self.groups:
            for stone in group.stones:
                # print("sssss")
                if stone.point == point and not points:
                    return stone
                if stone.point in points:
                    stones.append(stone)
        return stones

    def isblocked(self,indexes,turn):
        "A function for understanding if there is a free space for some of the stones inside the cluster"
        # print("the indexes are ->",indexes)
        for point in indexes:
            #for a,b in [(point[0] + 1, point[1]), (point[0] - 1, point[1]), (point[0], point[1] + 1), (point[0], point[1] - 1)]:
            for a, b in [(point[0] + 1, point[1]), (point[0] - 1, point[1]), (point[0], point[1] + 1),(point[0], point[1] - 1)]:
                # print("check neigbor ->",a,b,self.mat[a,b])
                if self.mat[a,b] == 1:
                    print("blocking neighbors are ",a,b)
                if self.mat[a,b] == 0:
                    print("Stone " + str(point[0]) + " " + str(point[1]) + " is not blocked the cluster is free !!")
                    return False

        return True

    def neighbors(self,x,y,turn):
        neighboring =[(x,y)]
        # print("points are",(x,y),self.mat[x,y])
        for point in neighboring:
            for a,b in [(point[0]+1,point[1]),(point[0]-1,point[1]),(point[0],point[1]+1),(point[0],point[1]-1)]:
                #print("a,b are->",(a,b),self.mat[a,b])
                if self.mat[a,b]==turn and (a,b) not in neighboring:
                    neighboring.append((a,b))
                    #print("add-->", (a,b))

        #print(neighboring)
        if Board.isblocked(self,neighboring,turn) == True:
            print("Trueee")
            return neighboring

    def setmatrix(self, x, y):
            """Creating a function for insterting where a stone has been set on the board , 1 = black , 2 = white """
            # print("Function got : x = " + str(x) + " y = " + str(y))

            # Checking if there is a stone allready in this position
            if self.mat[x, y] == 1 | self.mat[x, y] == 2:
                # print("A stone is allready set in this place !!")
                return 0
            if self.mat[x, y] == -1:
                 print(" This zone has been eaten cannot place a stone there  !!")

            # If a white stone has been set
            if self.next == WHITE:
                self.mat[x, y] = 2

            # If a black stone has been set
            if self.next == BLACK:
                self.mat[x, y] = 1

        # def squarecheck(self,i,j):

    def capturestone(self):
            """Creating a function for eating a stone if needed , returns an index for what stones need to be eaten"""
            indexes = []

            # Asking what stone has been played
            if self.next == BLACK:
                color = 2
                opposite = 1
            else:
                color = 1
                opposite = 2

            # print("Color " + str(color))
            # print("Opposite " + str(opposite))

            # A special case for the edges of the map
            if ((self.mat[1, 1] == color) and (self.mat[1, 2] == opposite) and (self.mat[2, 1] == opposite) and (
                    self.mat[2, 2] == opposite)):
                indexes.append((1, 1))
                self.mat[1, 1] = -1

            if ((self.mat[1, 19] == color) and (self.mat[1, 18] == opposite) and (self.mat[2, 18] == opposite) and (
                    self.mat[2, 19] == opposite)):
                indexes.append((1, 19))
                self.mat[1, 19] = -1

            if ((self.mat[19, 1] == color) and (self.mat[18, 1] == opposite) and (self.mat[18, 2] == opposite) and (
                    self.mat[19, 2] == opposite)):
                indexes.append((19, 1))
                self.mat[19, 1] = -1

            if ((self.mat[19, 19] == color) and (self.mat[19, 18] == opposite) and (self.mat[18, 19] == 2) and (
                    self.mat[18, 18] == opposite)):
                indexes.append((19, 19))
                self.mat[19, 19] = -1

                # Checking for all of the board if there are stones to remove not in the edges
            for i in range(1, 17):
                for j in range(2, 18):

                    # Checking for an X shape in the matrix
                    if (self.mat[i + 1, j] == color) and (self.mat[i, j] == opposite) and (
                            self.mat[i + 1, j - 1] == opposite) and (self.mat[i + 1, j + 1] == opposite) and (
                            self.mat[i+2, j] == opposite):
                        self.mat[i + 1, j] = -1
                        indexes.append((i + 1, j))

                    # Checking a square of 4 X 4 in the matrix
            return indexes


