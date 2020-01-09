import pytest
from travelplanner import Passenger, Route, Journey, read_passengers
import os


def test_invalid():
    with pytest.raises(ValueError):
        route_invalid = Route(os.path.join(
                              os.path.dirname(__file__),
                              'route_invalid.csv'))


def test():
    john = Passenger(start=(5, 1), end=(3, 13), speed=20)
    passenger_data_list = read_passengers(
        os.path.join(
            os.path.dirname(__file__),
            'passengers.csv'))
    print(john.walk_time())
    route1 = Route(os.path.join(
        os.path.dirname(__file__),
        'route.csv'))
    route1.plot_map()
    print(route1.timetable())
    print(route1.generate_cc())
    passenger_list = []
    for data in passenger_data_list:
        passenger = Passenger(data[0], data[1], data[2])
        passenger_list.append(passenger)
    j = Journey(route1, passenger_list)
    j.plot_bus_load()
    start, end = j.passenger_trip(j.passenger[0])
    print(start, end)
    print(j.travel_time(0))
    j.print_time_stats()


if __name__ == '__main__':
    test()
    test_invalid()
