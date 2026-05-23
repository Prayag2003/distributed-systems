# Distributed Systems Course - Martin Kleppmann

Implementations and simulations for exercises from Martin Kleppmann's [Distributed Systems](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf) lecture series at the University of Cambridge (Part IB, Michaelmas 2021/22).

## Course Chapters

| #   | Chapter                                  | Topics                                                                                                                                     |
| --- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **Introduction**                         | About distributed systems · Distributed systems and computer networking · Remote Procedure Calls (RPC)                                     |
| 2   | **Models of Distributed Systems**        | The two generals problem · The Byzantine generals problem · Describing nodes and network behaviour · Fault tolerance and high availability |
| 3   | **Time, Clocks, and Ordering of Events** | Physical clocks · Clock synchronisation and monotonic clocks · Causality and happens-before                                                |
| 4   | **Broadcast Protocols and Logical Time** | Logical time · Delivery order in broadcast protocols · Broadcast algorithms                                                                |
| 5   | **Replication**                          | Manipulating remote state · Quorums · Replication using broadcast                                                                          |
| 6   | **Consensus**                            | Introduction to consensus · The Raft consensus algorithm                                                                                   |
| 7   | **Replica Consistency**                  | Two-phase commit · Linearizability · Eventual consistency                                                                                  |
| 8   | **Case Studies**                         | Collaboration and conflict resolution · Google's Spanner                                                                                   |

## Exercise Index

| Ex  | Chapter | Topic                                    | Directory                                                                            | Status |
| :-: | :-----: | ---------------------------------------- | ------------------------------------------------------------------------------------ | :----: |
|  4  |    2    | FIFO Links over Reliable Unordered Links | [`00-fault-tolerance-and-high-tolerance/`](./00-fault-tolerance-and-high-tolerance/) |   ✅   |
|  -  |    3    | Lamport Clocks                           | [`01-lamport-clocks/`](./01-lamport-clocks/)                                         |   ✅   |
|  -  |    3    | Vector Clocks                            | [`02-vector-clocks/`](./02-vector-clocks/)                                           |   ✅   |

> More exercises will be added as I work through the course.

## Course Reference

- 📖 [Lecture Notes (PDF)](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf)
- 🎥 [Video Lectures (YouTube)](https://www.youtube.com/playlist?list=PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB)
- 🌐 [Course Web Page](https://www.cst.cam.ac.uk/teaching/2122/ConcDisSys)

## Running

Each exercise is a self-contained Python project. Navigate into the directory and run:

```bash
python3 main.py
```
