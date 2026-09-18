import os

# Logging and reporting configuration 
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOG_DIR = os.path.join(ROOT_DIR, "logs")
DEFAULT_LOG_LEVEL = "DEBUG"  # DEBUG|INFO|WARNING|ERROR|CRITICAL
DEFAULT_REPORT_DIR = os.path.join(ROOT_DIR, "reports")

# Application settings(can be overridden by the environment variables stored in the existing docker-compose.yml)
BASE_URL = os.getenv("BASE_URL", "http://localhost:3000/")

# User store of the application under test. With --reset-app-data, conftest.py empties it
# at the start of every repetition: the backend reads and rewrites this whole file on each
# request, so a store that grows across repetitions slows down every later test. The
# default is the automation-lab checkout next to this repository.
_SIBLING_USERS_FILE = os.path.join(
    os.path.dirname(ROOT_DIR), "automation-lab", "backend", "app", "storage", "users.json"
)
AUT_USERS_FILE = os.getenv(
    "AUT_USERS_FILE", _SIBLING_USERS_FILE if os.path.exists(_SIBLING_USERS_FILE) else ""
)

IMPLICIT_WAIT = 10000  # default value used by the waiting calls (in milliseconds)

# Browser configuration defaults -> not needed to set them here as this is handled by pytest-playwright command line args

# Browser viewport. Kept identical to the Selenium framework so that both render the
# same layout and do the same paint work; pytest-playwright otherwise defaults to 1280x720.
VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

# Resource monitoring configuration.
# Sampling the process tree perturbs the durations being measured, so runs that measure
# execution time should use MONITOR_RESOURCES=false, and resource usage should be measured
# in separate runs.
MONITOR_RESOURCES = os.getenv("MONITOR_RESOURCES", "true").lower() in ("1", "true", "yes", "y", "on")
# Sampling below the Windows scheduler tick (~15.6 ms) yields both spurious zero samples
# and single-tick spikes, so the interval is kept well above it.
MONITOR_INTERVAL = float(os.getenv("MONITOR_INTERVAL", "0.5"))

# Synchronisation tuning for the waits shared by both page object layers. The values
# are deliberately identical across the two frameworks so that neither is given more
# slack than the other when the application updates asynchronously.
SETTLE_POLL_S = 0.05             # how often a polling wait re-checks its condition
LOADING_APPEAR_TIMEOUT_S = 1.0   # how long to wait for a spinner to show up at all
LOADING_DISAPPEAR_TIMEOUT_S = 10.0
SETTLE_TIMEOUT_S = 10.0          # upper bound for "the page stopped changing" waits
# How long content must stay unchanged to count as settled. The list page shows
# transient states (an empty placeholder, a spinner) for only 10-35 ms, so this is
# comfortably longer than those while adding little to each wait.
STABLE_DWELL_S = 0.15

# Timeouts shared by both frameworks, in seconds, so that neither is given more slack.
# PAGE_LOAD_TIMEOUT_S bounds the wait for a page's URL after navigating to it.
# ACTION_TIMEOUT_S bounds how long an element may take to become usable before an
# interaction fails; Playwright applies it through its default timeout, Selenium through
# an explicit wait before each interaction.
PAGE_LOAD_TIMEOUT_S = 10.0
ACTION_TIMEOUT_S = 10.0
