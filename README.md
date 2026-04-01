CPU Scheduling Simulator


A high-fidelity terminal-based simulator designed to analyze and compare CPU scheduling algorithms. This project was developed as part of the Operating Systems course to demonstrate process management, preemption logic, and multi-level feedback queueing.

1. Project Overview

Objective: To simulate and visualize the behavior of various CPU scheduling algorithms.

Major Features: * Time-proportional Gantt Chart visualization.

Automatic calculation of Waiting Time, Turnaround Time, and Response Time.

Support for CSV-based batch input or manual interactive entry.

2. Team Information
Team Name: Team OS-CPU-Scheduling-Team2

Members:

Run Chandara , Eung David , Ron Sovanrith


3. Implemented Algorithms
The system implements the following 5 algorithms with specific logic:

- First-Come, First-Served (FCFS): Non-preemptive. Processes are executed in the exact order of their arrival.

- Shortest Job First (SJF): Non-preemptive. When the CPU is free, it selects the process with the smallest total burst time among arrived processes.

- Shortest Remaining Time (SRT): Preemptive version of SJF. The CPU re-evaluates at every arrival or clock tick; if a new process has a shorter remaining time than the current one, it preempts.

- Round Robin (RR): Preemptive. Each process gets a fixed "Time Quantum." If it doesn't finish, it moves to the back of the ready queue.

- Multilevel Feedback Queue (MLFQ): 3-Queue structure:

Queue 0: RR (q=2)

Queue 1: RR (q=4)

Queue 2: FCFS

Aging: Processes waiting in lower queues for >10 units are promoted to prevent starvation.

4. System Architecture
- Programming Language: Python 3.12

- Architecture: Modular functional design.

- Process Class: Manages state and metadata for each task.

- Simulation Engine: Independent functions for each algorithm returning a schedule tuple.

- Visualization Engine: Grid-based ASCII renderer for the Gantt Chart.

5. Requirements & Installation
- No external libraries (like NumPy or Pandas) are required. The project runs on standard Python 3.x.

- Clone the Repository:

Bash
git clone [your-repo-url]
cd [your-repo-folder]
Run the Simulator:

Bash
python3 cpu_scheduler.py
6. Input Format (CSV)
If using a CSV file, format it as follows (without headers):
PID, Arrival_Time, Burst_Time, [Priority]

Example (data.csv):

Code snippet
P1, 0, 8
P2, 1, 4
P3, 2, 9
P4, 3, 5

7. Performance Metrics
The simulator evaluates performance based on:

Waiting Time (WT): Turnaround Time - Burst Time

Turnaround Time (TAT): Finish Time - Arrival Time

Response Time (RT): First Start Time - Arrival Time

