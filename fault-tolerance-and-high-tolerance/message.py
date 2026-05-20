from dataclasses import dataclass


@dataclass
class Message:
    """A message sent over the network with a sequence number for FIFO ordering."""
    payload: str
    seq_number: int
    sender_id: int
    receiver_id: int

    def __str__(self):
        return (f"Message('{self.payload}', seq={self.seq_number}, "
                f"{self.sender_id}→{self.receiver_id})")
