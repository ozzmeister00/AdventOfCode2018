"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still
struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better.
You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers
(one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the
 same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented
 by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are
 entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others,
the input is large;  if you copy/paste your input, make sure you get the whole thing.)
"""
import string

from utils import ProblemSolver


class Day05Solver(ProblemSolver):
    """
    Solver for day 4
    """
    def __init__(self):
        super(Day05Solver, self).__init__(5)

        self.testDataPartOne = {'dabAcCaCBAcCcaDA': 10}

    def ProcessInput(self, data=None):
        """
        Map our input letters to positive or negative numbers and return them out in a list
        :param data:
        :return: a dict of {guardID: Guard}
        """
        if not data:
            data = self.rawData

        # map ASCII letters to positive or negative numbers
        letterMap = {string.ascii_uppercase[i]: i + 1 for i in range(len(string.ascii_uppercase))}
        letterMap.update({string.ascii_lowercase[i]: -1 * (i + 1) for i in range(len(string.ascii_lowercase))})

        processed = []

        for letter in data:
            processed.append(letterMap[letter])

        return processed

    def SolvePartOne(self, data=None):
        """
        Resolve the reactions in the polymer string until nothing can be resolved

        :param data:
        :return: The resulting length of the polymer string
        """
        if not data:
            data = self.processed

        pointer = 0
        changed = True

        polymer = data

        while changed:
            if pointer == 0:
                changed = False

            pointer += 1
            pointer %= len(polymer)





if __name__ == '__main__':
    day05 = Day05Solver()
    day05.Run()
