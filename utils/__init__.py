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

