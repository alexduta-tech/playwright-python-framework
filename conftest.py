"""
Conftest file to define pytest fixtures for Playwright tests.
Fixtures to run before and after each test, including logger, screenshot etc.
"""
import csv
import os
import platform
import time
import uuid
import pytest
from monitoring import resource_monitor
from utils.config import (
    AUT_USERS_FILE,
    DEFAULT_REPORT_DIR,
    MONITOR_RESOURCES,
    MONITOR_INTERVAL,
    ACTION_TIMEOUT_S,
    VIEWPORT_WIDTH,
    VIEWPORT_HEIGHT,
)
from utils.docker import running_in_docker
from utils.logger import get_logger

# Ensure reports directory exists
os.makedirs(DEFAULT_REPORT_DIR, exist_ok=True)

RESOURCE_SUMMARY_FIELDS = [
    "run_id",
    "framework",
    "os",
    "browser",
    "browser_version",
    "headless",
    "process_name",
    "sample_interval_s",
    "samples",
    "cpu_avg",
    "cpu_peak",
    "mem_avg_mb",
    "mem_peak_mb",
]


# Repetition whose data was last reset; a sentinel so that the first test always resets
_last_reset_repetition = [object()]
_data_resets = [0]


def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--reset-app-data",
        action="store_true",
        default=False,
        help="Empty the user store of the application under test (AUT_USERS_FILE) before "
             "every repetition, so that each repetition starts from the same data.",
    )


def pytest_configure(config):
    """Fail fast if a data reset is requested but the user store cannot be found."""
    if config.getoption("reset_app_data") and not (AUT_USERS_FILE and os.path.isfile(AUT_USERS_FILE)):
        raise pytest.UsageError(
            f"--reset-app-data: the application's users.json was not found "
            f"({AUT_USERS_FILE or 'AUT_USERS_FILE is not set'}); set AUT_USERS_FILE to its path"
        )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    """
    Label the resource samples taken from here on with this test and repetition, and,
    with --reset-app-data, empty the application's user store before the first test of
    each repetition (pytest-repeat with --repeat-scope=session), or once per session
    without --count. This runs before pytest starts timing the test, so it is not part
    of any duration.
    """
    callspec = getattr(item, "callspec", None)
    repetition = callspec.params.get("__pytest_repeat_step_number") if callspec else None
    monitor = getattr(item.session, "resource_monitor", None)
    if monitor is not None:
        # pytest-repeat numbers steps from 0; test IDs show them from 1
        monitor.label = ((repetition or 0) + 1, item.name)
    if not item.config.getoption("reset_app_data") or repetition == _last_reset_repetition[0]:
        return None
    with open(AUT_USERS_FILE, "w", encoding="utf-8") as f:
        f.write('{\n    "users": []\n}\n')
    _last_reset_repetition[0] = repetition
    _data_resets[0] += 1
    return None


def pytest_terminal_summary(terminalreporter, config):
    """Add a summary of the application data resets to the terminal report."""
    if config.getoption("reset_app_data"):
        terminalreporter.write_line(f"Application data reset {_data_resets[0]} time(s): {AUT_USERS_FILE}")


# Browsers the tests of this session ran on, as "name version ..." labels
_browsers_seen = set()


def _record_browser(json_metadata, browser):
    """
    Attach the browser a test ran on to its JSON report entry and remember it for the
    session summary, so that browser versions are taken from the run itself.
    """
    json_metadata["browser"] = browser
    label = f"{browser['name']} {browser['version']}"
    if browser.get("channel"):
        label += f" (channel {browser['channel']})"
    if browser.get("driver_version"):
        label += f" (driver {browser['driver_version']})"
    _browsers_seen.add(label)


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    """
    Add the browsers used by the session to the top level of the JSON report.
    """
    json_report["browsers"] = sorted(_browsers_seen)
    json_report["data_reset"] = {"enabled": _data_resets[0] > 0, "users_file": AUT_USERS_FILE,
                                 "resets": _data_resets[0]}


def _browser_metadata(config):
    """Describe the browser this run was launched with, from the pytest command line."""
    browsers = config.getoption("browser") or ["chromium"]
    channel = config.getoption("browser_channel")
    return {
        # A channel (chrome, msedge) overrides the engine name, since it identifies
        # the actual binary that was launched.
        "browser": channel or ",".join(browsers),
        "headless": not config.getoption("headed"),
    }


