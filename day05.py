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

Speedups:
-- You can go in reverse through the polymer so you don't have to move quite as much
-- Then when you're resolving the polymer you know you can first try to react the stuff that you just collapsed
"""
import string

from utils import ProblemSolver


class Polymer(list):
    """
    A subclass of list that takes in a string of capital and lower case letters, and stores them as
    positive and negative integers to aid in properly resolve the polymer chain
    """

    # store off some class properties to make it easier to access these later
    LetterMap = {string.ascii_uppercase[i]: i + 1 for i in range(len(string.ascii_uppercase))}
    LetterMap.update({string.ascii_lowercase[i]: -1 * (i + 1) for i in range(len(string.ascii_lowercase))})
    NumberMap = {v: k for k, v in LetterMap.items()}

    def __init__(self, inString, *args, **kwargs):
        super(Polymer, self).__init__(*args, **kwargs)

        for i in inString:
            self.append(Polymer.LetterMap[i])

    def resolveAll(self):
        """
        Make a single resolution pass on the polymer starting with the 1st index and moving up
        until the pointer is beyond the size of this Polymer

        :return: if at any point we did, in fact, resolve a pair of polymers out
        """
        i = 0
        didChange = False
        while i < len(self):
            old = i
            i = self.resolve(i)

            # Resolve returns the index that we should be checking, and if we remove two indicies we want to say at
            # the same index
            # so if our new index equals the index we checked, then something changed and we set this flag
            if old == i:
                didChange = True

        return didChange

    def resolve(self, index):
        """
        Tries to resolve the polymer component and index and the index next to it

        If the sum of the two components is 0, we know we can resolve the away these two components

        :param index: where we should check
        :return: the index to check next (the same index if something was resolved
            (because the index + 2 item is now at index)
        """
        # make sure we can check the next item (if index + 1 > len(self) then we're out of range
        if index < len(self) - 1:
            if (self[index] + self[index + 1]) == 0:

                # pop out the next item
                self.pop(index + 1)

                # pop out the current item
                self.pop(index)
                return index

        return index + 1

    def __str__(self):
        """
        :return: the letter string representing this Polymer
        """
        return ''.join([Polymer.NumberMap[i] for i in self])


class Day05Solver(ProblemSolver):
    """
    Solver for day 5
    """
    def __init__(self):
        super(Day05Solver, self).__init__(5)

        self.testDataPartOne = {'dabAcCaCBAcCcaDA': 10}
        self.testDataPartTwo = {'dabAcCaCBAcCcaDA': 4}

    def ProcessInput(self, data=None):
        """
        Map our input letters to positive or negative numbers and return them out in a list
        :param data:
        :return: a Polymer object based off our input data
        """
        if not data:
            data = self.rawData

        processed = Polymer(data)

        return processed

    def SolvePartOne(self, data=None):
        """
        Resolve the reactions in the polymer string until nothing can be resolved

        :param data: the Polymer instance to use for resolving all
        :return: The resulting length of the polymer string
        """
        if not data:
            data = self.processed

        # resolve all until resolveAll returns false because nothing was changed
        while data.resolveAll():
            pass

        return len(data)

    def SolvePartTwo(self, data=None):
        """
        Make a series of polymers based off our test data, each one omitting one pair of letters

        And run tests on those
        :param data: the Polymer instance to start with
        :return: the shortest possible polymer chain if we removed one pair of letters
        """
        if not data:
            data = self.processed

        # convert our data back to a string so we can more easily manipulate it
        inString = str(data)

        # get a unique list of the letters in our string
        condensed = list(set(inString.lower()))

        # Make a new polymer by removing one lowercase and capital letter pair from our base polymer string
        tests = {letter: Polymer(inString.replace(letter, '').replace(letter.capitalize(), '')) for letter in condensed}

        results = {}

        for test in tests:
            results[test] = self.SolvePartOne(data=tests[test])

        print(results)

        return min(results.values())


if __name__ == '__main__':
    day05 = Day05Solver()
    day05.Run()
