from dataclasses import dataclass


@dataclass
class Message:
    payload: str
    sender_id: int
    receiver_id: int
    vector_clock: list[int]     # copy of sender's vector at send time

    def __str__(self):
        return f"Message('{self.payload}', V={self.vector_clock}, {self.sender_id}→{self.receiver_id})"
