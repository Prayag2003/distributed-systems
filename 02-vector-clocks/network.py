"""Reliable but unordered point-to-point link (shuffles messages on flush)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from message import Message

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

    def flush(self):
        """Deliver all queued messages in random order (silently)."""
        random.shuffle(self.queue)
        for msg in self.queue:
            self.nodes[msg.receiver_id].on_receive(msg)
        self.queue.clear()
