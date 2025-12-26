"""Utility functions for Docker environment detection.
"""

def running_in_docker(logger=None) -> bool:
    """Check if the code is running inside a Docker container.
    Args:
        logger: Optional logger for debug messages.
    Returns:
        bool: True if running in a Docker container, False otherwise.
    """    
    try:
        with open("/proc/1/cgroup", "r") as f:
            content = f.read()
            docker_run = "docker" in content or "containerd" in content
            logger.debug(f"Running in Docker: {docker_run}")
            return docker_run
    except:
        logger.debug("Not running in Docker")
        return False