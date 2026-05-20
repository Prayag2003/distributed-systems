"""
A node that implements FIFO links on top of a reliable unordered network.

Algorithm (from Kleppmann's distributed systems course):

  Sender side:
    - Maintain an incrementing sequence number per receiver
    - Tag every outgoing message with the next seq number

  Receiver side:
    - Buffer incoming messages by (sender, seq_number)
    - Only deliver when the next expected seq number is available
    - Deliver consecutively while the buffer has the next seq
"""

from collections import defaultdict
from message import Message
from network import Network
import visuals


class Node:

    def __init__(self, node_id: int, network: Network):
        self.node_id = node_id
        self.network = network

        # ── Sender state (per receiver) ──
        self.send_seq: dict[int, int] = defaultdict(lambda: 0)

        # ── Receiver state (per sender) ──
        self.recv_buffer: dict[int, dict[int, Message]] = defaultdict(dict)
        self.next_deliver: dict[int, int] = defaultdict(lambda: 1)

        # ── Delivered log (for verification) ──
        self.delivered: list[Message] = []

        # Register with the network
        network.register(self)

    def fifo_send(self, payload: str, receiver_id: int):
        """
        Send a message with FIFO guarantees.
        Assigns a monotonically increasing sequence number per receiver.
        """
        self.send_seq[receiver_id] += 1
        seq = self.send_seq[receiver_id]

        msg = Message(
            payload=payload,
            seq_number=seq,
            sender_id=self.node_id,
            receiver_id=receiver_id,
        )

        visuals.log_send(self.node_id, receiver_id, payload, seq)
        self.network.enqueue(msg)

    def on_receive(self, msg: Message):
        """
        Called by the network when a message arrives.
        Buffers out-of-order messages and delivers in sequence order.
        """
        sender = msg.sender_id
        seq = msg.seq_number

        # Buffer the incoming message
        self.recv_buffer[sender][seq] = msg
        visuals.log_buffer(self.node_id, msg.payload, seq, sender, self.next_deliver[sender])

        # Deliver as many consecutive in-order messages as possible
        while self.next_deliver[sender] in self.recv_buffer[sender]:
            next_seq = self.next_deliver[sender]
            delivered_msg = self.recv_buffer[sender].pop(next_seq)
            self.delivered.append(delivered_msg)
            self.next_deliver[sender] += 1
            visuals.log_fifo_deliver(self.node_id, delivered_msg.payload, next_seq)
