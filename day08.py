from utils import ProblemSolver


class Node(object):
    def __init__(self, name, numChildren, numMetaDatas, parent):
        self.id = name
        self.numMetaDatas = numMetaDatas
        self.metaData = []
        self.numChildren = numChildren
        self.children = []
        self.parent = parent

    def getValue(self, nodes):
        if not self.numChildren:
            print('node ', self.id, 'has no children, returning metadata value', sum(self.metaData))
            return sum(self.metaData)

        else:
            total = 0
            print(self.metaData, self.children)
            for childIndex in self.metaData:
                if childIndex <= len(self.children):
                    childIndex -= 1
                    value = nodes[self.children[childIndex]].getValue(nodes)
                    print('child index, ', childIndex, 'childID', self.children[childIndex], 'value ', value)
                    total += value
                else:
                    print('childIndex', childIndex, 'is out of bounds of our children')
            return total

    def needsMetadata(self):
        return len(self.metaData) < self.numMetaDatas

    def childrenDiscovered(self):
        return len(self.children) == self.numChildren

    def __repr__(self):
        return 'Node({}, {}, {}, {})>{}'.format(self.id, self.numChildren, self.numMetaDatas, self.parent, self.metaData)


class Day08Solver(ProblemSolver):
    def __init__(self):
        super(Day08Solver, self).__init__(8)

        self.testDataPartOne = {'2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2': 138}
        self.testDataPartTwo = {'2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2': 66}

    def ProcessInput(self, data=None):
        """
        Parses the input tree string to determine each node's
        children and metadata, ultimately building a flat list
        :param data:
        :return:
        """

        if not data:
            data = self.rawData

        nodes = {}

        isNewID = True
        isMetaData = False
        currentNode = 0

        pointer = 0
        ints = [int(j) for j in data.split()]
        while pointer < len(ints):
            if isNewID:
                # current node is up one from the
                parent = currentNode
                currentNode = len(nodes.keys()) + 1 # our new node is now one-up from the length of the list, since it's just an identifier

                numChildren = ints[pointer]
                numMetaDatas = ints[pointer + 1]

                nodes[currentNode] = Node(currentNode, numChildren, numMetaDatas, parent)
                if parent:
                    nodes[parent].children.append(currentNode)

                # move the pointer up two spots
                pointer += 2

            # if we've disocvered all our children, the current pointer index is probably metadata
            if nodes[currentNode].childrenDiscovered():
                isMetaData = True
                isNewID = False
            # if we haven't discovered all the children for the current node, the next pointer is going to be a new ID
            else:
                isNewID = True
                isMetaData = False

            # get all the metadata in one go
            if isMetaData:
                while nodes[currentNode].needsMetadata():
                    nodes[currentNode].metaData.append(ints[pointer])
                    pointer += 1

                isMetaData = False
                currentNode = nodes[currentNode].parent

        return nodes

    def SolvePartOne(self, data=None):
        """
        Loop over all our nodes and return the sum of all the metadata
        :param data:
        :return:
        """
        if not data:
            data = self.processed

        flattenedList = sum([data[n].metaData for n in data], [])

        return sum(flattenedList)

    def SolvePartTwo(self, data=None):
        if not data:
            data = self.processed

        # for i in data:
        #     print(i, data[i].children)

        return data[1].getValue(data)

if __name__ == '__main__':
    day08 = Day08Solver()
    day08.Run()
