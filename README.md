## Background

### Distance-Vector Routing

* Each router keeps its own distance vector, which contains its distance to all destinations.
* When a router receives a distance vector from a neighbor, it updates its own
distance vector and the forwarding table.
* Each router broadcasts its own distance vector to all neighbors when the distance vector changes. The broadcast is also done periodically if no detected change has occurred.
* Each router **does not** broadcast the received distance vector to its neighbors. It **only** broadcasts its own distance vector to its neighbors.

### Link-State Routing

* Each router keeps its own link state and other nodes' link states it receives. The link state of a router contains the links and their weights between the router and its neighbors.
* When a router receives a link state from its neighbor, it updates the stored link state and the forwarding table. **Then it broadcasts the link state to other neighbors.**
* Each router broadcast its own link state to all neighbors when the link state changes. The broadcast is also done periodically if no detected change has occurred.
* A sequence number is added to each link state message to distinguish between old and new link state messages. Each router stores the sequence number together with the link state. If a router receives a link state message with a smaller sequence number (i.e., an old link state message), the link state message is simple disregarded.

### Method descriptions
These are the methods you need to complete in `DVrouter` and `LSrouter`:

* `__init__(self, addr, heartbeatTime)`
  * Class constructor. `addr` is the address of this router.  Add your own class fields and initialization code (e.g. to create forwarding table data structures). Routing information should be sent by this router at least once every `heartbeatTime` milliseconds.


* `handlePacket(self, port, packet)`
  * Process incoming packet: This method is called whenever a packet arrives at the router on port number `port`. You should check whether the packet is a traceroute packet or a routing packet and handle it appropriately. Methods and fields of the packet class are defined in `packet.py`.


* `handleNewLink(self, port, endpoint, cost)`
  * This method is called whenever a new link is added to the router on port number `port` connecting to a router or client with address `endpoint` and link cost `cost`.  You should store the argument values in a data structure to use for routing. If you want to send packets along this link, call `self.send(port, packet)`.  


* `handleRemoveLink(self, port)`
  * This method is called when the existing link on port number `port` is disconnected. You should update data structures appropriately.


* `handleTime(self, timeMillisecs)`
  * This method is called regularly and provides you with the current time in millisecs for sending routing packets at regular intervals.


* `debugString(self)`
  * This method is called by the network visualization to print current details about the router.  It should return any string that will be helpful for debugging. This method is for your own use and will not be graded.

## Running and Testing

You should test your `DVrouter` and `LSrouter` using the provided network simulator.  There are multiple json files defining different network architectures and  link failures and additions.  "05_pg242_net.json" and "03_pg244_net.json" files define the networks on pages 242 and 244 of the provided textbook reading respectively.  The json files without "events" in their file name do not have link failures or additions and are good for initial testing.

Run the simulation with the graphical interface using the command

`python visualize_network.py [networkSimulationFile.json] [DV|LS]`

The argument `DV` or `LS` indicates whether to run `DVrouter` or `LSrouter`, respectively.  

Run the simulation without the graphical interface with the command

`python network.py [networkSimulationFile.json] [DV|LS]`

The routes to and from each client at the end of the simulation will print, along with whether they match the reference lowest-cost routes. If the routes match, your implementation has passed for that simulation.  If they do not, continue debugging (using print statements and the `debugString()` method in your router classes).

The bash script `test_dv_ls.sh` will run all the supplied networks with your router implementations. You may need to run `chmod 744 test_dv_ls.sh` first to make the script executable.  You can also pass "LS" or "DV" as an argument to `test_dv_ls.sh` (e.g. `test_dv_ls.sh DV`) to test only one implementation.

As always, start early and feel free to ask questions on Piazza and in office hours.

## Acknowledgements

This programming assignment is based on Princeton University's Assignment 2 from COS 461: Computer Networks.
