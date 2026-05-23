"""ANSI-colored terminal output helpers for Lamport clock simulation."""


class Colors:
    RESET     = "\033[0m"
    BOLD      = "\033[1m"
    DIM       = "\033[2m"

    RED       = "\033[31m"
    GREEN     = "\033[32m"
    YELLOW    = "\033[33m"
    BLUE      = "\033[34m"
    MAGENTA   = "\033[35m"
    CYAN      = "\033[36m"
    WHITE     = "\033[37m"
    GRAY      = "\033[90m"

    B_RED     = "\033[91m"
    B_GREEN   = "\033[92m"
    B_YELLOW  = "\033[93m"
    B_CYAN    = "\033[96m"

    BG_BLUE   = "\033[48;5;24m"
    BG_GREEN  = "\033[48;5;22m"
    BG_RED    = "\033[48;5;52m"
    BG_MAGENTA = "\033[48;5;53m"


C = Colors


# ── Layout ────────────────────────────────────────────────────────────────────

def header_box(title: str, subtitle: str = "", width: int = 62):
    print()
    print(f"  {C.B_CYAN}╔{'═' * width}╗{C.RESET}")
    print(f"  {C.B_CYAN}║{C.RESET}  {C.BOLD}{C.WHITE}{title.center(width - 4)}{C.RESET}  {C.B_CYAN}║{C.RESET}")
    if subtitle:
        print(f"  {C.B_CYAN}║{C.RESET}  {C.DIM}{subtitle.center(width - 4)}{C.RESET}  {C.B_CYAN}║{C.RESET}")
    print(f"  {C.B_CYAN}╚{'═' * width}╝{C.RESET}")
    print()


def section_header(title: str, icon: str = "▸"):
    print(f"\n  {C.B_YELLOW}{icon} {title}{C.RESET}")
    print(f"  {C.DIM}{'─' * 56}{C.RESET}\n")


def sub_section(title: str):
    print(f"\n  {C.CYAN}┌─ {title}{C.RESET}")


def network_flush_banner(count: int):
    print()
    print(f"  {C.BG_BLUE}{C.BOLD}{C.WHITE}  ⚡ NETWORK FLUSH — delivering {count} message(s) (shuffled)  {C.RESET}")
    print()


# ── Event logging ─────────────────────────────────────────────────────────────

def log_local_event(node_id: int, clock: int, description: str):
    print(f"  {C.MAGENTA}  ● LOCAL{C.RESET}   "
          f"Node {C.BOLD}{node_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} {description}  "
          f"{C.YELLOW}t={clock}{C.RESET}")


def log_send(sender_id: int, receiver_id: int, payload: str, clock: int):
    print(f"  {C.GREEN}  ↗ SEND{C.RESET}    "
          f"Node {C.BOLD}{sender_id}{C.RESET} → Node {C.BOLD}{receiver_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.WHITE}{payload}{C.RESET}'  "
          f"{C.YELLOW}t={clock}{C.RESET}")


def log_enqueue(payload: str, timestamp: int, sender_id: int, receiver_id: int):
    print(f"  {C.BLUE}  ◆ QUEUE{C.RESET}   "
          f"'{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(t={timestamp}) {sender_id}→{receiver_id}{C.RESET}")


def log_network_deliver(payload: str, timestamp: int, receiver_id: int):
    print(f"  {C.YELLOW}  ↓ WIRE{C.RESET}    "
          f"→ Node {C.BOLD}{receiver_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(t={timestamp}){C.RESET}")


def log_receive(node_id: int, sender_id: int, payload: str,
                msg_t: int, old_t: int, new_t: int):
    print(f"  {C.B_GREEN}  ✓ RECV{C.RESET}    "
          f"Node {C.BOLD}{node_id}{C.RESET} ← Node {sender_id}  "
          f"{C.DIM}│{C.RESET} '{C.BOLD}{C.WHITE}{payload}{C.RESET}'  "
          f"{C.GRAY}msg_t={msg_t}, local_t={old_t}{C.RESET} → "
          f"{C.YELLOW}{C.BOLD}t={new_t}{C.RESET}")


