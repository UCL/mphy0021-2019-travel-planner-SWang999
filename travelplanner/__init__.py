import math
import csv
import numpy as np
import matplotlib.pyplot as plt


def read_passengers(file):
    passengers = []
    with open(file, newline='', encoding='UTF-8') as f:
        rows = csv.reader(f)
        for row in rows:
            row = [int(x) for x in row]
            passengers.append(((row[0], row[1]), (row[2], row[3]), row[4]))
    return passengers


class Passenger(object):
    '''
    >>> john = Passenger((5,1), (3,13), 20)
    >>> print(john.walk_time())
    243.31050121192877
    '''
    passengers_id = 0

    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed
        self.id = Passenger.passengers_id
        Passenger.passengers_id += 1

    def walk_time(self):
        distance = math.sqrt((self.end[0] - self.start[0])**2 +
                             (self.end[1] - self.start[1])**2)
        return distance*self.speed


class Route(object):
    def __init__(self, filename, bus_speed=10):
        self.filename = filename
        self.route = self.read_route(self.filename)
        self.speed = bus_speed
        self.valid_check()

    def read_route(self, filename):
        route = []
        with open(filename, newline='', encoding='UTF-8') as f:
            rows = csv.reader(f)
            for row in rows:
                route.append((int(row[0]), int(row[1]), row[2]))
        return route

    def plot_map(self):
        max_x = max([n[0] for n in self.route]) + 5
        max_y = max([n[1] for n in self.route]) + 5
        grid = np.zeros((max_y, max_x))
        for x, y, stop in self.route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        figure = plt.gcf()
        plt.show()
        return figure

    def timetable(self):
        time = 0
        stops = {}
        for step in self.route:
            if step[2]:
                stops[step[2]] = time
            time += self.speed
        return stops

    def generate_cc(self):
        start = self.route[0][:2]
        cc = []
        freeman_cc2coord = {0: (1, 0),
                            1: (1, -1),
                            2: (0, -1),
                            3: (-1, -1),
                            4: (-1, 0),
                            5: (-1, 1),
                            6: (0, 1),
                            7: (1, 1)}
        freeman_coord2cc = {val: key for key, val in freeman_cc2coord.items()}
        for b, a in zip(self.route[1:], self.route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(str(freeman_coord2cc[(x_step, y_step)]))
        return start, ''.join(cc)

    def valid_check(self):
        start, check = self.generate_cc()
        check = list(check)
        for i in check:
            if int(i) % 2 == 1:
                raise ValueError('Route is invalid because '
                                 'diagonal moves are not allowed')


class Journey(object):
    bus_time_total = 0
    walk_time_total = 0

    def __init__(self, route, passenger):
        self.route = route
        self.passenger = passenger

    def plot_bus_load(self):
        stops = {step[2]: 0 for step in self.route.route if step[2]}
        for member in self.passenger:
            trip = self.passenger_trip(member)
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
        prev = ''
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        fig, ax = plt.subplots()
        ax.step(tuple(range(len(stops))), tuple(stops.values()), where='post')
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        figure = plt.gcf()
        plt.show()
        return figure

    def passenger_trip(self, passenger):
        start = passenger.start
        end = passenger.end
        stops = [value for value in self.route.route if value[2]]
        # calculate closer stops
        # start
        distances = [(math.sqrt(
                    (x - start[0]) ** 2 +
                    (y - start[1]) ** 2), stop) for x, y, stop in stops]
        closer_start = min(distances,
                           key=lambda item: (item[0], -ord(item[1])))
        # end
        distances = [(math.sqrt(
                    (x - end[0]) ** 2 +
                    (y - end[1]) ** 2), stop) for x, y, stop in stops]
        closer_end = min(distances)
        return closer_start, closer_end

    def travel_time(self, passenger_id):
        trip = self.passenger_trip(passenger=self.passenger[passenger_id])
        timetab = self.route.timetable()
        walktime = self.passenger[passenger_id].walk_time()
        bus_travel = timetab[trip[1][1]] - timetab[trip[0][1]]
        walk_travel = \
            trip[0][0] * self.passenger[passenger_id].speed + \
            trip[1][0] * self.passenger[passenger_id].speed
        if bus_travel + walk_travel > walktime:
            return walktime
        else:
            return bus_travel + walk_travel

    def print_time_stats(self):
        for member in self.passenger:
            trip = self.passenger_trip(passenger=member)
            timetab = self.route.timetable()
            walktime = member.walk_time()
            bus_travel = timetab[trip[1][1]] - timetab[trip[0][1]]
            walk_travel = trip[0][0] * member.speed + trip[1][0] * member.speed
            if bus_travel + walk_travel > walktime:
                self.walk_time_total += walktime
            else:
                self.bus_time_total += bus_travel
                self.walk_time_total += walk_travel
        passenger_num = len(self.passenger)
        print('Average time on bus: %.2f min \n'
              'Average walking time: %.2f min' %
              (self.bus_time_total/passenger_num,
               self.walk_time_total/passenger_num))
