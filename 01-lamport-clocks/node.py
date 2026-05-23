"""Lamport clock node: t++ on local/send, max(t, msg.t)+1 on receive."""

from message import Message
from network import Network
import visuals


class Node:

    # ── Global event log (for space-time diagram rendering) ───────────
    _global_log: list = []
    _log_seq: int = 0

    @classmethod
    def clear_log(cls):
        """Reset the global event log (call at the start of each phase)."""
        cls._global_log = []
        cls._log_seq = 0

    @classmethod
    def get_log(cls):
        """Return a copy of the global event log."""
        return list(cls._global_log)

    # ── Instance ──────────────────────────────────────────────────────

    def __init__(self, node_id: int, network: Network):
        self.node_id = node_id
        self.network = network
        self.clock: int = 0                           # Lamport timestamp

        # Event log: list of (event_type, clock_value, description)
        self.events: list[tuple[str, int, str]] = []

        network.register(self)

    # ── Lamport clock rules ───────────────────────────────────────────────

    def local_event(self, description: str = "local event"):
        """On local event: t ← t + 1."""
        self.clock += 1
        self.events.append(("LOCAL", self.clock, description))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'local', 'node': self.node_id,
            'clock': self.clock, 'desc': description,
            'order': Node._log_seq,
        })
        visuals.log_local_event(self.node_id, self.clock, description)

    def send(self, payload: str, receiver_id: int):
        """On send: t ← t + 1, attach t to the message."""
        self.clock += 1

        msg = Message(
            payload=payload,
            sender_id=self.node_id,
            receiver_id=receiver_id,
            timestamp=self.clock,
        )

        self.events.append(("SEND", self.clock, f"'{payload}' → Node {receiver_id}"))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'send', 'node': self.node_id,
            'target': receiver_id, 'clock': self.clock,
            'payload': payload, 'order': Node._log_seq,
        })
        visuals.log_send(self.node_id, receiver_id, payload, self.clock)
        self.network.enqueue(msg)

    def on_receive(self, msg: Message):
        """On receive: t ← max(t, msg.t) + 1."""
        old_t = self.clock
        self.clock = max(self.clock, msg.timestamp) + 1

        self.events.append(("RECV", self.clock, f"'{msg.payload}' from Node {msg.sender_id}"))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'recv', 'node': self.node_id,
            'source': msg.sender_id, 'clock': self.clock,
            'msg_clock': msg.timestamp, 'payload': msg.payload,
            'order': Node._log_seq,
        })
        visuals.log_receive(self.node_id, msg.sender_id, msg.payload,
                            msg.timestamp, old_t, self.clock)
