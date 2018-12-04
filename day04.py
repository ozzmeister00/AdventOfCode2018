"""
--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time, it's across from the prototype suit
 manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a
 guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first
person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight
for the past few months secretly observing this guard post! They've been writing down the ID of the
one guard on duty that night - the Elves seem to have decided that one guard was enough for the
overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or
waking up is always the one whose shift most recently started. Because all asleep/awake times
are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which
 shows the guard on duty that day; and Minute, which shows the minutes during which the
 guard was asleep within the midnight hour. (The Minute column's header shows the minute's
  ten's digit in the first row and the one's digit in the second row.) Awake is shown as .,
  and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on
the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute
 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able
to trick that guard into working tonight so you can have the best chance of sneaking in.
You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5),
 while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during
  minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order
you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (
In the above example, the answer would be 10 * 24 = 240.)


Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute
 - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose?
(In the above example, the answer would be 99 * 45 = 4455.)
"""

import datetime

from utils import ProblemSolver


class Guard(object):
    """
    Stores the information about a guard
    """
    def __init__(self, number):
        self.id = number
        self.midnight = [0 for i in range(0, 60)] # initialize a list of length 60 to represent each minute from 00:00 to 00:59
        self.shiftsLogs = []

    def processLogs(self):
        """
        Sort, Loop through all our shift logs and process them
        """
        self.shiftsLogs.sort()
        asleepTime = -1
        awakeTime = -1
        for log in self.shiftsLogs:
            if log.action == ShiftActions.FallsAsleep:
                asleepTime = log.minute
            elif log.action == ShiftActions.WakesUp:
                awakeTime = log.minute

            if asleepTime > 0 and awakeTime > 0:
                self.sleep(asleepTime, awakeTime)
                asleepTime = awakeTime = 0

    def sleep(self, start, end):
        """
        Log that the guard was asleep from start minute to end minute

        :param start: minute start of the sleep
        :param end: minute the guard wakes up
        """
        for i in range(start, end):
            self.midnight[i] += 1

    def asleepTime(self):
        """
        :return: the amount of time the guard spends asleep during all of their logged shifts
        """
        return sum(self.midnight)

    def asleepMinute(self):
        """
        :return: the index of the minute the guard is most asleep
        """
        return self.midnight.index(self.asleepMinuteTime())

    def asleepMinuteTime(self):
        """
        Return the maximum value of all our minute indicies at midnight
        (how many minutes were spent asleep during a given time)
        :return:
        """
        return max(self.midnight)

    def __lt__(self, other):
        return self.asleepTime() < other.asleepTime()

    def __le__(self, other):
        return self.asleepTime() <= other.asleepTime()

    def __eq__(self, other):
        return self.asleepTime() == other.asleepTime()

    def __ge__(self, other):
        return self.asleepTime() >= other.asleepTime()

    def __gt__(self, other):
        return self.asleepTime() > other.asleepTime()

    def __str__(self):
        return 'Guard #{} is asleep for {} minutes, and most likely for {} during minute {}'.format(self.id, self.asleepTime(), self.asleepMinuteTime(), self.asleepMinute())


class ShiftActions(object):
    """
    Enum class of the possible actions performed on a shift
    """
    StartsShift = 0
    FallsAsleep = 1
    WakesUp = 2


# map action enum to strings for later representation
ActionMapping = {ShiftActions.StartsShift: 'starts shift',
                 ShiftActions.FallsAsleep: 'falls asleep',
                 ShiftActions.WakesUp: 'wakes up'}


class ShiftLog(object):
    """
    Object to store a log of a guard's shift, from start to 1am
    """
    def __init__(self, dateString, action):
        self.datetime = datetime.datetime.strptime(dateString, '[%Y-%m-%d %H:%M')

        self.guardId = -1

        if 'begins shift' in action:
            self.action = ShiftActions.StartsShift
            self.guardId = int(action.replace('begins shift', '').replace('Guard #', ''))
        elif 'wakes up' in action:
            self.action = ShiftActions.WakesUp
        elif 'falls asleep' in action:
            self.action = ShiftActions.FallsAsleep
        else:
            raise ValueError('{} is an unrecognized action'.format(action))

    @property
    def minute(self):
        """
        Return the minute value of our datetime object
        :return:
        """
        minute = self.datetime.minute
        if self.datetime.hour > 0:
            minute -= 60
        return minute

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __le__(self, other):
        return self.datetime <= other.datetime

    def __eq__(self, other):
        return self.datetime == other.datetime

    def __ge__(self, other):
        return self.datetime >= other.datetime

    def __gt__(self, other):
        return self.datetime > other.datetime

    def __str__(self):
        return self.datetime.strftime('[%Y-%m-%d %H:%M]') + 'Guard #{} {}'.format(self.guardId, ActionMapping[self.action])


class Day04Solver(ProblemSolver):
    """
    Solver for day 4
    """
    def __init__(self):
        super(Day04Solver, self).__init__(4)

        self.testDataPartOne = {'''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up''': 240}
        self.testDataPartTwo = self.testDataPartOne.copy()

        # test data for part two is the same, just with a different value
        for test in self.testDataPartTwo:
            self.testDataPartTwo[test] = 4455

    def ProcessInput(self, data=None):
        """
         First parses the input log into a list of ShiftLogs, then sorts those using ShiftLog's custom
            equivalency functionality. Then figures out the guard ID associated with each log by marching
             forward through the log and associating IDs with those logs,
             and while it does that adds those log entries to the guard's data


        :param data:
        :return: a dict of {guardID: Guard}
        """
        if not data:
            data = self.rawData

        processed = {}

        logs = []

        for line in data.split('\n'):
            dt, action = line.split('] ')
            logs.append(ShiftLog(dt, action))

        # sort our entries by time
        logs.sort()

        # figure out which guard is active in each log
        activeGuard = -1
        for log in logs:
            if log.action == ShiftActions.StartsShift:
                activeGuard = log.guardId
                if activeGuard not in processed:
                    processed[activeGuard] = Guard(activeGuard)
                processed[activeGuard].shiftsLogs.append(log)
            else:
                log.guardId = activeGuard
                processed[log.guardId].shiftsLogs.append(log)

        for guard in processed:
            processed[guard].processLogs()

        return processed

    def SolvePartOne(self, data=None):
        """
        Finds the maximum value of all the "minutes" in our data (captializing on the custom equivalency functions) to
        find the correct guard for this test

        :param data:
        :return: the minute in which our most asleep guard was most asleep * the guard's ID
        """
        if not data:
            data = self.processed

        mostAsleep = max(data.values())

        return mostAsleep.asleepMinute() * mostAsleep.id

    def SolvePartTwo(self, data=None):
        """
        Builds a separate dict of {guardID: (how long the guard was asleep during their most asleep time,
                                                when the guard was most asleep)}

        Loops over that dict to find who was most asleep during their most asleep time

        :param data:
        :return: the ID of the guard who was most asleep at any given time * the time they were most asleep
        """
        if not data:
            data = self.processed

        asleepMinutes = {guard.id: (guard.asleepMinuteTime(), guard.asleepMinute()) for guard in data.values()}
        asleepDuration = -1
        asleepMinute = -1
        asleepId = -1
        for id in asleepMinutes:
            if asleepMinutes[id][0] > asleepDuration:
                asleepDuration = asleepMinutes[id][0]
                asleepMinute = asleepMinutes[id][1]
                asleepId = id

        return asleepId * asleepMinute


if __name__ == '__main__':
    day04 = Day04Solver()
    day04.Run()