# 02 - Vector Clocks

Implementation of Vector Clocks to solve the concurrency detection limitation of Lamport Clocks (Chapter 3).

## Overview

Unlike Lamport Clocks which provide a single scalar timestamp and guarantee $a \rightarrow b \implies L(a) < L(b)$, Vector Clocks use an array of timestamps (one per node) to guarantee that $V(a) < V(b) \iff a \rightarrow b$. This allows us to accurately detect when two events are concurrent: $a \parallel b$.

This simulation includes four phases to demonstrate vector clock behavior and properties:

1. **Simple Exchange**: Demonstrates basic send and receive invariant updates.
2. **Concurrent Sends**: Shows how concurrent messages have concurrent vector timestamps.
3. **Causal Chain**: Validates transitive happens-before properties.
4. **Solving Lamport's Limitation**: Replicates the concurrent local events scenario where Lamport Clocks falsely implied a causal relationship. Vector clocks correctly show they are concurrent ($[2,0] \parallel [0,1]$).

## Running

Run the simulation directly:

```bash
python3 main.py
```

## Structure

* `node.py`: Implements the `Node` with the local vector clock `V`.
* `network.py`: A silent unordered network delivery simulator.
* `message.py`: Carries the payload and the vector clock snapshot.
* `main.py`: Sets up the 4 phases and verifies correctness.
* `visuals.py`: Renders the vector-aware ASCII space-time diagram in the terminal.
