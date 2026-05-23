"""Vector clock node: V[i]++ on event, merge + V[i]++ on receive."""

from message import Message
from network import Network


class Node:

    # ── Global event log (for space-time diagram) ─────────────────────
    _global_log: list = []
    _log_seq: int = 0

    @classmethod
    def clear_log(cls):
        cls._global_log = []
        cls._log_seq = 0

    @classmethod
    def get_log(cls):
        return list(cls._global_log)

    # ── Instance ──────────────────────────────────────────────────────

    def __init__(self, node_id: int, node_count: int, network: Network):
        self.node_id = node_id
        self.index = node_id - 1                    # 0-indexed position in vector
        self.node_count = node_count
        self.network = network
        self.vector: list[int] = [0] * node_count

        # Per-node event log: (event_type, vector_snapshot, description)
        self.events: list[tuple[str, list[int], str]] = []

        network.register(self)

    # ── Vector clock rules ────────────────────────────────────────────

    def local_event(self, description: str = "local event"):
        """On local event: V[i] ← V[i] + 1."""
        self.vector[self.index] += 1
        v = list(self.vector)
        self.events.append(("LOCAL", v, description))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'local', 'node': self.node_id,
            'vector': v, 'desc': description,
            'order': Node._log_seq,
        })

    def send(self, payload: str, receiver_id: int):
        """On send: V[i] ← V[i] + 1, attach copy of V."""
        self.vector[self.index] += 1
        v = list(self.vector)

        msg = Message(
            payload=payload,
            sender_id=self.node_id,
            receiver_id=receiver_id,
            vector_clock=list(self.vector),
        )

        self.events.append(("SEND", v, f"'{payload}' → Node {receiver_id}"))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'send', 'node': self.node_id,
            'target': receiver_id, 'vector': v,
            'payload': payload, 'order': Node._log_seq,
        })
        self.network.enqueue(msg)

    def on_receive(self, msg: Message):
        """On receive: V[j] ← max(V[j], msg.V[j]) ∀j, then V[i] ← V[i] + 1."""
        for j in range(self.node_count):
            self.vector[j] = max(self.vector[j], msg.vector_clock[j])
        self.vector[self.index] += 1
        v = list(self.vector)

        self.events.append(("RECV", v, f"'{msg.payload}' from Node {msg.sender_id}"))
        Node._log_seq += 1
        Node._global_log.append({
            'type': 'recv', 'node': self.node_id,
            'source': msg.sender_id, 'vector': v,
            'msg_vector': list(msg.vector_clock),
            'payload': msg.payload, 'order': Node._log_seq,
        })

    # ── Comparison helpers ────────────────────────────────────────────

    @staticmethod
    def happens_before(v1: list[int], v2: list[int]) -> bool:
        """v1 → v2: v1[i] ≤ v2[i] for all i, and v1 ≠ v2."""
        return all(a <= b for a, b in zip(v1, v2)) and v1 != v2

    @staticmethod
    def is_concurrent(v1: list[int], v2: list[int]) -> bool:
        """v1 ∥ v2: neither v1 → v2 nor v2 → v1 (and v1 ≠ v2)."""
        return (not Node.happens_before(v1, v2)
                and not Node.happens_before(v2, v1)
                and v1 != v2)
