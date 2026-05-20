"""
FIFO Link Simulation
====================
Demonstrates how to build a FIFO (ordered) link on top of a
reliable but unordered point-to-point network.

Exercise 4 from Martin Kleppmann's Distributed Systems course.

Usage:
    python main.py
"""

import random
from message import Message
from network import Network
from node import Node
import visuals


def phase_one(network: Network, node_a: Node, node_b: Node) -> bool:
    """Unidirectional: A sends 5 messages to B."""
    visuals.section_header("Phase 1 · Unidirectional  (A → B)", icon="①")

    messages = ["hello", "how", "are", "you", "?"]
    for payload in messages:
        node_a.fifo_send(payload, receiver_id=2)

    network.flush()

    delivered = [m.payload for m in node_b.delivered]
    passed = delivered == messages
    visuals.log_verification(messages, delivered, passed)
    return passed


def phase_two(network: Network) -> bool:
    """Bidirectional: A sends pings, B receives them, then B replies with pongs."""
    visuals.section_header("Phase 2 · Bidirectional  (A ↔ B)", icon="②")

    # Fresh nodes so seq counters start at 1
    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # Step 1: Node A sends pings to Node B
    visuals.sub_section("Step 1: Node A sends pings")
    node_a.fifo_send("ping-1", receiver_id=2)
    node_a.fifo_send("ping-2", receiver_id=2)
    network.flush()

    # Step 2: Node B received the pings, now replies with pongs
    visuals.sub_section("Step 2: Node B replies with pongs")
    node_b.fifo_send("pong-1", receiver_id=1)
    node_b.fifo_send("pong-2", receiver_id=1)
    network.flush()

    a_delivered = [m.payload for m in node_a.delivered]
    b_delivered = [m.payload for m in node_b.delivered]
    a_expected = ["pong-1", "pong-2"]
    b_expected = ["ping-1", "ping-2"]
    passed = (a_delivered == a_expected) and (b_delivered == b_expected)
    visuals.log_bidirectional_verification(
        a_delivered, a_expected, b_delivered, b_expected, passed
    )
    return passed


def phase_three(network: Network) -> bool:
    """Multiple flushes: seq counters persist across rounds."""
    visuals.section_header("Phase 3 · Multiple Flushes  (persistent seq)", icon="③")

    # Fresh nodes so seq counters start at 1
    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # Batch 1
    visuals.sub_section("Batch 1")
    node_a.fifo_send("batch1-msg1", receiver_id=2)
    node_a.fifo_send("batch1-msg2", receiver_id=2)
    network.flush()

    # Batch 2 — seq counters continue (seq=3, 4)
    visuals.sub_section("Batch 2")
    node_a.fifo_send("batch2-msg1", receiver_id=2)
    node_a.fifo_send("batch2-msg2", receiver_id=2)
    network.flush()

    delivered = [m.payload for m in node_b.delivered]
    expected = ["batch1-msg1", "batch1-msg2", "batch2-msg1", "batch2-msg2"]
    passed = delivered == expected
    visuals.log_verification(expected, delivered, passed)
    return passed


def main():
    visuals.header_box(
        "FIFO LINK SIMULATION",
        "reliable unordered link  →  FIFO ordered delivery"
    )

    random.seed(42)

    # Setup
    network = Network()
    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # Run phases
    results = [
        phase_one(network, node_a, node_b),
        phase_two(network),
        phase_three(network),
    ]

    visuals.final_result(all(results))


if __name__ == "__main__":
    main()
