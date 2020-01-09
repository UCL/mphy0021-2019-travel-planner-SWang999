from argparse import ArgumentParser
import travelplanner


def process():

    parser = ArgumentParser(description='travelplanner')
    parser.add_argument('route_filepath_name', type=str,
                        help='Accepts a full path and full filename '
                             'csv file such as home/route.csv.')
    parser.add_argument('passenger_filepath_name', type=str,
                        help='Accepts a full path and full filename '
                             'csv file such as home/passenger.csv.')
    parser.add_argument('--speed', default=10, type=int,
                        help='Accepts a number indicating '
                             'the speed of the bus.')
    parser.add_argument('--saveplots', action='store_true',
                        help='Save the two plots.')

    arguments = parser.parse_args()

    passenger_t = travelplanner.read_passengers(
       arguments.passenger_filepath_name)
    route1 = travelplanner.Route(
       arguments.route_filepath_name, arguments.speed)
    passenger_list = []
    print(" Stops: minutes from start\n", route1.timetable())
    for data in passenger_t:
        passenger = travelplanner.Passenger(data[0], data[1], data[2])
        passenger_list.append(passenger)
        print("Trip for passenger: %s" % passenger.passengers_id)
        j = travelplanner.Journey(route=route1, passenger=[passenger])
        start, end = j.passenger_trip(passenger)
        total_time = j.travel_time(0)
        print((" Walk %3.2f units to stop %s, \n"
               " get on the bus and alite at stop %s and \n"
               " walk %3.2f units to your destination.") %
              (start[0], start[1], end[1], end[0]))
        # print((f" Walk {start[0]:3.2f} units to stop {start[1]}, \n"
        # f" get on the bus and alite at stop {end[1]} and \n"
        # f" walk {end[0]:3.2f} units to your destination."))
        print(
           " Total time of travel: %s minutes" % total_time)
        # print(f" Total time of travel: {total_time:03.2f} minutes")

    if arguments.saveplots:
        # Plots the route of the bus
        fig1 = route1.plot_map()
        fig1.savefig('./map.png')
        # Plots the number of passenger on the bus
        j2 = travelplanner.Journey(route=route1, passenger=passenger_list)
        fig2 = j2.plot_bus_load()
        fig2.savefig('./load.png')


if __name__ == "__main__":
    process()
