"""
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote
 its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them
  - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist
of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from
the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and
ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example,
consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others,
does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric
 are within two or more claims?


Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any
other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.
"""

from PIL import Image

from utils import ProblemSolver


class Claim(object):
    def __init__(self, idNumber, x, y, w, h):
        self.id = idNumber
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def area(self):
        return self.w * self.h

    def __str__(self):
        return '#{} @ {},{}: {}x{}'.format(self.id, self.x, self.y, self.w, self.h)


class Day03Solver(ProblemSolver):
    def __init__(self):
        super(Day03Solver, self).__init__(3)

        self.testDataPartOne = {'#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2': 4}
        self.testDataPartTwo = {'#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2': 3}

        self.image = None

    def ProcessInput(self, data=None):
        """

        :param data:
        :return:
        """
        if not data:
            data = self.rawData

        processed = []

        for claim in data.split('\n'):
            idNum = int(claim.split(' @ ')[0].replace('#',''))
            coords, size = claim.split(' @ ')[-1].split(': ')
            x, y = [int(i) for i in coords.split(',')]
            w, h = [int(i) for i in size.split('x')]

            processed.append(Claim(idNum, x, y, w, h))

        return processed

    def SolvePartOne(self, data=None):
        """
        loops over the claim data, and adds a value of 1 to each pixel in the claim
        returns the number of pixels whose value is greater than 1

        :param data:
        :return:
        """
        if not data:
            data = self.processed

        image = Image.new('L', (1000, 1000))

        for claim in data:
            for w in range(claim.w):
                for h in range(claim.h):
                    x, y = w + claim.x, h + claim.y
                    currentValue = image.getpixel((x, y))
                    currentValue += 1
                    image.putpixel((x, y), currentValue)

        counter = 0

        for x in range(image.width):
            for y in range(image.height):
                val = image.getpixel((x, y))
                if val > 1:
                    counter += 1

        self.image = image

        return counter

    def CheckIfClaimIsClean(self, image, claim):
        """
        Loop over all the pixels in the claim and return False if any value in the claim > 1
        """
        print(claim)
        for x in range(claim.x, claim.w + claim.y):
            for y in range(claim.y, claim.h + claim.y):
                if image.getpixel((x, y)) > 1:
                    return False

        return True

    def SolvePartTwo(self, data=None):
        """

        :param data:
        :return:
        """
        if not data:
            data = self.processed

        # make sure we have an image to operate on
        if not self.image:
            self.SolvePartOne(data=data)

        # use the solver in part 1, that stores off an image of pixels, and get it out of part one
        image = self.image

        for claim in data:
            if self.CheckIfClaimIsClean(image, claim):
                return claim.id


if __name__ == '__main__':
    day03 = Day03Solver()
    day03.Run()
