from dataclasses import dataclass


@dataclass
class Message:
    payload: str
    seq_number: int
    sender_id: int
    receiver_id: int

    def __str__(self):
        return f"Message('{self.payload}', seq={self.seq_number}, {self.sender_id}→{self.receiver_id})"
