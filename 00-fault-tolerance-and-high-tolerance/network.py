"""Reliable but unordered point-to-point link (shuffles messages on flush)."""

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
        self.nodes[node.node_id] = node

    def enqueue(self, msg: Message):
        self.queue.append(msg)
        visuals.log_enqueue(msg.payload, msg.seq_number, msg.sender_id, msg.receiver_id)

    def flush(self):
        """Deliver all queued messages in random order."""
        random.shuffle(self.queue)
        visuals.network_flush_banner(len(self.queue))

        for msg in self.queue:
            visuals.log_network_deliver(msg.payload, msg.seq_number, msg.receiver_id)
            self.nodes[msg.receiver_id].on_receive(msg)

        self.queue.clear()
