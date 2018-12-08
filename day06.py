"""
"""

from PIL import Image
from PIL import ImageColor

from random import randint
import math

import itertools
import collections

from utils import ProblemSolver


def sign(p1, p2, p3):
    return ((p1[0] - p3[0]) * (p2[1] - p3[1])) - ((p2[0] - p3[0]) * (p1[1] - p3[1]))


def pointInTriangle(pt, t1, t2, t3):
    d1 = sign(pt, t1, t2)
    d2 = sign(pt, t2, t3)
    d3 = sign(pt, t3, t1)

    hasNeg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    hasPos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (hasNeg and hasPos)


class TimeCoordinates(object):
    def __init__(self, image, coordinates):
        self.coordinates = {coord: (randint(0, 255), randint(0, 255), randint(0, 255)) for coord in coordinates}
        self.image = image

    def voroni(self):
        """
        Assigns a unique color to each coordinate, and determines which coordinates in the map are manhattan-close
        to which point, then
        :return:
        """
        for x in range(self.image.width):
            for y in range(self.image.height):
                distances = {}
                for coord in self.coordinates:
                    distances[coord] = abs((x - coord[0]) + (y - coord[1]))

                maxV = max(distances.values())

                # if there's only one categorically closer
                if list(distances.values()).count(maxV) == 1:
                    inverted = {v: k for k, v in distances.items()}
                    closestCoord = inverted[maxV]
                    self.image.putpixel((x, y), self.coordinates[closestCoord])


class Day06Solver(ProblemSolver):
    """
    Solver for day 6
    """
    def __init__(self):
        super(Day06Solver, self).__init__(6)

        self.testDataPartOne = {'1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9': 17}

    def ProcessInput(self, data=None):
        """
        Map our input letters to positive or negative numbers and return them out in a list
        :param data:
        :return: a time coordinates object with an image and the used coordinate for voronication
        """
        if not data:
            data = self.rawData

        points = []
        xBounds = []
        yBounds = []
        # determine size based on bounding box of the available points
        for coord in data.split('\n'):
            x, y = coord.split(', ')
            xBounds.append(int(x))
            yBounds.append(int(y))
            points.append((int(x), int(y)))

        xSize = max(xBounds)
        ySize = max(yBounds)

        print(xSize, ySize)

        image = Image.new('RGB', (xSize, ySize))

        processed = TimeCoordinates(image, points)

        return processed

    def SolvePartOne(self, data=None):
        """
        Triangulate the available points to determine which points are "bounded"
        Then figure out closest point for each point in the triangluated areas

        """
        if not data:
            data = self.processed

        data.voroni()

        # get all the possible triangle combinations
        triangles = list(itertools.combinations(data.coordinates.keys(), 3))

        areas = collections.defaultdict(int)

        # loop over all our points
        for x in range(data.image.width):
            for y in range(data.image.height):
                # figure out if the point is in any of our triangles
                inTriangle = False
                for t1, t2, t3 in triangles:
                    point = (x, y)

                    if point == t1 or point == t2 or point == t3:
                        inTriangle = True
                        break

                    if pointInTriangle(point, t1, t2, t3):
                        inTriangle = True
                        break

                if inTriangle:
                    print(point)
                    color = data.image.getpixel(point)
                    areas[color] += 1

        # we're getting bad data here
        for area in areas:
            print(areas[area])


if __name__ == '__main__':
    day06 = Day06Solver()
    processed = day06.ProcessInput(list(day06.testDataPartOne.keys())[0])
    day06.SolvePartOne(data=processed)