def _rotate_summary_if_schema_changed(path):
    """
    Move an existing summary aside when it was written with a different set of columns.

    csv.DictWriter only emits a header for an empty file, so appending the current
    fields to a file written by an older version would silently misalign every value
    under the previous header.
    """
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return

    with open(path, newline="") as existing:
        header = next(csv.reader(existing), [])

    if header != RESOURCE_SUMMARY_FIELDS:
        archived = f"{os.path.splitext(path)[0]}_{time.strftime('%Y%m%d-%H%M%S')}.csv"
        os.replace(path, archived)


# Fixtures to run before and after each test
@pytest.fixture
def logger(request):
    """
    Fixture to log the start and end of each test.
    """
    test_name = request.node.name
    logger = get_logger(test_name)
    logger.info(f"Start test: {test_name}")
    yield logger
    logger.info(f"Finish test: {test_name}")


@pytest.fixture(scope="function")
def browser(launch_browser, json_metadata, pytestconfig):
    """
    Launch and close a browser around every test.

    This overrides pytest-playwright's session-scoped `browser` fixture on purpose.
    The Selenium framework starts and quits a driver per test, so a session-scoped
    browser here would make the two frameworks incomparable: Playwright would pay
    the browser startup cost once per session instead of once per test. A long-lived
    browser also degrades measurably over repeated runs, which shows up as a steadily
    increasing suite duration rather than as stable measurements.
    """
    browser = launch_browser()
    _record_browser(json_metadata, {
        "name": browser.browser_type.name,
        "version": browser.version,
        "channel": pytestconfig.getoption("browser_channel") or "",
    })
    yield browser
    browser.close()


@pytest.fixture
def context(new_context):
    """
    Create the browser context with the shared action timeout.

    Playwright waits up to 30 s by default for an element to become actionable,
    while the Selenium framework waits ACTION_TIMEOUT_S, so the default is aligned.
    """
    context = new_context()
    context.set_default_timeout(ACTION_TIMEOUT_S * 1000)
    return context


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Pin the viewport so that both frameworks render at the same size.
    """
    return {
        **browser_context_args,
        "viewport": {"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
    }


@pytest.fixture
def screenshot(request, page, logger):
    """
    Automatically take a screenshot at the end of the test.
    Requires pytest-playwright's 'page' fixture.
    """
    logger.debug(f"Playwright test")
    logger.debug(f"Operating System: {platform.platform()}")
    running_in_docker(logger)
    
    yield  # let the test run

    # Attempt to save a screenshot after the test
    try:
        screenshot_path = os.path.join(DEFAULT_REPORT_DIR, f"{request.node.name}.png")
        page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved at {screenshot_path}")
    except Exception:
        logger.exception("Failed to save screenshot")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Start resource monitoring at the beginning of the test session.

    Monitoring is skipped when MONITOR_RESOURCES is disabled: sampling the process
    tree competes with the tests for CPU and inflates the measured durations, so
    runs that measure execution time must run without it.
    """
    session.resource_monitor = None

    if not MONITOR_RESOURCES:
        return

    metadata = _browser_metadata(session.config)
    session.resource_monitor = resource_monitor.ResourceMonitor(
        interval=MONITOR_INTERVAL,
        browser=metadata["browser"],
        headless=metadata["headless"],
    )
    session.resource_monitor.start()


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Stop resource monitoring at the end of the test session.
    """
    monitor = getattr(session, "resource_monitor", None)
    if monitor is None:
        return

    monitor.stop()
    results = monitor.summary()
    monitor.write_samples(os.path.join(DEFAULT_REPORT_DIR, "resource_samples.csv"))

    run_id = str(uuid.uuid4())[:8]
    summary_path = os.path.join(DEFAULT_REPORT_DIR, "resource_summary.csv")
    _rotate_summary_if_schema_changed(summary_path)

    with open(summary_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESOURCE_SUMMARY_FIELDS)

        if f.tell() == 0:
            writer.writeheader()

        writer.writerow({
            "run_id": run_id,
            **results,
            "browser_version": "; ".join(sorted(_browsers_seen)),
        })
