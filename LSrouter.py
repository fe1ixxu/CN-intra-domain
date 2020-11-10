####################################################
# LSrouter.py
# Name: Haoran Xu, Yuwei Wan
# JHED ID: hxu64, ywan10
#####################################################

import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads
import yaml

class LSrouter(Router):
    """Link state routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        # Hints: initialize local state
        self.graph = {}
        self.seq_num = {}
        self.graph[addr] = {}
        self.seq_num[addr] = 0
        self.table = {}
        self.portdict = {}



    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        if packet.isTraceroute():
            # Hints: this is a normal data packet
            # if the forwarding table contains packet.dstAddr
            #   send packet based on forwarding table, e.g., self.send(port, packet)

            addr = packet.dstAddr
            if addr in self.table:
                while self.table[addr] != self.addr and addr != self.addr:
                    addr = self.table[addr]
                if addr in self.graph[self.addr]:
                    self.send(self.graph[self.addr][addr]["port"], packet)
        else:
            # Hints: this is a routing packet generated by your routing protocol
            # check the sequence number
            # if the sequence number is higher and the received link state is different
            #   update the local copy of the link state
            #   update the forwarding table
            #   broadcast the packet to other neighbors
            
            ifupdate = False
            content = yaml.safe_load(packet.content)
            addrs = content["add"] if content["add"] else content["reduce"]
            if addrs is not None and addrs["src"] not in self.seq_num:
                self.seq_num[addrs["src"]] = 0
            if addrs is None or content["seq_num"] <= self.seq_num[addrs["src"]]:
                self.dijkstra()
                return
            self.seq_num[addrs["src"]] = content["seq_num"]
            if addrs["src"] not in self.graph:
                self.graph[addrs["src"]] = {}

            if content["add"]: 
                self.graph[addrs["src"]] = content["info"]
            elif content["reduce"]:
                self.graph[addrs["src"]] = content["info"]
            else:
                ifupdate = True

            
            if ifupdate:
                self.dijkstra()
            else:
                for neighbor, info in self.graph[self.addr].items():
                    p = Packet(Packet.ROUTING, self.addr, neighbor, dumps(content))
                    self.send(info["port"], p)



    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # Hints:
        # update the forwarding table
        # broadcast the new link state of this router to all neighbors

        self.graph[self.addr][endpoint] = {"port": port, "cost":cost}
        self.portdict[port] = endpoint
        self.seq_num[self.addr] += 1
        content = {
        "info": self.graph[self.addr],
        "add": {"src": self.addr, "tgt": endpoint},
        "reduce": None,
        "seq_num": self.seq_num[self.addr]
        }
        content = dumps(content)
        for neighbor, info in self.graph[self.addr].items():
            p = Packet(Packet.ROUTING, self.addr, neighbor, content)
            self.send(info["port"], p)



    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        # Hints:
        # update the forwarding table
        # broadcast the new link state of this router to all neighbors

        endpoint = self.portdict.pop(port)
        self.graph[self.addr].pop(endpoint)
        self.seq_num[self.addr] += 1
        content = {
        "info": self.graph[self.addr],
        "add": None,
        "reduce": {"src": self.addr, "tgt": endpoint},
        "seq_num": self.seq_num[self.addr]
        }
        content = dumps(content)
        for neighbor, info in self.graph[self.addr].items():
            p = Packet(Packet.ROUTING, self.addr, neighbor, content)
            self.send(info["port"], p)


    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time >= self.heartbeatTime:
            self.last_time = timeMillisecs
            # Hints:
            # broadcast the link state of this router to all neighbors
            content = {
            "info": self.graph[self.addr],
            "add": None,
            "reduce": None,
            }

            content = dumps(content)
            for neighbor, info in self.graph[self.addr].items():
                p = Packet(Packet.ROUTING, self.addr, neighbor, content)
                self.send(info["port"], p)


    def graph_with_clients(self):
        G = {}
        for src_addr, info in self.graph.items():
            G[src_addr] = info
            for tgt_addr, info_d in info.items():
                if tgt_addr not in self.graph:
                    if tgt_addr not in G:
                        G[tgt_addr] = {}
                    G[tgt_addr][src_addr] = info_d
        return G


    def dijkstra(self):
        self.table = {}
        N = set()
        D = {}
        for src, info in self.graph.items():
            N.add(src)
            for des, info_d in info.items():
                N.add(des)

        for addr in N:
            if addr != self.addr:
                D[addr] = float("inf") if addr not in self.graph[self.addr] else self.graph[self.addr][addr]["cost"]
            else:
                D[addr] = 0
        G = self.graph_with_clients()

        while(len(N) != 0):
            addr = min(N, key=lambda x: D[x])
            N.remove(addr)
            for neighbor, info in G[addr].items():
                D[neighbor] = min(D[neighbor], D[addr] + info["cost"])
                if D[addr] + info["cost"] <= D[neighbor]:
                    self.table[neighbor] = addr

    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return str(self.graph) + "\n" + str(self.table) + str(len(self.graph)) + "\n" + str(self.seq_num)
