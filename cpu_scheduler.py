#!/usr/bin/env python3
import csv
from typing import List, Tuple

class Process:
    def __init__(self, pid: str, arrival: int, burst: int, priority: int = 0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority          
        self.remaining = burst            
        self.start_time = -1              
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.last_checked = arrival

    def __repr__(self):
        return f"P({self.pid})"

# --- UI & Visualization ---

def print_gantt_chart(schedule: List[Tuple[str, int, int]]):
    if not schedule:
        return

    print("\nGantt Chart Visual:")

    # SCALE = characters per 1 unit of time. 
    # Use 3 to ensure there is enough room for PIDs like "P10"
    SCALE = 3 
    
    # Calculate the total characters needed for the chart
    max_time = schedule[-1][2]
    total_chars = (max_time * SCALE) + 1
    
    # Initialize rows with spaces
    top_row = list(" " * total_chars)
    mid_row = list(" " * total_chars)
    btm_row = list(" " * total_chars)
    # Timeline row needs extra space for multi-digit numbers at the end
    time_row = list(" " * (total_chars + 5))

    # Draw the boxes
    for pid, start, end in schedule:
        s_idx = start * SCALE
        e_idx = end * SCALE
        
        # Draw boundaries
        top_row[s_idx] = "+"
        mid_row[s_idx] = "|"
        btm_row[s_idx] = "+"
        
        # Draw horizontal lines
        for i in range(s_idx + 1, e_idx):
            top_row[i] = "-"
            btm_row[i] = "-"
            
        # Place PID (centered)
        pid_str = str(pid)
        width = e_idx - s_idx
        if len(pid_str) < width:
            offset = (width - len(pid_str)) // 2
            for i, char in enumerate(pid_str):
                mid_row[s_idx + offset + i] = char
        else:
            for i in range(min(len(pid_str), width - 1)):
                mid_row[s_idx + 1 + i] = pid_str[i]

    # Close the very last box
    top_row[total_chars - 1] = "+"
    mid_row[total_chars - 1] = "|"
    btm_row[total_chars - 1] = "+"

    # Draw Timeline Numbers
    # Place '0'
    time_row[0] = "0"
    # Place each 'end' time exactly at its scale position
    for _, _, end in schedule:
        e_idx = end * SCALE
        e_str = str(end)
        # To make it look perfect, if the number is > 1 digit, 
        # we center the number under the '+' 
        start_offset = e_idx - (len(e_str) // 2)
        if start_offset < 0: start_offset = 0
        
        for i, char in enumerate(e_str):
            time_row[start_offset + i] = char

    # Print the final result
    print("".join(top_row))
    print("".join(mid_row))
    print("".join(btm_row))
    print("".join(time_row).rstrip())
    print("")

def compute_metrics(processes: List[Process]):
    print(f"{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Wait':<10}{'Turn':<10}{'Resp':<10}")
    print("-" * 60)
    
    t_wait, t_turn, t_resp = 0, 0, 0
    for p in sorted(processes, key=lambda x: x.pid):
        p.waiting_time = p.turnaround_time - p.burst
        p.response_time = max(0, p.start_time - p.arrival)
        print(f"{p.pid:<10}{p.arrival:<10}{p.burst:<10}{p.waiting_time:<10}{p.turnaround_time:<10}{p.response_time:<10}")
        t_wait += p.waiting_time
        t_turn += p.turnaround_time
        t_resp += p.response_time
    
    n = len(processes)
    print("-" * 60)
    print(f"Average Waiting Time:    {t_wait/n:.2f}")
    print(f"Average Turnaround Time: {t_turn/n:.2f}")
    print(f"Average Response Time:   {t_resp/n:.2f}")

# --- Input Handling ---

def read_processes_from_file(filename: str) -> List[Process]:
    processes = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    processes.append(Process(row[0].strip(), int(row[1]), int(row[2]), int(row[3]) if len(row) > 3 else 0))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return processes

def read_processes_interactive() -> List[Process]:
    print("Enter: pid arrival burst [priority] (or 'done' to finish)")
    processes = []
    while True:
        line = input("> ").strip()
        if line.lower() == 'done': break
        parts = line.split()
        if len(parts) >= 3:
            processes.append(Process(parts[0], int(parts[1]), int(parts[2]), int(parts[3]) if len(parts) > 3 else 0))
    return processes

# --- Algorithms ---

def fcfs(processes: List[Process]) -> List[Tuple[str, int, int]]:
    procs = sorted(processes, key=lambda p: p.arrival)
    schedule, current_time = [], 0
    for p in procs:
        if current_time < p.arrival: current_time = p.arrival
        p.start_time = current_time
        p.finish_time = current_time + p.burst
        p.turnaround_time = p.finish_time - p.arrival
        schedule.append((p.pid, p.start_time, p.finish_time))
        current_time = p.finish_time
    return schedule

def sjf(processes: List[Process]) -> List[Tuple[str, int, int]]:
    remaining = sorted(processes, key=lambda p: p.arrival)
    schedule, current_time = [], 0
    while remaining:
        available = [p for p in remaining if p.arrival <= current_time]
        if not available:
            current_time = min(p.arrival for p in remaining)
            continue
        p = min(available, key=lambda p: p.burst)
        p.start_time = current_time
        p.finish_time = current_time + p.burst
        p.turnaround_time = p.finish_time - p.arrival
        schedule.append((p.pid, p.start_time, p.finish_time))
        current_time = p.finish_time
        remaining.remove(p)
    return schedule

def srt(processes: List[Process]) -> List[Tuple[str, int, int]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    schedule, current_time = [], 0
    last_pid, last_start = None, 0
    while True:
        available = [p for p in procs if p.arrival <= current_time and p.remaining > 0]
        if not available:
            if all(p.remaining == 0 for p in procs): break
            current_time = min(p.arrival for p in procs if p.remaining > 0)
            continue
        p = min(available, key=lambda p: p.remaining)
        if last_pid != p.pid:
            if last_pid is not None: schedule.append((last_pid, last_start, current_time))
            last_pid, last_start = p.pid, current_time
            if p.start_time == -1: p.start_time = current_time
        p.remaining -= 1
        current_time += 1
        if p.remaining == 0:
            p.finish_time = current_time
            p.turnaround_time = p.finish_time - p.arrival
            schedule.append((p.pid, last_start, current_time))
            last_pid = None
    for orig in processes:
        for p in procs:
            if orig.pid == p.pid:
                orig.start_time, orig.finish_time, orig.turnaround_time = p.start_time, p.finish_time, p.turnaround_time
    return schedule

def round_robin(processes: List[Process], quantum: int) -> List[Tuple[str, int, int]]:
    procs = [Process(p.pid, p.arrival, p.burst) for p in processes]
    procs.sort(key=lambda p: p.arrival)
    ready_queue, schedule, current_time, idx = [], [], 0, 0
    while ready_queue or idx < len(procs):
        while idx < len(procs) and procs[idx].arrival <= current_time:
            ready_queue.append(procs[idx]); idx += 1
        if not ready_queue:
            current_time = procs[idx].arrival; continue
        p = ready_queue.pop(0)
        if p.start_time == -1: p.start_time = current_time
        exec_time = min(quantum, p.remaining)
        schedule.append((p.pid, current_time, current_time + exec_time))
        current_time += exec_time
        p.remaining -= exec_time
        while idx < len(procs) and procs[idx].arrival <= current_time:
            ready_queue.append(procs[idx]); idx += 1
        if p.remaining > 0: ready_queue.append(p)
        else:
            p.finish_time = current_time
            p.turnaround_time = p.finish_time - p.arrival
    for orig in processes:
        for p in procs:
            if orig.pid == p.pid:
                orig.start_time, orig.finish_time, orig.turnaround_time = p.start_time, p.finish_time, p.turnaround_time
    return schedule

def mlfq(processes: List[Process], q_vals=[2, 4], aging=10) -> List[Tuple[str, int, int]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
    procs.sort(key=lambda p: p.arrival)
    q0, q1, q2 = [], [], []
    schedule, current_time, idx = [], 0, 0
    while q0 or q1 or q2 or idx < len(procs):
        while idx < len(procs) and procs[idx].arrival <= current_time:
            q0.append(procs[idx]); idx += 1
        for p in q1[:]:
            if current_time - p.last_checked > aging:
                p.last_checked = current_time; q0.append(p); q1.remove(p)
        for p in q2[:]:
            if current_time - p.last_checked > aging:
                p.last_checked = current_time; q1.append(p); q2.remove(p)
        if q0: p, qt, qv = q0.pop(0), 0, q_vals[0]
        elif q1: p, qt, qv = q1.pop(0), 1, q_vals[1]
        elif q2: p, qt, qv = q2.pop(0), 2, None
        else: current_time = procs[idx].arrival; continue
        if p.start_time == -1: p.start_time = current_time
        ex = p.remaining if qt == 2 else min(qv, p.remaining)
        schedule.append((p.pid, current_time, current_time + ex))
        current_time += ex
        p.remaining -= ex
        p.last_checked = current_time
        if p.remaining > 0:
            if qt == 0: q1.append(p)
            else: q2.append(p)
        else:
            p.finish_time = current_time
            p.turnaround_time = p.finish_time - p.arrival
    for orig in processes:
        for p in procs:
            if orig.pid == p.pid:
                orig.start_time, orig.finish_time, orig.turnaround_time = p.start_time, p.finish_time, p.turnaround_time
    return schedule

def main():
    print("=== CPU SCHEDULING SIMULATOR ===")
    print("1. Load CSV\n2. Manual Input")
    choice = input("Choice: ").strip()
    processes = read_processes_from_file(input("File: ")) if choice == '1' else read_processes_interactive()
    if not processes: return
    print("\n1.FCFS 2.SJF 3.SRT 4.RR 5.MLFQ")
    algo = input("Algo: ").strip()
    if algo == '1': s = fcfs(processes)
    elif algo == '2': s = sjf(processes)
    elif algo == '3': s = srt(processes)
    elif algo == '4': s = round_robin(processes, int(input("Quantum: ")))
    elif algo == '5': s = mlfq(processes)
    else: return
    print_gantt_chart(s)
    compute_metrics(processes)

if __name__ == "__main__":
    main()