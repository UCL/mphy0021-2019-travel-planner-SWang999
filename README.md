Greetings!
------------------------

This is a travelplanner package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

This package can help you plan some passengers' journey on a specific route. If you are a navigation software developer or a staff of passenger transport center, hope this could help you a lot.

## Installation

Browse to the directory where this file lives, and run:
```bash
pip install .
```
That command will download any dependencies we have


## Usage: 

----Invoke the tool----

Invoke the tool with 'bussimula <route_file_name> <passengers_file_name>  --speed <int> --saveplots <Bool>'

It will print a timetable about this route like {Stops: minutes from start} and then it will print travel indications for every passenger in the 'passenger.csv'. Also it will plot two pictures showing the map of the route and the evolution of the load. If '--saveplots' is True, these two picture will be saved in files named map.png and load.png respectively at where you use this command. 

Note that the file name should be a complete file path name like '/home/muchun/PycharmProjects/travel/route.csv'

speed's default value is 10

saveplots's default value is False 

You can edit the bus's speed such as 15 minutes per unit by '--speed 15'

You can choose to save the route map and bus load plot by '--saveplots True'

--For Example--

'''bash
$ bussimula /home/muchun/PycharmProjects/travelplanner/route.csv /home/muchun/PycharmProjects/travelplanner/passengers.csv --speed 25 --saveplots True
'''

---Cite this package---

Cite this package with 'from travelplanner import Passenger, Route, Journey, read_passenger

------------------------
Passenger class takes a starting point, end point and speed

it has the following methods:

    walk_time(): gives the time that this passenger would need to get from their starting point to their
    end point, walking at their speed.

You can use read_passenger(<passengers_csv_filename>) to read passenger data from csv file. It would return a list contain every passenger's data in forms like [((starting point), (end point), speed),((starting point), (end point), speed)]

-------------------------

Route class takes a file name and a optional paramater bus speed (default = 10)

it has the following methods:

    plot_map(): plots and displays a map of the route

    timetable(): returns a dictionary mapping stop names to times, assuming the first stop is at time 0.

    generate_cc(): returns a tuple containing the starting point and a string with the chain code.

    valid_check(): checks whether this route is valid. This method will be called automatically when defining a Route class.

-------------------------

Journey class takes a Route and a list of Passenger objects

it has the following methods:

    plot_bus_load(): plots and displays a graph of the number of passengers on the bus as it moves along the route

    travel_time(id): returns a dictionary of times about how long that passenger spent on that mode of transport for 
    the passenger with the specified id.

    print_time_stats(): print average time on bus and average walking time for all passengers.

--------------------------

