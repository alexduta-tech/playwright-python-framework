"""Utility functions for Docker environment detection.
"""
import os

def running_in_docker(logger=None) -> bool:
    """Check if the code is running inside a Docker container.
    Args:
        logger: Optional logger for debug messages.
    Returns:
        bool: True if running in a Docker container, False otherwise.
    """
    # Docker creates this marker file in every container; the cgroup check covers
    # runtimes that do not.
    docker_run = os.path.exists("/.dockerenv")

    if not docker_run:
        try:
            with open("/proc/1/cgroup", "r") as f:
                content = f.read()
            docker_run = "docker" in content or "containerd" in content
        except OSError:
            # /proc only exists on Linux, so this is the path taken on the Windows host
            docker_run = False

    if logger:
        logger.debug(f"Running in Docker: {docker_run}")
    return docker_run
