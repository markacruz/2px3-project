from asyncio import events
from asyncio.windows_events import NULL
import random 

#Constants
ARRIVAL = "Arrival"
DEPARTURE = "Departure"
STOP = "Stop"
E = "East"
S = "South"
W = "West"
MEAN_ARRIVAL_TIME = random.randint(10, 20)
PRINT_EVENTS = False

class Driver:

    stop_time = random.randint(3, 6)
    clear_time = random.randint(5, 10)

    def __init__(self, name, arrival_time):
        self.name = name
        self.arrival_time = arrival_time
    
    #Returns driver instance stop time
    def get_stop_time(self):
        return self.stop_time

    #Returns driver instance clear time
    def get_clear_time(self):
        return self.clear_time

class Event:

    def __init__(self, event_type, time, direction):
        self.type = event_type
        self.time = time
        self.direction = direction 

        clear_direction = ""
        generate_random = random.randint(0,1)
                
        if self.direction == E:
            if generate_random == 0:
                clear_direction = 'West'
            else:
                clear_direction = 'South'
        elif self.direction == W:
            if generate_random == 0:
                clear_direction = 'East'
            else:
                clear_direction = 'South'
        else:
            if generate_random == 0:
                clear_direction = 'West'
            else:
                clear_direction = 'East'

        self.clear_direction = clear_direction

class EventQueue:

    def __init__(self):
        self.events = []

    #Add event (will get sent to the back of the queue)
    def add_event(self, event):
        # print("Adding event: " + event.type + ", clock: " + str(event.time))
        self.events.append(event)

    #Get the next event in the queue and pop it (remove it)
    #Returns removed next event
    def get_next_event(self):
        min_time = 9999999999999
        min_index = 0
        for i in range(len(self.events)):
            if self.events[i].time < min_time:
                min_time = self.events[i].time
                min_index = i
        event = self.events.pop(min_index)
        # print("Removing event: " + event.type + ", clock: " + str(event.time))
        return event

