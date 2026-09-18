"""
psutil resource monitoring for the test automation framework.
"""
import csv
import os
import platform
import threading
import time
import psutil

from utils.config import MONITOR_INTERVAL

class ResourceMonitor:
    def __init__(self, interval=MONITOR_INTERVAL, browser="unknown", headless=True):
        self.interval = interval
        # Recorded from the pytest command line rather than hardcoded, so the summary
        # always describes the browser the run actually used.
        self.browser = browser
        self.headless = headless
        self.cpu_samples = []
        self.mem_samples = []
        # Every sample, labelled with the repetition and test running when it was taken,
        # so that usage can be analysed per repetition instead of per session only.
        # conftest.py sets `label` before each test; a tuple is replaced atomically.
        self.label = ("", "")
        self.samples = []
        self._running = False
        self.process = psutil.Process(os.getpid())
        # psutil derives cpu_percent() from the delta against the previous call on the
        # SAME Process object. children() returns freshly built objects on every call,
        # so the tree must be cached by pid, otherwise every child reports 0.0 forever
        # and the browser's CPU usage never reaches the samples.
        self._tracked = {self.process.pid: self.process}
        # A process only produces a usable reading from its second call onwards.
        self._primed = set()

    def _tracked_processes(self):
        """
        Return the current process tree, reusing cached Process objects so that the
        CPU deltas accumulated for already-seen processes are preserved.
        """
        current = {self.process.pid: self.process}

        try:
            children = self.process.children(recursive=True)
        except psutil.NoSuchProcess:
            children = []

        for child in children:
            cached = self._tracked.get(child.pid)
            if cached is not None:
                try:
                    # Reuse the cached object unless the pid was recycled meanwhile.
                    if cached.create_time() == child.create_time():
                        current[child.pid] = cached
                        continue
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            current[child.pid] = child

        # Drop exited processes so a recycled pid is primed again before it counts.
        self._primed &= current.keys()
        self._tracked = current
        return current

    def _collect(self):
        """
        Collect resource usage data for the current process and its children.
        """
        # Prime the CPU counters for the root process so that its first in-loop
        # reading is already a real measurement rather than a placeholder 0.0.
        self.process.cpu_percent(interval=None)
        self._primed.add(self.process.pid)

        # The while loop continuously collects CPU and memory usage samples
        # of the current process and its children as long as the `_running`
        # flag is True.
        next_sample = time.monotonic()
        started = next_sample

        while self._running:
            cpu = 0.0
            mem = 0
            repetition, test = self.label
            tracked = self._tracked_processes()

            for pid, process in tracked.items():
                try:
                    usage = process.cpu_percent(interval=None)
                    mem += process.memory_info().rss
                # If a process disappeared mid-sample, skip it and keep going
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

                # The first reading of a newly seen process has no reference point
                # and is always 0.0, so prime it now and count it from the next sample.
                if pid in self._primed:
                    cpu += usage
                else:
                    self._primed.add(pid)

            self.cpu_samples.append(cpu)
            self.mem_samples.append(mem)
            self.samples.append((time.monotonic() - started, repetition, test, cpu, mem, len(tracked)))

            # Schedule against a fixed clock so that the time spent collecting does
            # not stretch the period beyond the configured interval. After an overrun
            # the schedule restarts from now instead of firing a burst of samples.
            next_sample = max(next_sample + self.interval, time.monotonic())
            time.sleep(max(0.0, next_sample - time.monotonic()))

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

    def write_samples(self, path):
        """
        Write every sample to a CSV file, one row per sample.
        """
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["t_s", "repetition", "test", "cpu_percent", "mem_mb", "processes"])
            for t, repetition, test, cpu, mem, processes in self.samples:
                writer.writerow([f"{t:.3f}", repetition, test, f"{cpu:.1f}", f"{mem / 1024**2:.1f}", processes])

    def summary(self):
        """
        Generate the resource monitoring summary.
        """
        return {
            "framework": "playwright",
            "os": platform.system(),
            "browser": self.browser,
            "headless": self.headless,
            "process_name": self.process.name(),
            "sample_interval_s": self.interval,
            "samples": len(self.cpu_samples),
            "cpu_avg": sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0,
            "cpu_peak": max(self.cpu_samples) if self.cpu_samples else 0.0,
            "mem_avg_mb": (sum(self.mem_samples) / len(self.mem_samples)) / 1024**2 if self.mem_samples else 0.0,
            "mem_peak_mb": max(self.mem_samples) / 1024**2 if self.mem_samples else 0.0,
        }
