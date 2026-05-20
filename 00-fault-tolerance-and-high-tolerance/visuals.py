"""
Pretty terminal output helpers using ANSI colors and box-drawing characters.
"""


# ── ANSI Color Codes ──────────────────────────────────────────────────────────

class Colors:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"

    # Foreground
    RED        = "\033[31m"
    GREEN      = "\033[32m"
    YELLOW     = "\033[33m"
    BLUE       = "\033[34m"
    MAGENTA    = "\033[35m"
    CYAN       = "\033[36m"
    WHITE      = "\033[37m"
    GRAY       = "\033[90m"

    # Bright foreground
    B_RED      = "\033[91m"
    B_GREEN    = "\033[92m"
    B_YELLOW   = "\033[93m"
    B_BLUE     = "\033[94m"
    B_MAGENTA  = "\033[95m"
    B_CYAN     = "\033[96m"

    # Background
    BG_GRAY    = "\033[48;5;236m"
    BG_BLUE    = "\033[48;5;24m"
    BG_GREEN   = "\033[48;5;22m"
    BG_RED     = "\033[48;5;52m"


C = Colors  # shorthand


# ── Box Drawing ───────────────────────────────────────────────────────────────

def header_box(title: str, subtitle: str = "", width: int = 62):
    """Print a double-line box header."""
    print()
    print(f"  {C.B_CYAN}╔{'═' * width}╗{C.RESET}")
    print(f"  {C.B_CYAN}║{C.RESET}  {C.BOLD}{C.WHITE}{title.center(width - 4)}{C.RESET}  {C.B_CYAN}║{C.RESET}")
    if subtitle:
        print(f"  {C.B_CYAN}║{C.RESET}  {C.DIM}{subtitle.center(width - 4)}{C.RESET}  {C.B_CYAN}║{C.RESET}")
    print(f"  {C.B_CYAN}╚{'═' * width}╝{C.RESET}")
    print()


def section_header(title: str, icon: str = "▸"):
    """Print a section divider."""
    print(f"\n  {C.B_YELLOW}{icon} {title}{C.RESET}")
    print(f"  {C.DIM}{'─' * 56}{C.RESET}\n")


def sub_section(title: str):
    """Print a lighter sub-section."""
    print(f"\n  {C.CYAN}┌─ {title}{C.RESET}")


def network_flush_banner(count: int):
    """Print a visually distinct network flush banner."""
    print()
    print(f"  {C.BG_BLUE}{C.BOLD}{C.WHITE}  ⚡ NETWORK FLUSH - delivering {count} messages (shuffled)  {C.RESET}")
    print()


# ── Event Loggers ─────────────────────────────────────────────────────────────

def log_send(sender_id: int, receiver_id: int, payload: str, seq: int):
    """Log a message send event."""
    print(f"  {C.GREEN}  ↗ SEND{C.RESET}    "
          f"Node {C.BOLD}{sender_id}{C.RESET} → Node {C.BOLD}{receiver_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(seq={seq}){C.RESET}")


def log_enqueue(payload: str, seq: int, sender_id: int, receiver_id: int):
    """Log a message being enqueued in the network."""
    print(f"  {C.BLUE}  ◆ QUEUE{C.RESET}   "
          f"'{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(seq={seq}) {sender_id}→{receiver_id}{C.RESET}")


def log_network_deliver(payload: str, seq: int, receiver_id: int):
    """Log the network delivering a message (possibly out of order)."""
    print(f"  {C.YELLOW}  ↓ WIRE{C.RESET}    "
          f"→ Node {C.BOLD}{receiver_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(seq={seq}){C.RESET}")


def log_buffer(node_id: int, payload: str, seq: int, sender_id: int, waiting_for: int):
    """Log a message being buffered (waiting for earlier seq)."""
    if seq != waiting_for:
        status = f"{C.B_RED}⏳ buffered, waiting for seq={waiting_for}{C.RESET}"
    else:
        status = f"{C.B_GREEN}✓ ready to deliver{C.RESET}"

    print(f"  {C.MAGENTA}  ◇ BUFFER{C.RESET}  "
          f"Node {C.BOLD}{node_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.WHITE}{payload}{C.RESET}' "
          f"{C.GRAY}(seq={seq}){C.RESET}  {status}")


def log_fifo_deliver(node_id: int, payload: str, seq: int):
    """Log a message being delivered in FIFO order."""
    print(f"  {C.B_GREEN}  ✓ FIFO{C.RESET}    "
          f"Node {C.BOLD}{node_id}{C.RESET}  "
          f"{C.DIM}│{C.RESET} '{C.BOLD}{C.WHITE}{payload}{C.RESET}' "
          f"{C.GREEN}(seq={seq}) delivered ✓{C.RESET}")


# ── Verification ──────────────────────────────────────────────────────────────

def log_verification(sent: list, delivered: list, passed: bool):
    """Print verification results in a box."""
    status = f"{C.B_GREEN}✓ PASS{C.RESET}" if passed else f"{C.B_RED}✗ FAIL{C.RESET}"
    print(f"\n  {C.CYAN}┌─ Verification ─────────────────────────────────┐{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  Sent:      {sent}")
    print(f"  {C.CYAN}│{C.RESET}  Delivered:  {delivered}")
    print(f"  {C.CYAN}│{C.RESET}  Status:     {status}")
    print(f"  {C.CYAN}└────────────────────────────────────────────────┘{C.RESET}\n")


def log_bidirectional_verification(
    a_delivered: list, a_expected: list,
    b_delivered: list, b_expected: list,
    passed: bool
):
    """Print bidirectional verification results."""
    status = f"{C.B_GREEN}✓ PASS{C.RESET}" if passed else f"{C.B_RED}✗ FAIL{C.RESET}"
    print(f"\n  {C.CYAN}┌─ Bidirectional Verification ───────────────────┐{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  Node A recv: {a_delivered}")
    print(f"  {C.CYAN}│{C.RESET}  Expected:    {a_expected}")
    print(f"  {C.CYAN}│{C.RESET}  Node B recv: {b_delivered}")
    print(f"  {C.CYAN}│{C.RESET}  Expected:    {b_expected}")
    print(f"  {C.CYAN}│{C.RESET}  Status:      {status}")
    print(f"  {C.CYAN}└────────────────────────────────────────────────┘{C.RESET}\n")


def final_result(all_passed: bool):
    """Print the final result banner."""
    if all_passed:
        print(f"  {C.BG_GREEN}{C.BOLD}{C.WHITE}  ✓ ALL TESTS PASSED - FIFO link working correctly!  {C.RESET}")
    else:
        print(f"  {C.BG_RED}{C.BOLD}{C.WHITE}  ✗ SOME TESTS FAILED - check output above  {C.RESET}")
    print()
