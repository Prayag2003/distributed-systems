"""
Lamport Clock Simulation
========================
Demonstrates the Lamport logical clock algorithm across multiple
scenarios, including its key limitation (cannot detect concurrency).

Exercise from Martin Kleppmann's Distributed Systems course,
Chapter 4: Broadcast Protocols and Logical Time.

Usage:
    python main.py
"""

import random
from network import Network
from node import Node
import visuals


def phase_one(network: Network) -> bool:
    """Simple exchange between 2 nodes: A local → A send → B recv → B local → B send → A recv."""
    visuals.section_header("Phase 1 · Simple Exchange  (A ↔ B)", icon="①")
    Node.clear_log()

    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # A does a local event, then sends to B
    visuals.sub_section("Step 1: Node A — local event, then send to B")
    node_a.local_event("database write")
    node_a.send("hello", receiver_id=2)
    network.flush()

    # B does a local event, then replies to A
    visuals.sub_section("Step 2: Node B — local event, then reply to A")
    node_b.local_event("process request")
    node_b.send("world", receiver_id=1)
    network.flush()

    # Space-time diagram
    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    # Verify: every send timestamp < corresponding receive timestamp
    # A sent "hello" at t=2, B received it → B's recv clock must be > 2
    a_send_t = node_a.events[1][1]   # SEND "hello"
    b_recv_t = node_b.events[0][1]   # RECV "hello"
    b_send_t = node_b.events[2][1]   # SEND "world"
    a_recv_t = node_a.events[2][1]   # RECV "world"

    checks = [
        (f"T(A sends 'hello')={a_send_t}  <  T(B recvs 'hello')={b_recv_t}", a_send_t < b_recv_t),
        (f"T(B sends 'world')={b_send_t}  <  T(A recvs 'world')={a_recv_t}", b_send_t < a_recv_t),
    ]
    passed = all(ok for _, ok in checks)
    visuals.log_verification("send < receive invariant", checks, passed)
    return passed


def phase_two(network: Network) -> bool:
    """Concurrent sends: A and B both send before either receives."""
    visuals.section_header("Phase 2 · Concurrent Sends  (A ↔ B)", icon="②")
    Node.clear_log()

    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # Both nodes send before any delivery
    visuals.sub_section("Both nodes send simultaneously")
    node_a.send("ping", receiver_id=2)
    node_b.send("pong", receiver_id=1)
    network.flush()

    # Space-time diagram
    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    # Verify: for each message, send_t < recv_t
    a_send_t = node_a.events[0][1]   # SEND "ping"
    b_recv_t = node_b.events[1][1]   # RECV "ping"  (after B's own send)
    b_send_t = node_b.events[0][1]   # SEND "pong"
    a_recv_t = node_a.events[1][1]   # RECV "pong"

    checks = [
        (f"T(A sends 'ping')={a_send_t}  <  T(B recvs 'ping')={b_recv_t}", a_send_t < b_recv_t),
        (f"T(B sends 'pong')={b_send_t}  <  T(A recvs 'pong')={a_recv_t}", b_send_t < a_recv_t),
    ]
    passed = all(ok for _, ok in checks)
    visuals.log_verification("send < receive on concurrent sends", checks, passed)
    return passed


def phase_three(network: Network) -> bool:
    """Three-node causal chain: A → B → C. Verify transitivity."""
    visuals.section_header("Phase 3 · Causal Chain  (A → B → C)", icon="③")
    Node.clear_log()

    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)
    node_c = Node(node_id=3, network=network)

    # A sends to B
    visuals.sub_section("Step 1: A → B")
    node_a.local_event("prepare data")
    node_a.send("data", receiver_id=2)
    network.flush()

    # B processes and forwards to C
    visuals.sub_section("Step 2: B → C (forwarding)")
    node_b.local_event("process data")
    node_b.send("forwarded-data", receiver_id=3)
    network.flush()

    # Space-time diagram
    visuals.draw_space_time_diagram(Node.get_log(), [1, 2, 3])

    # Verify transitivity: T(A_send) < T(B_recv) < T(B_send) < T(C_recv)
    a_send_t = node_a.events[1][1]   # SEND "data"
    b_recv_t = node_b.events[0][1]   # RECV "data"
    b_send_t = node_b.events[2][1]   # SEND "forwarded-data"
    c_recv_t = node_c.events[0][1]   # RECV "forwarded-data"

    checks = [
        (f"T(A send)={a_send_t}  <  T(B recv)={b_recv_t}", a_send_t < b_recv_t),
        (f"T(B recv)={b_recv_t}  <  T(B send)={b_send_t}", b_recv_t < b_send_t),
        (f"T(B send)={b_send_t}  <  T(C recv)={c_recv_t}", b_send_t < c_recv_t),
        (f"Transitive: T(A send)={a_send_t}  <  T(C recv)={c_recv_t}", a_send_t < c_recv_t),
    ]
    passed = all(ok for _, ok in checks)
    visuals.log_verification("causal chain transitivity", checks, passed)
    return passed


def phase_four() -> bool:
    """Demonstrate the limitation: Lamport clocks cannot detect concurrency."""
    visuals.section_header("Phase 4 · Limitation  (cannot detect concurrency)", icon="④")
    Node.clear_log()

    network = Network()
    node_a = Node(node_id=1, network=network)
    node_b = Node(node_id=2, network=network)

    # Both nodes do local events independently — no communication
    visuals.sub_section("Independent local events (no messages exchanged)")
    node_a.local_event("write-x")
    node_a.local_event("write-y")
    node_b.local_event("write-z")

    # Space-time diagram
    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    # A has t=1,2 and B has t=1 — Lamport says T(A:write-y)=2 > T(B:write-z)=1
    # but these events are actually CONCURRENT (no causal relationship)
    a_event_t = node_a.events[1][1]  # write-y, t=2
    b_event_t = node_b.events[0][1]  # write-z, t=1

    visuals.log_limitation(
        "Lamport clocks assign T(A:write-y)=2 > T(B:write-z)=1,\n"
        "  but these events are actually CONCURRENT (no causal link)!",
        [
            f"T(A:write-y) = {a_event_t}",
            f"T(B:write-z) = {b_event_t}",
            f"Lamport ordering: A:write-y > B:write-z  (misleading!)",
            "",
            "Lamport clocks guarantee:  a → b  ⟹  T(a) < T(b)",
            "But NOT the converse:      T(a) < T(b)  ⟹  a → b  (FALSE!)",
            "",
            "→ This is why we need VECTOR CLOCKS (Exercise 02)",
        ]
    )

    # This phase always passes — it's a demonstration, not a correctness check
    checks = [
        (f"Events are concurrent (no messages exchanged)", True),
        (f"Lamport assigns T(A:write-y)={a_event_t} > T(B:write-z)={b_event_t} anyway", a_event_t > b_event_t),
        (f"Cannot distinguish from causal ordering — limitation confirmed", True),
    ]
    passed = all(ok for _, ok in checks)
    visuals.log_verification("limitation demonstration", checks, passed)
    return passed


def main():
    visuals.header_box(
        "LAMPORT CLOCK SIMULATION",
        "logical timestamps  ·  happens-before ordering"
    )

    random.seed(42)

    network = Network()

    results = [
        phase_one(network),
        phase_two(network),
        phase_three(network),
        phase_four(),
    ]

    visuals.final_result(all(results))


if __name__ == "__main__":
    main()
