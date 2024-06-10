import psutil
import time
import pygetwindow as gw
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class WindowSwitchDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Switch Detection")
        self.root.geometry("800x600")

        self.last_active_window = None
        self.switch_times = []
        self.switch_counts = []

        self.create_widgets()
        self.update_window()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Monitoring window switches...", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.switch_count_label = ttk.Label(self.root, text="Switch Count: 0", font=("Helvetica", 12))
        self.switch_count_label.pack()

        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Window Switches Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Switch Count")
        self.line, = self.ax.plot([], [], marker='o')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20)

    def get_active_window_title(self):
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
            return None
        except Exception as e:
            print(f"Error getting active window: {e}")
            return None

    def update_window(self):
        current_active_window = self.get_active_window_title()
        if current_active_window != self.last_active_window:
            self.last_active_window = current_active_window
            switch_time = datetime.now()
            self.switch_times.append(switch_time)
            self.switch_counts.append(len(self.switch_times))
            self.update_graph()
            self.update_switch_count_label()

        self.root.after(1000, self.update_window)

    def update_switch_count_label(self):
        self.switch_count_label.config(text=f"Switch Count: {len(self.switch_counts)}")

    def update_graph(self):
        self.line.set_xdata(self.switch_times)
        self.line.set_ydata(self.switch_counts)
        self.ax.set_xlim(self.switch_times[0], self.switch_times[-1])
        self.ax.set_ylim(0, max(self.switch_counts) + 1)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowSwitchDetector(root)
    root.mainloop()
