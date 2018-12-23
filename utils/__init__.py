"""
Utility functions commonly used in solving the Advent of Code
"""

import functools
import operator
import os

INPUTS_FOLDER_NAME = "inputData"


def product(iterable):
    """
    Returns the product of an iterable of numbers
    :param iterable: eg [1, 2, 3, 4, 5]
    :return: the product of all items in the literal multiplied together
    """
    return functools.reduce(operator.mul, iterable, 1)



def getInputsFolder():
    """

    :return: the absolute path on the file system to the inputData folder, which should be relative to this package
    """
    # figure out where we are
    utilsFolder = os.path.dirname(os.path.abspath(__file__))

    # go up one folder
    sourceFolder = os.path.split(utilsFolder)[0]

    return os.path.join(sourceFolder, INPUTS_FOLDER_NAME)


class ProblemSolver(object):
    """
    Common class for loading and processing data from each day's challenge
    """
    def __init__(self, day):
        """
        Finds the input data file for this day, and loads the raw contents of that file into
        the rawData property of the instance
        :param day: the number day for this data
        """
        self.day = day
        self.fileName = 'day{}.txt'.format(str(day).zfill(2))
        self.filePath = os.path.join(getInputsFolder(), self.fileName)

        # load in the file's data
        with open(self.filePath, 'r') as fh:
            self.rawData = fh.read()

        # leave this open for later access by process input
        self.processed = None
        self.partOneResult = None
        self.partTwoResult = None

        self.testDataPartOne = {}
        self.testDataPartTwo = {}

    def ProcessInput(self, data=None):
        """
        To be implemented by each day's class to process data into a helpful format
        for later handling

        returns: Processed Input
        """
        raise NotImplementedError()

    def TestAlgorithm(self, algorithm, part=1):
        """
        :param algorithm: The algorithm function to test on the test data
        :param part: the part of the day's solution to test

        :returns: If the tests passed, otherwise raises exception since we should pass our tests
        """
        testData = self.testDataPartOne
        if part == 2:
            testData = self.testDataPartTwo

        for test in testData:
            processed = self.ProcessInput(data=test)
            result = algorithm(data=processed)
            if result != testData[test]:
                raise Exception("Test on data {} returned result {}".format(processed, result))

        return True

    def SolvePartOne(self, data=None):
        """
        Method to be implemented to solve for part one
        :returns: The solution for part one
        """
        raise NotImplementedError()

    def SolvePartTwo(self, data=None):
        """
        Method to be implemented to solve for part two
        :returns: The solution for part two
        """
        raise NotImplementedError()

    def Run(self):
        """
        Run the full suite of testing and processing for this day
        :return:
        """
        self.processed = self.ProcessInput()
        print('TestResult:', self.TestAlgorithm(self.SolvePartOne))
        print('Result: ', self.SolvePartOne())
        print('TestResult2:', self.TestAlgorithm(self.SolvePartTwo, part=2))
        print('Result: ', self.SolvePartTwo())


class Float2(list):
    """
    A Float2 object to make it easier to access and multiply 2-length lists of numbers
    """
    def __init__(self, inV):
        """

        :param inV: two-length list of numbers
        """
        inV = [float(v) for v in inV] # convert our inputs to floats
        super(Float2, self).__init__(inV)

    def __add__(self, other):
        return Float2([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Float2([self.x - other.x, self.y - other.y])

    def __mul__(self, other):
        return Float2([self.x * other.x, self.y * other.y])

    @property
    def x(self):
        """
        Access the first, X value of the list
        :return:
        """
        return self[0]

    @x.setter
    def x(self, v):
        self[0] = v

    @property
    def y(self):
        """
        The second, Y value of the list
        :return:
        """
        return self[1]

    @y.setter
    def y(self, v):
        self[1] = v


def dot(a, b):
    """
    :param a: list of numbers
    :param b: list of numbers equal in length to the first list
    :return: dot product of n-length lists of numbers
    """
    if len(a) != len(b):
        raise ValueError("Input lists must be of equal length (got {} and {})".format(len(a), len(b)))

    return sum([x * y for x, y in zip(a, b)])


def getBarycentric(p, a, b, c):
    """
    Get the barycentric coordinates of cartesin point a in
    reference frame abc

    :param p: Float2 test point
    :param a: Float2 point A
    :param b: Float2 point B
    :param c: Float2 point C
    :return: the UVW coordinate of cartesian point P in reference frame created by points ABC
    """
    v0 = b - a  # Vector BA
    v1 = c - a  # Vector CA
    v2 = p - a  # Vector PA
    d00 = dot(v0, v0)  # dot BA . BA
    d01 = dot(v0, v1)  # dot BA . CA
    d11 = dot(v1, v1)  # dot CA . CA
    d20 = dot(v2, v0)  # dot PA . BA
    d21 = dot(v2, v1)  # dot PA . CA

    denom = (d00 * d11) - (d01 * d01)

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return u, v, w
