import os

class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    WHITE = '\033[97m'
    CYAN = '\033[36m'
    B_CYAN = '\033[96m'
    MAGENTA = '\033[35m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'

def section_header(title: str, icon: str = "•"):
    print(f"\n  {icon} {C.BOLD}{title}{C.RESET}")
    print(f"  {C.DIM}{'─' * 56}{C.RESET}\n")

def format_vector(v: list[int]) -> str:
    return f"[{','.join(map(str, v))}]"

def draw_space_time_diagram(event_log, node_ids, title="Space-Time Diagram"):
    """
    Render an ASCII space-time diagram in the terminal with vector clocks.

    event_log: list of dicts from Node._global_log
    node_ids:  list of node IDs in column order (left to right)
    """
    n = len(node_ids)
    COL_SPACING = 30 # extra space for vectors like [1,2,3]
    FIRST_COL = 14
    node_pos = {nid: FIRST_COL + i * COL_SPACING for i, nid in enumerate(node_ids)}
    TOTAL_W = FIRST_COL + (n - 1) * COL_SPACING + 28

    # ── Process log: pair sends with their matching receives ──
    entries = []
    pending_sends = {}

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
                    'send_v': send_evt['vector'],
                    'recv_v': event['vector'],
                    'payload': event['payload'],
                })

    # ── Canvas helpers ──

    def make_row():
        chars = [' '] * TOTAL_W
        colors = [None] * TOTAL_W
        for nid in node_ids:
            p = node_pos[nid]
            if p < TOTAL_W:
                chars[p] = '│'
                colors[p] = C.DIM
        return chars, colors

    def place(chars, colors, pos, text, color=None):
        for j, ch in enumerate(text):
            p = pos + j
            if 0 <= p < TOTAL_W:
                chars[p] = ch
                colors[p] = color

    def render(chars, colors):
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
    print(f"  {C.CYAN}┌─ {title}{C.RESET}")

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
            vec_str = format_vector(entry['vector'])
            desc = entry.get('desc', '')

            chars[pos] = '●'
            colors[pos] = C.MAGENTA

            place(chars, colors, pos - len(vec_str) - 1, vec_str, C.YELLOW)
            place(chars, colors, pos + 2, desc, None)

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

            chars[from_pos] = '●'
            colors[from_pos] = C.GREEN

            for p in range(left + 1, right):
                chars[p] = '─'
                colors[p] = C.DIM

            chars[to_pos] = '▶' if going_right else '◀'
            colors[to_pos] = C.B_CYAN

            payload_str = f" '{entry['payload']}' "
            mid = (left + right) // 2 - len(payload_str) // 2
            place(chars, colors, max(left + 1, mid), payload_str, C.WHITE)

            send_v = format_vector(entry['send_v'])
            recv_v = format_vector(entry['recv_v'])
            
            if going_right:
                place(chars, colors, from_pos - len(send_v) - 1, send_v, C.YELLOW)
                place(chars, colors, to_pos + 2, recv_v, C.YELLOW)
            else:
                place(chars, colors, from_pos + 2, send_v, C.YELLOW)
                place(chars, colors, to_pos - len(recv_v) - 1, recv_v, C.YELLOW)

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

def final_result(all_passed: bool):
    if all_passed:
        print(f"  {C.BG_GREEN}{C.BOLD}{C.WHITE}  ✓ ALL PHASES PASSED — Vector clock working correctly!  {C.RESET}")
    else:
        print(f"  {C.BG_RED}{C.BOLD}{C.WHITE}  ✗ SOME PHASES FAILED — check output above  {C.RESET}")
    print()
