"""
psutil resource monitoring for the test automation framework.
"""
import os
import platform
import threading
import time
import psutil

class ResourceMonitor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.cpu_samples = []
        self.mem_samples = []
        self._running = False
        self.process = psutil.Process(os.getpid())

    def _collect(self):
        """ 
        Collect resource usage data for the current process and its children.
        """
        # Prime the CPU to avoid 0.0 at first call: Initialize psutil’s internal CPU counters before real measurement starts
        self.process.cpu_percent(interval=None)

        # The while loop continuously collects CPU and memory usage samples
        # of the current process and its children as long as the `_running`
        # flag is True. 
        while self._running:
            try:
                procs = [self.process] + self.process.children(recursive=True)

                cpu = sum(p.cpu_percent(interval=None) for p in procs)
                mem = sum(p.memory_info().rss for p in procs)

                self.cpu_samples.append(cpu)
                self.mem_samples.append(mem)

                time.sleep(self.interval)
            
            # If the process is no longer running, stop the monitoring
            except psutil.NoSuchProcess:
                break

    def start(self):
        """
        Start the resource monitoring thread.
        """
        self._running = True
        self.thread = threading.Thread(target=self._collect, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stop the resource monitoring thread.
        """
        self._running = False
        self.thread.join()
#
    def summary(self):
        """
        Generate the resource monitoring summary.
        """
        return {
            "framework": "playwright",
            "os": platform.system(),
            "browser": "chrome", # TODO: set this manually
            "headles": "True",  # TODO: set this manually
            "process_name": self.process.name(),
            "cpu_avg": sum(self.cpu_samples) / len(self.cpu_samples),
            "cpu_peak": max(self.cpu_samples),
            "mem_avg_mb": (sum(self.mem_samples) / len(self.mem_samples)) / 1024**2,
            "mem_peak_mb": max(self.mem_samples) / 1024**2,
        }