# ── Timeline ─────────────────────────────────────────────────────────────────

def print_timeline(node_id: int, events: list[tuple[str, int, str]]):
    """Print the event log for a node as a compact timeline."""
    print(f"  {C.CYAN}  Node {node_id} timeline:{C.RESET}")
    for event_type, clock, desc in events:
        if event_type == "LOCAL":
            color = C.MAGENTA
            icon = "●"
        elif event_type == "SEND":
            color = C.GREEN
            icon = "↗"
        else:
            color = C.B_GREEN
            icon = "✓"
        print(f"    {color}{icon} t={clock:<3}{C.RESET} {desc}")
    print()


# ── Verification ──────────────────────────────────────────────────────────────

def log_verification(description: str, checks: list[tuple[str, bool]], passed: bool):
    status = f"{C.B_GREEN}✓ PASS{C.RESET}" if passed else f"{C.B_RED}✗ FAIL{C.RESET}"
    print(f"\n  {C.CYAN}┌─ Verification: {description} {'─' * max(1, 36 - len(description))}┐{C.RESET}")
    for label, ok in checks:
        mark = f"{C.B_GREEN}✓{C.RESET}" if ok else f"{C.B_RED}✗{C.RESET}"
        print(f"  {C.CYAN}│{C.RESET}  {mark} {label}")
    print(f"  {C.CYAN}│{C.RESET}  Status: {status}")
    print(f"  {C.CYAN}└{'─' * 52}┘{C.RESET}\n")


def log_limitation(description: str, details: list[str]):
    print(f"\n  {C.BG_MAGENTA}{C.BOLD}{C.WHITE}  ⚠ LIMITATION DEMO  {C.RESET}")
    print(f"  {C.B_YELLOW}{description}{C.RESET}")
    for line in details:
        print(f"  {C.DIM}  {line}{C.RESET}")
    print()


def final_result(all_passed: bool):
    if all_passed:
        print(f"  {C.BG_GREEN}{C.BOLD}{C.WHITE}  ✓ ALL PHASES PASSED — Lamport clock working correctly!  {C.RESET}")
    else:
        print(f"  {C.BG_RED}{C.BOLD}{C.WHITE}  ✗ SOME PHASES FAILED — check output above  {C.RESET}")
    print()


# ── Space-Time Diagram ───────────────────────────────────────────────────────

