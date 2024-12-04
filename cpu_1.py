import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread


# Function to calculate FCFS with arrival time
def fcfs(processes, burst_time, arrival_time):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    current_time = 0

    for i in range(n):
        if arrival_time[i] > current_time:
            current_time = arrival_time[i]
        start_time = current_time
        end_time = start_time + burst_time[i]
        gantt_chart.append((processes[i], start_time, end_time))
        current_time = end_time

    for i in range(n):
        waiting_time[i] = max(0, gantt_chart[i][1] - arrival_time[i])
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart


# Function to calculate Round Robin with arrival time
def round_robin(processes, burst_time, arrival_time, quantum):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = burst_time[:]
    gantt_chart = []
    current_time = 0
    queue = []

    while True:
        for i in range(n):
            if arrival_time[i] <= current_time and remaining_time[i] > 0 and i not in queue:
                queue.append(i)
        if not queue:
            break

        current_process = queue.pop(0)
        start_time = current_time
        if remaining_time[current_process] > quantum:
            current_time += quantum
            remaining_time[current_process] -= quantum
        else:
            current_time += remaining_time[current_process]
            remaining_time[current_process] = 0
        gantt_chart.append((processes[current_process], start_time, current_time))

    for i in range(n):
        waiting_time[i] = max(0, gantt_chart[i][1] - arrival_time[i])
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart


# Function to calculate Shortest Job First with arrival time
def sjf(processes, burst_time, arrival_time):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    completed = [False] * n
    current_time = 0

    while not all(completed):
        shortest_job = -1
        for i in range(n):
            if not completed[i] and (arrival_time[i] <= current_time) and (shortest_job == -1 or burst_time[i] < burst_time[shortest_job]):
                shortest_job = i
        start_time = current_time
        end_time = start_time + burst_time[shortest_job]
        gantt_chart.append((processes[shortest_job], start_time, end_time))
        waiting_time[shortest_job] = current_time - arrival_time[shortest_job]
        turnaround_time[shortest_job] = waiting_time[shortest_job] + burst_time[shortest_job]
        current_time = end_time
        completed[shortest_job] = True

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart


# Function to calculate Priority Scheduling with arrival time
def priority_scheduling(processes, burst_time, arrival_time, priority):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    gantt_chart = []
    completed = [False] * n
    current_time = 0

    while not all(completed):
        highest_priority = -1
        for i in range(n):
            if not completed[i] and (arrival_time[i] <= current_time) and (highest_priority == -1 or priority[i] < priority[highest_priority]):
                highest_priority = i
        start_time = current_time
        end_time = start_time + burst_time[highest_priority]
        gantt_chart.append((processes[highest_priority], start_time, end_time))
        waiting_time[highest_priority] = current_time - arrival_time[highest_priority]
        turnaround_time[highest_priority] = waiting_time[highest_priority] + burst_time[highest_priority]
        current_time = end_time
        completed[highest_priority] = True

    avg_waiting_time = sum(waiting_time) / n
    avg_turnaround_time = sum(turnaround_time) / n
    return waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart


# GUI for the application
class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")

        # Initialize step-by-step simulation variables
        self.is_simulating = False
        self.simulation_thread = None
        self.current_time = 0

        # Configure the grid to allow dynamic resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

        # Labels and Inputs
        self.num_processes_label = tk.Label(root, text="Number of Processes:")
        self.num_processes_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.num_processes_entry = tk.Entry(root)
        self.num_processes_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.burst_time_label = tk.Label(root, text="Burst Time (comma-separated):")
        self.burst_time_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.burst_time_entry = tk.Entry(root)
        self.burst_time_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.arrival_time_label = tk.Label(root, text="Arrival Time (comma-separated):")
        self.arrival_time_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.arrival_time_entry = tk.Entry(root)
        self.arrival_time_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        self.priority_label = tk.Label(root, text="Priority (comma-separated, for Priority Scheduling):")
        self.priority_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.priority_entry = tk.Entry(root)
        self.priority_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        self.quantum_label = tk.Label(root, text="Quantum Time (for Round Robin):")
        self.quantum_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.quantum_entry = tk.Entry(root)
        self.quantum_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # Buttons for different scheduling algorithms
        self.fcfs_button = tk.Button(root, text="FCFS Scheduling", command=self.fcfs_scheduling)
        self.fcfs_button.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.rr_button = tk.Button(root, text="Round Robin Scheduling", command=self.rr_scheduling)
        self.rr_button.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        self.sjf_button = tk.Button(root, text="SJF Scheduling", command=self.sjf_scheduling)
        self.sjf_button.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

        self.priority_button = tk.Button(root, text="Priority Scheduling", command=self.priority_scheduling)
        self.priority_button.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Output Labels
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Output display area
        self.output_text = tk.Text(root, height=10, width=40)
        self.output_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Gantt chart section
        self.gantt_label = tk.Label(root, text="Gantt Chart:")
        self.gantt_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        self.gantt_canvas = tk.Canvas(root, height=100)
        self.gantt_canvas.grid(row=10, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def get_input_data(self):
        try:
            num_processes = int(self.num_processes_entry.get())
            burst_time = list(map(int, self.burst_time_entry.get().split(",")))
            arrival_time = list(map(int, self.arrival_time_entry.get().split(",")))
            priority = list(map(int, self.priority_entry.get().split(","))) if self.priority_entry.get() else []
            quantum = int(self.quantum_entry.get()) if self.quantum_entry.get() else None
            return num_processes, burst_time, arrival_time, priority, quantum
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid data!")
            return None, None, None, None, None

    def display_results(self, waiting_time, turnaround_time, avg_waiting_time, avg_turnaround_time, gantt_chart):
        result = "Waiting Time: " + str(waiting_time) + "\n"
        result += "Turnaround Time: " + str(turnaround_time) + "\n"
        result += f"Average Waiting Time: {avg_waiting_time:.2f}\n"
        result += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

        self.gantt_chart = gantt_chart
        self.current_time = 0
        self.display_gantt_chart(gantt_chart, current_time=self.current_time)

    def display_gantt_chart(self, gantt_chart, current_time=None):
        self.gantt_canvas.delete("all")
        canvas_width = self.gantt_canvas.winfo_width()
        total_time = gantt_chart[-1][2]
        x_start = 10

        for process, start, end in gantt_chart:
            process_width = (end - start) / total_time * canvas_width
            color = "skyblue" if current_time is None or start <= current_time < end else "lightgray"
            self.gantt_canvas.create_rectangle(x_start, 20, x_start + process_width, 80, fill=color)
            self.gantt_canvas.create_text(
                x_start + process_width / 2, 50, text=f"P{process}", fill="black"
            )
            x_start += process_width

    def start_simulation(self):
        if not hasattr(self, "gantt_chart") or not self.gantt_chart:
            messagebox.showwarning("No Data", "Please run a scheduling algorithm first!")
            return
        if not self.is_simulating:
            self.is_simulating = True
            self.simulation_thread = Thread(target=self.run_simulation)
            self.simulation_thread.start()

    def pause_simulation(self):
        self.is_simulating = False

    def run_simulation(self):
        for process, start, end in self.gantt_chart:
            while self.current_time < end:
                if not self.is_simulating:
                    return
                self.display_gantt_chart(self.gantt_chart, current_time=self.current_time)
                time.sleep(1)
                self.current_time += 1

    def fcfs_scheduling(self):
        num_processes, burst_time, arrival_time, _, _ = self.get_input_data()
        if num_processes is None:
            return
        processes = range(num_processes)
        results = fcfs(processes, burst_time, arrival_time)
        self.display_results(*results)

    def rr_scheduling(self):
        num_processes, burst_time, arrival_time, _, quantum = self.get_input_data()
        if num_processes is None or quantum is None:
            return
        processes = range(num_processes)
        results = round_robin(processes, burst_time, arrival_time, quantum)
        self.display_results(*results)

    def sjf_scheduling(self):
        num_processes, burst_time, arrival_time, _, _ = self.get_input_data()
        if num_processes is None:
            return
        processes = range(num_processes)
        results = sjf(processes, burst_time, arrival_time)
        self.display_results(*results)

    def priority_scheduling(self):
        num_processes, burst_time, arrival_time, priority, _ = self.get_input_data()
        if num_processes is None or not priority:
            return
        processes = range(num_processes)
        results = priority_scheduling(processes, burst_time, arrival_time, priority)
        self.display_results(*results)


# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()