class Simulation:

    upper_arrival_time = 2 * MEAN_ARRIVAL_TIME

    def __init__(self, total_arrivals):
        self.num_of_arrivals = 0
        self.total_arrivals = total_arrivals
        self.clock = 0

        """
        Each road is represented as a list of waiting cars. You may
        want to consider making a "road" a class.
        """
        self.east, self.south, self.west = [], [], []
        self.east_ready = False
        self.south_ready = False
        self.west_ready = False
        self.intersection_free = True
        self.events = EventQueue()
        self.generate_arrival()
        self.print_events = PRINT_EVENTS
        self.data = []
        self.stop_time = []
        self.clear_time = []

    #Enable printing events as the simulation runs
    def enable_print_events(self):
        self.print_events = True
    
    #Method that runs the simulation
    def run(self):
        while (self.num_of_arrivals <= self.total_arrivals) | (self.events.events != []):
            if self.print_events:
                self.print_state()
            self.execute_next_event()
            
    #Execute the next event in the queue
    #(Get next event, and execute appropriate method depending on event type)
    def execute_next_event(self):
        
        event = self.events.get_next_event()
        self.clock = event.time
        if event.type == ARRIVAL:
            self.execute_arrival(event)
        if event.type == DEPARTURE:
            self.execute_departure(event)
        if event.type == STOP:
            self.execute_stop(event)

    #Driver leaving intersection event
    def execute_departure(self, event):

        if self.print_events:
            print(str(self.clock)+ ": A driver from the " + event.direction + " has cleared the intersection going " + event.clear_direction + ".")
        
        # smallest_depart_time = 9999999999
        # next_depart = NULL
        # empty = len(self.east) == 0 & len(self.west) == 0 & len(self.south) == 0  

        # for i in self.events.events:
        #     if i.type == STOP:
        #         if (i.time) < smallest_depart_time:
        #             next_depart = i.direction
                    
        # if event.direction == E:

        #     #No drivers left to depart from the East
        #     if self.east == []:
        #         self.east_ready = False
        
        #     #Carry on to other direction waitlists
        #     if (next_depart == W) & (self.west_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == S) & (self.south_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == E) & (self.east_ready == True):
        #         self.depart_from(next_depart)
        #     else:
        #         self.intersection_free = True

        # if event.direction == S:

        #     #No drivers left to depart from the South
        #     if self.south == []:
        #         self.south_ready = False
        
        #     #Carry on to other direction waitlists
        #     if (next_depart == W) & (self.west_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == S) & (self.south_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == E) & (self.east_ready == True):
        #         self.depart_from(next_depart)
        #     else:
        #         self.intersection_free = True

        # if event.direction == W:

        #     #No drivers left to depart from the West
        #     if self.west == []:
        #         self.west_ready = False
        
        #     #Carry on to other direction waitlists
        #     if (next_depart == W) & (self.west_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == S) & (self.south_ready == True):
        #         self.depart_from(next_depart)
        #     elif (next_depart == E) & (self.east_ready == True):
        #         self.depart_from(next_depart)
        #     else:
        #         self.intersection_free = True

        #Lots of "traffic logic" below. It's just a counter-clockwise round-robin.

        if event.direction == E:

            #No drivers left to depart from the East
            if self.east == []:
                self.east_ready = False
        
            #Carry on to other direction waitlists
            if self.west_ready:
                self.depart_from(W)
            elif self.south_ready:
                self.depart_from(S)
            elif self.east_ready:
                self.depart_from(E)
            else:
                self.intersection_free = True

        if event.direction == S:

            #No drivers left to depart from the South
            if self.south == []:
                self.south_ready = False
        
            #Carry on to other direction waitlists
            if self.east_ready:
                self.depart_from(E)
            elif self.west_ready:
                self.depart_from(W)
            elif self.south_ready:
                self.depart_from(S)
            else:
                self.intersection_free = True

        if event.direction == W:

            #No drivers left to depart from the West
            if self.west == []:
                self.west_ready = False
        
            #Carry on to other direction waitlists
            if self.south_ready:
                self.depart_from(S)
            elif self.east_ready:
                self.depart_from(E)
            elif self.west_ready:
                self.depart_from(W)
            else:
                self.intersection_free = True
    
    #Create departure event for the first driver from the queue in the passed direction
    def depart_from(self, direction):
        
        #Make departure event for first car in East queue 
        if direction == E:
            clear_time = self.clock + self.east[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, E)
            driver = self.east.pop(0) #Car progessing into the intersection
            
        #Make departure event for first car in South queue
        if direction == S:
            clear_time = self.clock + self.south[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, S)
            driver = self.south.pop(0) #Car progessing into the intersection

        #Make departure event for first car in West queue 
        if direction == W:
            clear_time = self.clock + self.west[0].get_clear_time()
            new_event = Event(DEPARTURE, clear_time, W)
            driver = self.west.pop(0) #Car progessing into the intersection
            
        self.events.add_event(new_event)
        self.intersection_free = False
        self.stop_time.append(driver.stop_time)
        self.clear_time.append(driver.clear_time)
        self.data.append(clear_time - driver.arrival_time)

    #Stop driver at intersection, and call depart method to add depart event to queue
    def execute_stop(self, event):
        if self.print_events:
            print(str(self.clock)+ ": A driver from the " + event.direction + " has stopped.")

        if event.direction == E:
            self.east_ready = True
            if self.intersection_free:
                self.depart_from(E)

        if event.direction == S:
            self.south_ready = True
            if self.intersection_free:
                self.depart_from(S)

        if event.direction == W:
            self.west_ready = True
            if self.intersection_free:
                self.depart_from(W)
                
    #Start arrival event 
    def execute_arrival(self, event):
        driver = Driver(self.num_of_arrivals, self.clock)
        if self.print_events:
            print(str(self.clock)+ ": A driver arrives from the " + event.direction + ".")
            
        if event.direction == E:
            if self.east == []: #Car needs to stop before clearing
                self.east_ready = False
            self.east.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), E)
            self.events.add_event(new_event)
            
        elif event.direction == S:
            if self.south == []: #Car needs to stop before clearing
                self.south_ready = False
            self.south.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), S)
            self.events.add_event(new_event)
            
        else:
            if self.west == []: #Car needs to stop before clearing
                self.west_ready = False
            self.west.append(driver)
            new_event = Event(STOP, self.clock + driver.get_stop_time(), W)
            self.events.add_event(new_event)
            
        if (self.num_of_arrivals <= self.total_arrivals):
            self.generate_arrival() #Generate the next arrival

    #Generate a car arriving at the intersection
    def generate_arrival(self):
        #Generates a random number uniformily between 0 and upper_arrival_time
        inter_arrival_time = random.random() * self.upper_arrival_time
        time = self.clock + inter_arrival_time
        
        r = random.random()
        #Equally likely to arrive from each direction
        if r < (1/3):
            self.events.add_event(Event(ARRIVAL, time, E))
        elif r < (2/3):
            self.events.add_event(Event(ARRIVAL, time, S))
        else:
            self.events.add_event(Event(ARRIVAL, time, W))
        self.num_of_arrivals += 1 #Needed for the simulation to terminate

    def print_state(self):
        print("[E,S,W] = [" + str(len(self.east)) +","+ str(len(self.south)) +","+ str(len(self.west)) +"]")

    def generate_report(self):
        #Define a method to generate statistical results based on the time values stored in self.data
        #These could included but are not limited to: mean, variance, quartiles, etc. 

        # print("Avg. Stop Time: " + str(sum(self.stop_time)/len(self.stop_time)) +
        #  "s, Avg. Clear Time: " + str(sum(self.clear_time)/len(self.clear_time)) + "s")

        mean = sum(self.data)/len(self.data)
        variance = sum((xi - mean) ** 2 for xi in self.data) / len(self.data)

        return("Mean: " + str(mean) + " seconds")

def run():
    for x in range(100):
        sim = Simulation(5)
        sim.run()
        print("Simulation " + str(x + 1) + ": " + sim.generate_report())