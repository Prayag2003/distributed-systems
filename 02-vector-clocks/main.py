import sys
import visuals
from network import Network
from node import Node
from visuals import C

def format_vector(v):
    return f"[{','.join(map(str, v))}]"

def print_causality_box(title, checks):
    print(f"  {C.CYAN}┌─ Verification: {title} {'─' * max(0, 36 - len(title))}┐{C.RESET}")
    all_pass = True
    for desc, condition in checks:
        if condition:
            print(f"  {C.CYAN}│{C.RESET}  {C.GREEN}✓{C.RESET} {desc}")
        else:
            print(f"  {C.CYAN}│{C.RESET}  {C.RED}✗{C.RESET} {desc}")
            all_pass = False
    
    status = f"{C.GREEN}✓ PASS{C.RESET}" if all_pass else f"{C.RED}✗ FAIL{C.RESET}"
    print(f"  {C.CYAN}│{C.RESET}  Status: {status}")
    print(f"  {C.CYAN}└{'─'*52}┘{C.RESET}\n")
    return all_pass

def phase_one(network: Network) -> bool:
    visuals.section_header("Phase 1 · Simple Exchange (A ↔ B)", icon="①")
    Node.clear_log()
    node_a = Node(node_id=1, node_count=2, network=network)
    node_b = Node(node_id=2, node_count=2, network=network)

    node_a.local_event("database write")
    node_a.send("hello", receiver_id=2)
    network.flush()

    node_b.local_event("process request")
    node_b.send("world", receiver_id=1)
    network.flush()

    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    v_a_send = node_a.events[1][1]
    v_b_recv = node_b.events[0][1] 
    v_b_send = node_b.events[2][1] 
    v_a_recv = node_a.events[2][1]

    checks = [
        (f"V(A sends)={format_vector(v_a_send)} → V(B recvs)={format_vector(v_b_recv)}", Node.happens_before(v_a_send, v_b_recv)),
        (f"V(B sends)={format_vector(v_b_send)} → V(A recvs)={format_vector(v_a_recv)}", Node.happens_before(v_b_send, v_a_recv)),
    ]
    return print_causality_box("send → receive invariant", checks)

def phase_two(network: Network) -> bool:
    visuals.section_header("Phase 2 · Concurrent Sends (A ↔ B)", icon="②")
    Node.clear_log()
    node_a = Node(node_id=1, node_count=2, network=network)
    node_b = Node(node_id=2, node_count=2, network=network)

    node_a.send("ping", receiver_id=2)
    node_b.send("pong", receiver_id=1)
    network.flush()

    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    v_a_send = node_a.events[0][1]
    v_b_send = node_b.events[0][1]

    checks = [
        (f"V(A sends ping)={format_vector(v_a_send)} ∥ V(B sends pong)={format_vector(v_b_send)}", Node.is_concurrent(v_a_send, v_b_send))
    ]
    return print_causality_box("concurrent sends", checks)

def phase_three(network: Network) -> bool:
    visuals.section_header("Phase 3 · Causal Chain (A → B → C)", icon="③")
    Node.clear_log()
    node_a = Node(node_id=1, node_count=3, network=network)
    node_b = Node(node_id=2, node_count=3, network=network)
    node_c = Node(node_id=3, node_count=3, network=network)

    node_a.local_event("prepare data")
    node_a.send("data", receiver_id=2)
    network.flush()

    node_b.local_event("process data")
    node_b.send("forwarded-data", receiver_id=3)
    network.flush()

    visuals.draw_space_time_diagram(Node.get_log(), [1, 2, 3])

    v_a_send = node_a.events[1][1]
    v_c_recv = node_c.events[0][1]

    checks = [
        (f"Transitive: V(A sends)={format_vector(v_a_send)} → V(C recvs)={format_vector(v_c_recv)}", Node.happens_before(v_a_send, v_c_recv))
    ]
    return print_causality_box("causal chain transitivity", checks)

def phase_four() -> bool:
    visuals.section_header("Phase 4 · Solving Lamport's Limitation", icon="④")
    Node.clear_log()
    network = Network()
    node_a = Node(node_id=1, node_count=2, network=network)
    node_b = Node(node_id=2, node_count=2, network=network)

    node_a.local_event("write-x")
    node_a.local_event("write-y")
    node_b.local_event("write-z")

    visuals.draw_space_time_diagram(Node.get_log(), [1, 2])

    v_a_write_y = node_a.events[1][1]
    v_b_write_z = node_b.events[0][1]

    print("    ⚠ LAMPORT LIMITATION SOLVED")
    print(f"    V(A:write-y) = {format_vector(v_a_write_y)}")
    print(f"    V(B:write-z) = {format_vector(v_b_write_z)}")
    print("    Because neither vector is strictly ≤ the other in all dimensions,")
    print("    Vector clocks correctly identify these events as CONCURRENT!\n")

    checks = [
        ("Neither V(A) → V(B) nor V(B) → V(A)", not Node.happens_before(v_a_write_y, v_b_write_z) and not Node.happens_before(v_b_write_z, v_a_write_y)),
        (f"V(A:write-y) ∥ V(B:write-z)", Node.is_concurrent(v_a_write_y, v_b_write_z))
    ]
    return print_causality_box("detecting concurrency", checks)

def main():
    print(f"\n  {C.CYAN}╔{'═' * 62}╗{C.RESET}")
    print(f"  {C.CYAN}║{C.RESET}                   {C.BOLD}VECTOR CLOCK SIMULATION{C.RESET}                    {C.CYAN}║{C.RESET}")
    print(f"  {C.CYAN}║{C.RESET}        vector timestamps  ·  causality & concurrency        {C.CYAN}║{C.RESET}")
    print(f"  {C.CYAN}╚{'═' * 62}╝{C.RESET}\n")

    net1 = Network()
    p1 = phase_one(net1)

    net2 = Network()
    p2 = phase_two(net2)

    net3 = Network()
    p3 = phase_three(net3)

    p4 = phase_four()

    all_passed = p1 and p2 and p3 and p4
    visuals.final_result(all_passed)

if __name__ == "__main__":
    main()
