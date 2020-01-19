"""
AdventOfCode2018 day09
--- Day 9: Marble Mania ---
You talk to the Elves while you wait for your navigation system to initialize. To pass the time, they introduce you to their favorite marble game.

The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules. The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble, it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself. This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that there is one marble between the marble that was just placed and the current marble.) The marble that was just placed then becomes the current marble.

However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens. First, the current player keeps the marble they would have placed, adding it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score. The marble located immediately clockwise of the marble that was removed becomes the new current marble.

For example, suppose there are 9 players. After the marble with value 0 is placed in the middle, each player (shown in square brackets) takes a turn. The result of each of those turns would produce circles of marbles like this, where clockwise is to the right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3
[5]  0  4  2 (5) 1  3
[6]  0  4  2  5  1 (6) 3
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7
[9]  0  8  4 (9) 2  5  1  6  3  7
[1]  0  8  4  9  2(10) 5  1  6  3  7
[2]  0  8  4  9  2 10  5(11) 1  6  3  7
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15
[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15
The goal is to be the player with the highest score after the last marble is used up. Assuming the example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept marble 23 and removed marble 9, while no other player got any points in this very short example game).

Here are a few more examples:

10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
What is the winning Elf's score?
"""

from utils import ProblemSolver

class CircularList(list):
    """
    A list object that slices and sets items at the index % len(self) index, so you can wrap around
    the list without having to clamp your pointer
    """
    def __init__(self, *args):
        super(CircularList, self).__init__(*args)

    def __getitem__(self, index):
        if isinstance(index, int):
            index = index % len(self)
        elif isinstance(index, slice):
            # make sure these wrap around correctly
            start = index.start % len(self)
            stop = index.stop % len(self)

            # if they cross over the end of the list, keep going
            if stop <= start:
                return super(CircularList, self).__getitem__(
                    slice(start, len(self))) + \
                       super(CircularList, self).__getitem__(slice(0, stop))

            # otherwise, slice it normally
            return super(CircularList, self).__getitem__(slice(start, stop))

        return super(CircularList, self).__getitem__(index)

    def __setitem__(self, key, value):
        super(CircularList, self).__setitem__(key % len(self), value)

    def insert(self, index, _T):
        """

        :param index: unbound index to insert to
        :param _T: object to insert at index % len position
        """
        super(CircularList, self).insert(index % len(self), _T)

    def pop(self, index):
        """

        :param index: index % len to pop from
        :return: the item popped
        """
        return super(CircularList, self).pop(index % len(self))


class Marble(object):
    """
    Represents a marble, and contains the marble's position, value, and status
    """
    def __init__(self, name):
        self.id = name
        self.placed = False

    def hasRules(self):
        """

        :return: True, if the current marble has weird rules
        """
        return self.id % 23 == 0

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Player(object):
    """
    Object representing a player, which contains its current score, and a list of the marbles the player has
    """
    def __init__(self, name):
        self.id = name
        self.score = 0
        self.marbles = []


class MarbleGameState(object):
    """
    Object representing the state of our marble game
    """
    def __init__(self, marbleCount, playerCount):
        self.marbleCount = marbleCount
        self.marbles = [Marble(i) for i in range(self.marbleCount)]

        # put the first two marbles on the field, because that makes things easy
        self.marbles[0].placed = True
        self.marbles[1].placed = True
        self.playfield = CircularList([self.marbles[0], self.marbles[1]])
        self.playerCount = playerCount
        self.players = CircularList(Player(i) for i in range(self.playerCount))
        self.currentPlayer = 1
        self.currentMarble = 1
        self.turn = 0

    def update(self):
        """
        Performs a turn for the current game. Returns False if the game is over
        :return:
        """
        availableMarbles = [marble for marble in self.marbles if not marble.placed]

        # if there are no available marbles, bail out
        if not availableMarbles:
            return False

        nextMarble = availableMarbles[0]
        nextMarble.placed = True  # mark it as placed automatically, since that's true in both cases

        if nextMarble.hasRules():
            # grab the marble 7 to the left of the current marble
            otherMarble = self.playfield.pop(self.currentMarble - 7)

            print('Marble ', nextMarble, 'is popping ', otherMarble)

            # add that marble's value and the value of the ruled marble
            self.players[self.currentPlayer].score += nextMarble.id + otherMarble.id

            # the current marble is now the marble clockwise of the marble we removed
            self.currentMarble -= 6
        else:
            nextLoc = self.currentMarble + 1

            # when inserting a marble, we need to check if we're trying to insert to index 0
            # and instead append
            # if nextLoc % len(self.playfield) == 0:
            #     self.playfield.append(nextMarble)
            # else:
            self.playfield.insert(nextLoc, nextMarble)

            self.currentMarble = nextLoc

        self.currentPlayer += 1
        self.turn += 1

        return True

    def getWinningScore(self):
        """
        :return: the max score found in all the players
        """
        return max([player.score for player in self.players])

    def __str__(self):
        outString = ''
        for i in self.playfield:
            outString += ' '
            current = self.playfield[self.currentMarble]
            if i == current:
                outString += '(' + str(i) + ')'
            else:
                outString += str(i)
        return outString


class day09Solver(ProblemSolver):
    """
    AdventOfCode2018 day09
    """
    def __init__(self):
        super(day09Solver, self).__init__(9)

        self.testDataPartOne = {'10 players; last marble is worth 1618 points': 8317,
                                '13 players; last marble is worth 7999 points': 146373,
                                '17 players; last marble is worth 1104 points': 2764,
                                '21 players; last marble is worth 6111 points': 54718,
                                '30 players; last marble is worth 5807 points': 37305
                                }
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        
        :param data:
        :returns: processed data for today's challenge
        """
        if not data:
            data = self.rawData


        tokens = data.split()
        players = int(tokens[0])
        marbleCount = int(tokens[-2])

        return MarbleGameState(marbleCount, players)

    def SolvePartOne(self, data=None):
        """
        
        :param data: MarbleGameState that you want to solve
        :returns: The winning score for the given game state
        """
        if not data:
            data = self.processed

        turnLimit = 15

        while data.update() and turnLimit > data.turn:
            pass
            print(data.currentMarble, data)


        print(data)

        raise Exception("Bonk")

        return data.getWinningScore()

    def SolvePartTwo(self, data=None):
        """
        
        :param data:
        :returns: The solution to part two of today's challenge
        """
        if not data:
            data = self.processed


if __name__ == '__main__':
    day09 = day09Solver()
    day09.Run()
        

