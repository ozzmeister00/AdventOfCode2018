"""
--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

from utils import ProblemSolver

import collections
import string


class Step(object):
    """
    An object that represents a step in the sleigh-building process that knows
    what steps must preceed it and what steps need it to proceed
    """
    def __init__(self, letter='', successor=None, predecessor=None):

        self.letter = letter

        self.predecessors = []
        self.successors = []

        self.completed = False
        self.inProgress = False

        if successor:
            self.successors.append(successor)

        if predecessor:
            self.predecessors.append(predecessor)

    def __str__(self):
        return ''.join(self.predecessors) + '>' + self.letter + '>' + ''.join(self.successors)

    def __repr__(self):
        return 'Step("{}", predecessors={}, successors={})'.format(self.letter, self.predecessors, self.successors)


class Elf(object):
    """
    Represents a worker who can work on a task
    """
    def __init__(self, name):
        self.name = name
        self.task = ''
        self.timer = 0

    def update(self):
        """
        decrement the timer, and if our timer is 0, blank our task
        :return:
        """
        self.timer -= 1
        self.timer = max(0, self.timer)
        if self.timer == 0 and self.task:
            task = self.task
            self.task = ''
            return task

        return None

    def isAvailable(self):
        """
        :return: if this elf is available for a task
        """
        return self.task == ''

    def assignTask(self, task, timer):
        """
        assign us a task and set our timer properly
        :param task: the id of the task
        :param timer: how long it will take to finish the task
        :return:
        """
        # for safety
        if not self.isAvailable():
            raise Exception("This elf {} is not available, we're currently working on {}".format(self.name, self.task))

        #print('worker {} assigned task {} for {} seconds'.format(self.name, task, timer))

        self.task = task
        self.timer = timer


def allFinished(instructions):
    """
    Determine if any of the steps in our instruciton list are uncompleted.
    :param instructions:
    :return: if all instructions are completed
    """
    for i in instructions:
        if not instructions[i].completed:
            return False

    return True


def firstAvailable(instructions):
    """
    Sort our instructions alphabetically, then test if their predecessors are all completed
    and return that key

    :param instructions:
    :return:
    """
    for i in sorted(instructions.keys()):
        if not instructions[i].completed and not instructions[i].inProgress:
            # deteremine our predecessors
            predecessors = {p: instructions[p] for p in instructions[i].predecessors}

            # if they're all finished, return it
            if allFinished(predecessors):
                return i

    return None


class Day07Solver(ProblemSolver):
    """
    Processes and solves day 07
    """

    def __init__(self):
        super(Day07Solver, self).__init__(7)

        self.testDataPartOne = {'Step C must be finished before step A can begin.\nStep C must be finished before step F can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step D can begin.\nStep B must be finished before step E can begin.\nStep D must be finished before step E can begin.\nStep F must be finished before step E can begin.': 'CABDFE'}
        self.testDataPartTwo = {'Step C must be finished before step A can begin.\nStep C must be finished before step F can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step D can begin.\nStep B must be finished before step E can begin.\nStep D must be finished before step E can begin.\nStep F must be finished before step E can begin.': 15}

    def ProcessInput(self, data=None):
        """
        Build a dict mapping steps to a Step object that can hold the step's predecessors and successors
        """
        if not data:
            data = self.rawData

        processed = collections.defaultdict(Step)

        for line in data.split('\n'):
            tokens = line.split(' ')
            step = tokens[1]
            successor = tokens[-3]

            processed[step].successors.append(successor)
            processed[successor].predecessors.append(step)

        # populate this information here since we're relying on defaultdict to do the work for us up top
        for key in processed:
            processed[key].letter = key

        return processed

    def SolvePartOne(self, data=None):
        """

        :param data:
        :return:
        """
        if not data:
            data = self.processed

        completedOrder = []

        while not allFinished(data):
            first = firstAvailable(data)
            if first:
                completedOrder.append(first)
                data[first].completed = True
            else:
                raise Exception("something has gone wrong and nothing is available")

        return ''.join(completedOrder)

    def SolvePartTwo(self, data=None):
        """

        :param data:
        :return:
        """
        def getTaskTime(task):
            """

            :param task: the name of the task
            :return: how long the task should take (taskFactor + letter index)
            """
            return string.ascii_uppercase.index(task) + taskFactor + 1

        def firstAvailableWorker(workers):
            """
            # TODO this would be cooler if our worker pool was an object too
            :param workers: our workerpool
            :return: None, or the first available worker
            """
            for i, worker in enumerate(workers):
                if worker.isAvailable():
                    return i

            return -1

        if not data:
            data = self.processed
            for key in data:
                data[key].completed = False

        completedOrder = []

        taskFactor = 0
        workerPoolSize = 2

        # if we're not in test mode, scale up our pool and task timing
        if len(data) > 10:
            taskFactor = 60
            workerPoolSize = 5

        workerPool = [Elf(i) for i in range(workerPoolSize)]

        time = 0

        while not allFinished(data):

            # if we have any available workers
            while firstAvailableWorker(workerPool) > -1:
                newTask = firstAvailable(data)

                # if nothing is available, break out of this loop
                if not newTask:
                    break

                taskTime = getTaskTime(newTask)
                workerPool[firstAvailableWorker(workerPool)].assignTask(newTask, taskTime)
                data[newTask].inProgress = True

            debugString = str(time)

            for worker in workerPool:
                debugString += ' {}'.format(worker.task or '.')

            print(debugString)

            # update all our workers
            for worker in workerPool:
                completedTask = worker.update()
                if completedTask:
                    completedOrder.append(completedTask)
                    data[completedTask].completed = True

            time += 1

        return time


if __name__ == '__main__':
    day07 = Day07Solver()
    day07.Run()