def draw_space_time_diagram(event_log, node_ids, title="Space-Time Diagram"):
    """
    Render an ASCII space-time diagram in the terminal.

    event_log: list of dicts from Node._global_log
    node_ids:  list of node IDs in column order (left to right)
    """
    n = len(node_ids)
    COL_SPACING = 24
    FIRST_COL = 12
    node_pos = {nid: FIRST_COL + i * COL_SPACING for i, nid in enumerate(node_ids)}
    TOTAL_W = FIRST_COL + (n - 1) * COL_SPACING + 22

    # ── Process log: pair sends with their matching receives ──
    entries = []
    pending_sends = {}   # (payload, sender, target) → event dict

    for event in event_log:
        if event['type'] == 'local':
            entries.append(event)
        elif event['type'] == 'send':
            key = (event['payload'], event['node'], event['target'])
            pending_sends[key] = event
        elif event['type'] == 'recv':
            key = (event['payload'], event['source'], event['node'])
            if key in pending_sends:
                send_evt = pending_sends.pop(key)
                entries.append({
                    'type': 'msg',
                    'from': send_evt['node'],
                    'to': event['node'],
                    'send_t': send_evt['clock'],
                    'recv_t': event['clock'],
                    'payload': event['payload'],
                })

    # ── Canvas helpers ──

    def make_row():
        """Create a blank row with │ at each node position."""
        chars = [' '] * TOTAL_W
        colors = [None] * TOTAL_W
        for nid in node_ids:
            p = node_pos[nid]
            if p < TOTAL_W:
                chars[p] = '│'
                colors[p] = C.DIM
        return chars, colors

    def place(chars, colors, pos, text, color=None):
        """Place text at position, overwriting characters."""
        for j, ch in enumerate(text):
            p = pos + j
            if 0 <= p < TOTAL_W:
                chars[p] = ch
                colors[p] = color

    def render(chars, colors):
        """Convert char + color arrays into a single ANSI string."""
        parts = []
        prev = "SENTINEL"
        for i in range(len(chars)):
            col = colors[i]
            if col != prev:
                if prev is not None and prev != "SENTINEL":
                    parts.append(C.RESET)
                if col is not None:
                    parts.append(col)
                prev = col
            parts.append(chars[i])
        if prev is not None and prev != "SENTINEL":
            parts.append(C.RESET)
        return '  ' + ''.join(parts).rstrip()

    # ── Header ──
    print(f"\n  {C.CYAN}┌─ {title}{C.RESET}")

    hdr_c, hdr_col = [' '] * TOTAL_W, [None] * TOTAL_W
    for nid in node_ids:
        label = f"Node {nid}"
        pos = node_pos[nid] - len(label) // 2
        place(hdr_c, hdr_col, pos, label, C.BOLD)
    print(render(hdr_c, hdr_col))

    print(render(*make_row()))

    # ── Render each entry ──
    for entry in entries:
        chars, colors = make_row()

        if entry['type'] == 'local':
            nid = entry['node']
            pos = node_pos[nid]
            clock = entry['clock']
            desc = entry.get('desc', '')

            # ● marker at node position
            chars[pos] = '●'
            colors[pos] = C.MAGENTA

            # Clock label to the left of ●
            clock_str = f"t={clock}"
            place(chars, colors, pos - len(clock_str) - 1, clock_str, C.YELLOW)

            # Description to the right of ●
            place(chars, colors, pos + 2, desc, None)

            # Restore other nodes' │
            for other in node_ids:
                if other != nid:
                    p = node_pos[other]
                    if p < TOTAL_W:
                        chars[p] = '│'
                        colors[p] = C.DIM

        elif entry['type'] == 'msg':
            from_pos = node_pos[entry['from']]
            to_pos = node_pos[entry['to']]
            left = min(from_pos, to_pos)
            right = max(from_pos, to_pos)
            going_right = from_pos < to_pos

            # ● at sender position
            chars[from_pos] = '●'
            colors[from_pos] = C.GREEN

            # Fill ─ between sender and receiver
            for p in range(left + 1, right):
                chars[p] = '─'
                colors[p] = C.DIM

            # Arrow head at receiver
            chars[to_pos] = '▶' if going_right else '◀'
            colors[to_pos] = C.B_CYAN

            # Payload label centered in the arrow
            payload_str = f" '{entry['payload']}' "
            mid = (left + right) // 2 - len(payload_str) // 2
            place(chars, colors, max(left + 1, mid), payload_str, C.WHITE)

            # Send clock label
            send_label = f"t={entry['send_t']}"
            if going_right:
                place(chars, colors, from_pos - len(send_label) - 1,
                      send_label, C.YELLOW)
            else:
                place(chars, colors, from_pos + 2, send_label, C.YELLOW)

            # Recv clock label
            recv_label = f"t={entry['recv_t']}"
            if going_right:
                place(chars, colors, to_pos + 2, recv_label, C.YELLOW)
            else:
                place(chars, colors, to_pos - len(recv_label) - 1,
                      recv_label, C.YELLOW)

            # Uninvolved intermediate nodes: ┼ if arrow crosses, │ otherwise
            for nid in node_ids:
                p = node_pos[nid]
                if nid != entry['from'] and nid != entry['to']:
                    if left < p < right:
                        chars[p] = '┼'
                        colors[p] = C.DIM
                    elif p < TOTAL_W:
                        chars[p] = '│'
                        colors[p] = C.DIM

        print(render(chars, colors))
        print(render(*make_row()))

    print()
