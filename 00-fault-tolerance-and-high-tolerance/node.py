"""FIFO node: seq numbering on send, buffered in-order delivery on receive."""

from collections import defaultdict
from message import Message
from network import Network
import visuals


class Node:

    def __init__(self, node_id: int, network: Network):
        self.node_id = node_id
        self.network = network

        self.send_seq: dict[int, int] = defaultdict(lambda: 0)          # per receiver
        self.recv_buffer: dict[int, dict[int, Message]] = defaultdict(dict)  # per sender
        self.next_deliver: dict[int, int] = defaultdict(lambda: 1)       # per sender

        self.delivered: list[Message] = []  # log for verification

        network.register(self)

    def fifo_send(self, payload: str, receiver_id: int):
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
        """Buffer out-of-order messages, deliver in sequence order."""
        sender = msg.sender_id
        seq = msg.seq_number

        self.recv_buffer[sender][seq] = msg
        visuals.log_buffer(self.node_id, msg.payload, seq, sender, self.next_deliver[sender])

        # Deliver consecutive in-order messages
        while self.next_deliver[sender] in self.recv_buffer[sender]:
            next_seq = self.next_deliver[sender]
            delivered_msg = self.recv_buffer[sender].pop(next_seq)
            self.delivered.append(delivered_msg)
            self.next_deliver[sender] += 1
            visuals.log_fifo_deliver(self.node_id, delivered_msg.payload, next_seq)
