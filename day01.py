"""
Problem:
After feeling like you've been falling for a few minutes, you look at the device's tiny screen.
"Error: Device must be calibrated before first use. Frequency drift detected. Cannot maintain destination lock."
 Below the message, the device shows a sequence of changes in frequency (your puzzle input).
 A value like +6 means the current frequency increases by 6; a value like -3 means the current frequency
 decreases by 3.

 Starting with a frequency of zero, what is the resulting frequency
  after all of the changes in frequency have been applied?
"""

from utils import ProblemSolver


class Day01Solver(ProblemSolver):
    """
    Solves and tests for Day One
    """
    def __init__(self):
        super(Day01Solver, self).__init__(1)
        self.testDataPartOne = {'+1\n+1\n+1': 3,
                                '+1\n+1\n-2': 0,
                                '-1\n-2\n-3': -6
                                }

        self.testDataPartTwo = {'+1\n-1': 0,
                                '+3\n+3\n+4\n-2\n-4': 10,
                                '-6\n+3\n+8\n+5\n-6': 5,
                                '+7\n+7\n-2\n-7\n-4': 14
                                }

    def ProcessInput(self, data=None):
        """

        :param data:
        :return: processed data
        """
        if not data:
            data = self.rawData

        processed = []
        for i in data.split('\n'):
            processed.append(int(i.strip()))

        return processed

    def SolvePartOne(self, data=None):
        """
        Loop over our input data, and sum it all together
        :param data:
        :return: the resulting frequency
        """
        if not data:
            data = self.processed

        frequency = 0
        for i in data:
            frequency += i

        return frequency

    def SolvePartTwo(self, data=None):
        """
        Loop over the input data, storing the current frequency, until we find a frequency that
        gets hit twice
        :param data:
        :return:
        """
        if not data:
            data = self.processed

        currentFrequency = 0
        found = False
        currentIndex = 0

        frequencies = {currentFrequency} # set literal, who knew!?

        while not found:
            currentFrequency += data[currentIndex]

            oldLength = len(frequencies)

            frequencies.add(currentFrequency)

            newLength = len(frequencies)

            # if nothing gets added to the set, then we hit that number twice and return it
            if oldLength == newLength:
                found = True
                return currentFrequency

            currentIndex += 1
            currentIndex %= len(data) # keep our data in range


if __name__ == '__main__':
    day01 = Day01Solver()
    day01.Run()


