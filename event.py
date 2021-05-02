import heapq
import random
from simstate import SimState


class EventChain(object):
    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time.
    Always the oldest event is removed.
    """

    def __init__(self):
        """
        Initialize variables and event chain
        """
        self.event_list = []

    def insert(self, e):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent

        """
        # TODO Task 1.2.2: Your code goes here
        heapq.heappush(self.event_list,e)

    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (if timestamps are equal then smallest priority value i.e. highest priority event) from queue
        :return: next event in event chain
        """
        # TODO Task 1.2.2: Your code goes here
        return heapq.heappop(self.event_list)
        


class SimEvent(object):
    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for EventChain insertion is implemented by comparing first the timestamps and then the priorities
    """

    def __init__(self, sim, timestamp):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        """
        self.timestamp = timestamp
        self.priority = 0
        self.sim = sim

    def process(self):
        """
        General event processing routine. Should be implemented in subclass
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, priorities are compared.
        """
        if self.timestamp == other.timestamp:
            return self.priority < other.priority

        if self.timestamp < other.timestamp:
            return self.timestamp < other.timestamp
        
        # TODO Task 1.2.1: Your code goes here
 


class CustomerArrival(SimEvent):
    """
    Defines a new customer arrival event (new packet comes into the system)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new customer arrival event with given execution time.

        Priority of customer arrival event is set to 1 (second highest)
        """
        super(CustomerArrival, self).__init__(sim, timestamp)
        self.priority = 1

    def process(self):
        """
        Processing procedure of a customer arrival.

        Implement according to the task description.
        """
        # TODO Task 1.3.2: Your code goes here

        self.sim.sim_state.now=self.timestamp
        if not self.sim.system_state.add_packet_to_server():
            if not self.sim.system_state.add_packet_to_queue():
                self.sim.sim_state.packet_dropped()
                print('drop the packet')
            else:
                print('packet added to queue')
                self.sim.sim_state.packet_accepted()
        else:
            print('packet added to server')
            self.sim.sim_state.packet_accepted()
            if self.sim.sim_param.init_rand:
                random.seed(self.sim.sim_param.SEED)
                self.sim.sim_param.init_rand = False
            time=self.timestamp+random.randint(1,1000)
            self.sim.event_chain.insert(ServiceCompletion(self.sim,time))
        
        self.timestamp+=self.sim.sim_param.IAT 
        self.sim.event_chain.insert(self)


class ServiceCompletion(SimEvent):
    """
    Defines a service completion event (highest priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new service completion event with given execution time.

        Priority of service completion event is set to 0 (highest).
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.priority = 0

    def process(self):
        """
        Processing procedure of a service completion.

        Implement according to the task description
        """
        # TODO Task 1.3.3: Your code goes here
        self.sim.system_state.server_busy=False #let the server breathe for a moment
        self.sim.sim_state.now = self.timestamp
        if self.sim.system_state.buffer_content==0:
            self.sim.system_state.complete_service()
        else:
            if self.sim.system_state.start_service():
                time=self.timestamp+ random.randint(1,1000)
                self.sim.event_chain.insert(ServiceCompletion(self.sim, time))

class SimulationTermination(SimEvent):
    """
    Defines the end of a simulation. (least priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.

        Priority of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.priority = 2

    def process(self):
        """
        Implement according to the task description.
        """
        # TODO Task 1.3.1: Your code goes here
        self.sim.sim_state.now=self.timestamp
        self.sim.event_chain.insert(self)
        self.sim.sim_state.stop=True

