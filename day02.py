"""
warehouse? They'd be stored together, so the box IDs should be similar. Too bad it would take forever to
 search the warehouse for two similar box IDs..." They walk too far away to hear any more.

Late at night, you sneak to the warehouse - who knows what kinds of paradoxes you could cause if you
were discovered - and use your fancy wrist device to quickly scan every box and produce a list of the
 likely candidates (your puzzle input).

To make sure you didn't miss any, you scan the likely candidate boxes again, counting the number
that have an ID containing exactly two of any letter and then separately counting those with exactly
 three of any letter. You can multiply those
two counts together to get a rudimentary checksum and compare it to what your device predicts.
"""

from utils import ProblemSolver, product

import collections
import itertools
import difflib


class Day02Solver(ProblemSolver):
    """
    Find the right box in Santa's warehouse!
    """
    def __init__(self):
        super(Day02Solver, self).__init__(2)
        self.testDataPartOne = {'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab': 12}
        self.testDataPartTwo = {'abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz\n': 'fgij'}

    def ProcessInput(self, data=None):
        """
        Pull the input list of newline separate strings into a list
        :param data:
        :return: processed data for us by downstream functions
        """
        if not data:
            data = self.rawData

        processed = []
        for i in data.split('\n'):
            processed.append(i.strip())

        return processed

    def SolvePartOne(self, data=None):
        """
        Loop over our input data, and find strings that have an occurrence of 2 or 3 repeating letters
        (but not counting each set of repeating letters in the same string. eg if aabbcc, that only counts for
        one "2" count

        :param data:
        :return: the product of two-letter and three-letter occurrences
        """
        if not data:
            data = self.processed

        counts = {2: 0, 3: 0}
        for id in data:
            letters = {letter: id.count(letter) for letter in set(id)}
            for count in counts.keys():
                if count in letters.values():
                    counts[count] += 1

        return product(counts.values())

    def SolvePartTwo(self, data=None):
        """
        The boxes will have IDs which differ by exactly one character at the same position in both strings.

        Create 2-length permutations of the input data to compare, then use difftools.ndiff
        to find the number of chnaged characters between the two strings.

        # TODO speed this up

        :param data:
        :return: the contracted ID for the box we're trying to find
        """
        if not data:
            data = self.processed

        comparisons = itertools.permutations(data, 2)
        stringDiffs = collections.defaultdict(list)

        for a, b in comparisons:
            diff = difflib.ndiff(a, b)
            diffCount = sum([1 for i in diff if i[0] == '-'])
            stringDiffs[diffCount].append((a, b))

        assert len(stringDiffs[1]) != 1, 'We found more than one comparison with a distance of 1'

        # grab the comparison that produced a good result
        a, b = stringDiffs[1][0]

        # if the letter in each position matches the comparison string, add that letter
        # to the output string
        output = ''
        for i, letter in enumerate(a):
            if b[i] == letter:
                output += letter

        return output


if __name__ == '__main__':
    day02 = Day02Solver()
    day02.Run()
