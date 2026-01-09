import os

# Logging and reporting configuration 
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOG_DIR = os.path.join(ROOT_DIR, "logs")
DEFAULT_LOG_LEVEL = "DEBUG"  # DEBUG|INFO|WARNING|ERROR|CRITICAL
DEFAULT_REPORT_DIR = os.path.join(ROOT_DIR, "reports")

# Application settings(can be overridden by the environment variables stored in the existing docker-compose.yml)
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000/")
IMPLICIT_WAIT = 10000  # default value used by the waiting calls (in milliseconds)

# Browser configuration defaults -> not needed to set them here as this is handled by pytest-playwright command line args