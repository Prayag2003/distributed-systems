from dataclasses import dataclass


@dataclass
class Message:
    payload: str
    sender_id: int
    receiver_id: int
    timestamp: int          # sender's Lamport clock at send time

    def __str__(self):
        return f"Message('{self.payload}', t={self.timestamp}, {self.sender_id}→{self.receiver_id})"
