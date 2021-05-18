from finitequeue import FiniteQueue
from packet import Packet

class SystemState(object):
    
    """
    This class represents the state of our system.

    It contains information about whether the server is busy and how many customers
    are waiting in the queue (buffer). The buffer represents the physical buffer or
    memory of our system, where packets are stored before they are served.

    The integer variable buffer_content represents the buffer fill status, the flag
    server_busy indicates whether the server is busy or idle.

    The simulation object is only used to determine the maximum buffer space as
    determined in its object sim_param.
    """

    def __init__(self, sim):
        """
        Create a system state object
        :param sim: simulation object for determination of maximum number of stored
        packets in buffer
        :return: system_state object
        """
        self.last_arrival=0
        self.buffer_content = 0 #kept this one for debugging
        self.server_busy = False
        self.buffer=FiniteQueue(sim)
        self.served_packet=None
        self.sim = sim

    def add_packet_to_server(self):
        """
        Try to add a packet to the server unit.
        :return: True if server is not busy and packet has been added successfully.
        """
        iat= self.sim.sim_state.now - self.last_arrival
        self.last_arrival =self.sim.sim_state.now #update last arrival
        self.served_packet=Packet(self.sim,iat)
        self.served_packet.start_service()
        if self.server_busy:
            return False
        else:
           
            self.server_busy = True
            return True

    def add_packet_to_queue(self):
        """
        Try to add a packet to the buffer.

        :return: True if buffer/queue is not full and packet has been added successfully.
        """
        iat= self.sim.sim_state.now - self.last_arrival
        self.last_arrival =self.sim.sim_state.now #update last arrival
        pkt=Packet(self.sim,iat)
        return self.buffer.add(pkt)

    def complete_service(self):
        """
        Reset server status to idle after a service completion.
        """
        self.served_packet.complete_service()
        self.server_busy = False
        self.sim.counter_collection.count_packet(self.served_packet)

    def start_service(self):
        """
        If the buffer is not empty, take the next packet from there and serve it.
        :return: True if buffer is not empty and a stored packet is being served.
        """
        if self.buffer.get_queue_length() == 0:
            return False
        else:
            self.buffer_content -= 1
            self.served_packet=self.buffer.remove()
            self.served_packet.start_service()
            self.server_busy = True
            return True
    
    def get_queue_length(self):
        return self.buffer.get_queue_length()
