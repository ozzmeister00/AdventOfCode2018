"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

Your puzzle answer was 4290.

--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?

Your puzzle answer was 37318.
"""

from PIL import Image
from PIL import ImageColor

from random import randint
import math

import itertools
import collections

from utils import ProblemSolver, getBarycentric


class TimeCoordinates(object):
    """
    Data for day6, a list of input coordinates mapped to random colors, and an image
    that can fit all the input points
    """
    def __init__(self, image, coordinates, regionDistance):
        self.coordinates = {coord: (randint(1, 255), randint(1, 255), randint(1, 255)) for coord in coordinates}
        self.image = image
        self.pointsInRegion = 0
        self.regionDistance = regionDistance

        for coord in self.coordinates:
            #print('initializing coord', coord, 'to ', self.coordinates[coord])
            self.image.putpixel(coord, self.coordinates[coord])

    def voroni(self):
        """
        Assigns a unique color to each coordinate, and determines which coordinates in the map are manhattan-close
        to which point, then
        :return:
        """
        self.pointsInRegion = 0

        for x in range(self.image.width):
            for y in range(self.image.height):
                # store off the distance to each coordinate
                distances = {}
                for coord in self.coordinates:
                    distances[coord] = abs(x - coord[0]) + abs(y - coord[1])

                # get the minimum and total distances
                minV = min(distances.values())
                totalDistance = sum(distances.values())

                # if the distance is within our region distance, increment this value
                if totalDistance < self.regionDistance:
                    self.pointsInRegion += 1

                # skip the distance checking if we're already a coordinate
                if (x, y) in self.coordinates:
                    continue

                # if there's only one categorically closer
                if list(distances.values()).count(minV) == 1:
                    inverted = {v: k for k, v in distances.items()}
                    closestCoord = inverted[minV]
                    self.image.putpixel((x, y), self.coordinates[closestCoord])


class Day06Solver(ProblemSolver):
    """
    Solver for day 6
    """
    def __init__(self):
        super(Day06Solver, self).__init__(6)

        self.testDataPartOne = {'1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9': 17}
        self.testDataPartTwo = {'1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9': 16}

    def ProcessInput(self, data=None):
        """
        Grab the coordinate data from our input string

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

        xSize = max(xBounds) + 1
        ySize = max(yBounds) + 1

        print(xSize, ySize)

        image = Image.new('RGB', (xSize, ySize))

        # detect if we're parsing test data or our own
        regionDistance = 32
        if len(points) > 10:
            regionDistance = 10000

        processed = TimeCoordinates(image, points, regionDistance)

        return processed

    def SolvePartOneTriangulate(self, data=None):
        """
        Voroni our test data, and to detect if a region is finite or infinite by seeing if the test point
        is within any of the triangles created by our points

        NOTE! This method doesn't actually work, since the points in our data can be outside of the convex hull
        of all our coordinates.
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

                    # break out of this loop if we're at the tip of a triangle
                    if point == t1 or point == t2 or point == t3:
                        inTriangle = True
                        break

                    # this algorithm may not be sufficiently generous
                    # getbarycentric at least gives you the raw data, and maybe it needs a "near enough inside triangle"
                    u, v, w = getBarycentric(point, t1, t2, t3)
                    hasNeg = u < 0 or v < 0 or w < 0
                    hasPos = u > 0 or u > 0 or w > 0
                    if not (hasNeg and hasPos):
                        inTriangle = True
                        break

                if inTriangle:
                    color = data.image.getpixel(point)
                    areas[color] += 1
                else:
                    data.image.putpixel((x,y), (255,255,255))

        for area in areas:
            print(areas[area], area)

        data.image.save('test1.tga')

    def SolvePartOne(self, data=None):
        """
        voronize our image, and loop over all our regions, discarding regions that touch the edge of the grid

        return the area of the largest, finite region
        """
        if not data:
            data = self.processed

        data.voroni()

        areas = collections.defaultdict(int)

        infiniteColors = collections.defaultdict(int)

        for x in range(data.image.width):
            for y in range(data.image.height):
                point = (x, y)

                color = data.image.getpixel(point)

                # if any of the regions are on the border of the image, their fields extend into infinity
                # so we can automatically discount them in later processing
                if x == 0 or x == data.image.width - 1 or y == 0 or y == data.image.height - 1:
                    infiniteColors[color] += 1

                areas[color] += 1

        finiteAreas = [areas[color] for color in areas if color not in infiniteColors]

        return max(finiteAreas)

    def SolvePartTwo(self, data=None):
        """
        Find the region that is within a certain distance of all the points in the system
        Since we get this information basically for free during the voroni calculation

        :return: the number of points within our safe region distance
        """
        if not data:
            data = self.processed

        data.voroni()

        return data.pointsInRegion


if __name__ == '__main__':
    day06 = Day06Solver()
    day06.Run()
