"""
Simulates a reliable but unordered point-to-point link.

The network guarantees:
  - Reliability: no messages are ever dropped
  - NO ordering: messages may be delivered in any order

This is the "unreliable ordering" layer that the FIFO algorithm sits on top of.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from message import Message
import visuals

if TYPE_CHECKING:
    from node import Node


class Network:

    def __init__(self):
        self.queue: list[Message] = []
        self.nodes: dict[int, "Node"] = {}

    def register(self, node):
        """Register a node so the network knows where to deliver messages."""
        self.nodes[node.node_id] = node

    def enqueue(self, msg: Message):
        """Accept a message for later delivery."""
        self.queue.append(msg)
        visuals.log_enqueue(msg.payload, msg.seq_number, msg.sender_id, msg.receiver_id)

    def flush(self):
        """
        Deliver all queued messages in RANDOM order.
        This simulates the reliable link's reordering property.
        """
        random.shuffle(self.queue)
        visuals.network_flush_banner(len(self.queue))

        for msg in self.queue:
            visuals.log_network_deliver(msg.payload, msg.seq_number, msg.receiver_id)
            target = self.nodes[msg.receiver_id]
            target.on_receive(msg)

        self.queue.clear()
