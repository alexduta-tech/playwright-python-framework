# Playwright Python Framework

UI tests for the [Automation Playground](https://github.com/alexduta-tech/automation-lab) web app, written with Playwright, pytest and the Page Object Model. A Selenium version with the same tests is in [selenium-python-framework](https://github.com/alexduta-tech/selenium-python-framework).

## 1. Install

You need Python 3.13 and Chrome or Edge. Playwright uses the installed Chrome and Edge, and installs its own Firefox.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium firefox
```

## 2. Get and start the application

The tests need the [Automation Playground](https://github.com/alexduta-tech/automation-lab) app. Clone it into the same folder as this repository:

```
workspace/
├── automation-lab/
└── playwright-python-framework/
```

```powershell
git clone https://github.com/alexduta-tech/automation-lab.git
```

`--reset-app-data` and the Docker setup look for the app's data there. If you cloned it somewhere else, set `AUT_USERS_FILE` (local runs) or `AUT_STORAGE_DIR` (Docker) to its location.

Start the app before running the tests (see its README):

- for **local** test runs, use its **local** installation;
- for test runs **in Docker**, use its **Docker** installation.

## 3. Run the tests

```powershell
pytest -m smoke --browser-channel chrome                   # all tests, once, in Chrome
pytest tests/test_list_users.py --browser-channel chrome   # one test file
```

Choose the browser on the command line:

| Browser | Option |
|---|---|
| Chrome | `--browser-channel chrome` |
| Edge | `--browser-channel msedge` |
| Firefox (Playwright's own build) | `--browser firefox` |

Always choose a browser: without an option, Playwright uses its own Chromium instead of Chrome. Add `--headed` to see the browser window.

## 4. Repeated runs

- `--count=N` runs the whole test suite N times.
- `--reset-app-data` empties the app's user list before each repetition, so every repetition starts with the same data. Use it for repeated runs; without it, the app gets slower as users pile up.
- `MONITOR_RESOURCES` turns CPU and memory recording on or off. It is on by default; turn it off when you measure execution time, because recording uses CPU itself.

**Chrome, Edge and Firefox, 10 repetitions each**

```powershell
$env:MONITOR_RESOURCES = "false"
pytest -m smoke --browser-channel chrome --count=10 --reset-app-data
pytest -m smoke --browser-channel msedge --count=10 --reset-app-data
pytest -m smoke --browser firefox --count=10 --reset-app-data
```

Each run overwrites `reports/`, so copy the results somewhere else before starting the next browser.

**Chrome, 50 repetitions**

```powershell
$env:MONITOR_RESOURCES = "false"
pytest -m smoke --browser-channel chrome --count=50 --reset-app-data
```

**Chrome, 50 repetitions, with CPU and memory recording**

```powershell
$env:MONITOR_RESOURCES = "true"
pytest -m smoke --browser-channel chrome --count=50 --reset-app-data
```

`--reset-app-data` needs the app's `users.json`: set `AUT_USERS_FILE` to its path if it is not at the default location (see `utils/config.py`). If the file is not found, the run stops before any test starts.

> PowerShell keeps `$env:` values until you close the terminal. Remove one with `Remove-Item Env:MONITOR_RESOURCES`.

## 5. Results

| File | Contents |
|---|---|
| `reports/report.html` | Test results, to open in a browser |
| `reports/report.json` | All results with the duration of each test step |
| `reports/resource_samples.csv` | CPU and memory samples (when recording is on) |
| `reports/resource_summary.csv` | CPU and memory summary per run (when recording is on) |
| `reports/*.png` | Screenshot at the end of each test |
| `logs/` | One log file per test |

CPU values are summed over all processes and cores, so they can exceed 100%.

## 6. Settings

The browser is chosen on the command line (section 3); everything else is set with environment variables, whose defaults are in `utils/config.py`.

| Variable | Default | Meaning |
|---|---|---|
| `MONITOR_RESOURCES` | `true` | Record CPU and memory |
| `MONITOR_INTERVAL` | `0.5` | Seconds between CPU and memory samples |
| `BASE_URL` | `http://localhost:3000/` | Address of the app |
| `AUT_USERS_FILE` | see `utils/config.py` | Path to the app's `users.json`, used by `--reset-app-data` |
| `VIEWPORT_WIDTH`, `VIEWPORT_HEIGHT` | `1920`, `1080` | Browser window size |

## 7. Docker

Build the image and start the container:

```powershell
.\run_playwright_docker.bat
```

Run commands inside the container with `docker compose exec`, and pass settings with `-e`. The three runs from section 4 become:

```powershell
# Chrome, Edge and Firefox, 10 repetitions each (one command per browser)
docker compose exec -e MONITOR_RESOURCES=false playwright_tests pytest -m smoke --browser-channel chrome --count=10 --reset-app-data

# Chrome, 50 repetitions
docker compose exec -e MONITOR_RESOURCES=false playwright_tests pytest -m smoke --browser-channel chrome --count=50 --reset-app-data

# Chrome, 50 repetitions, with CPU and memory recording
docker compose exec -e MONITOR_RESOURCES=true playwright_tests pytest -m smoke --browser-channel chrome --count=50 --reset-app-data
```

For Edge and Firefox, replace `--browser-channel chrome` with `--browser-channel msedge` or `--browser firefox`.

Good to know:
- Results appear in this folder's `reports/` and `logs/`.
- Changes to `tests/`, `pages/`, `utils/`, `monitoring/` and `data/` apply immediately. After changing `conftest.py`, `pyproject.toml`, `Dockerfile` or `requirements.txt`, rebuild: `docker compose build`, then `docker compose up -d --force-recreate`.
- The app's data folder is mounted into the container for `--reset-app-data`. Set `AUT_STORAGE_DIR` to the app's `backend/app/storage` folder before starting the container if it is not at the default location (see `docker-compose.yml`).
- The image contains Chrome and Edge (versions in `/opt/browser-versions.txt`) and Playwright's Chromium and Firefox. To install specific Chrome and Edge versions, set `CHROME_VERSION` and `EDGE_VERSION` before `docker compose build` (only the current Chrome release can be installed).
- Tests always run headless in Docker.

## 8. Measurement series with both frameworks

To run this suite and the [Selenium version](https://github.com/alexduta-tech/selenium-python-framework) many times in a row, alternating the two frameworks and keeping every report, use `run_measurements.sh` from [test-metrics-analyzer](https://github.com/alexduta-tech/test-metrics-analyzer). Its README explains how to run it. The test cases are described in the app's [TEST_CASES.md](https://github.com/alexduta-tech/automation-lab/blob/main/TEST_CASES.md).

## Project structure

```
.
├── conftest.py      # test setup: browser per test, window size, timeouts, screenshots, data reset, CPU and memory recording
├── pages/           # page objects
├── tests/           # tests
├── utils/           # settings, waits, test data, logging
├── monitoring/      # CPU and memory recording
├── data/            # test files
├── Dockerfile, docker-compose.yml, run_playwright_docker.bat
├── pyproject.toml   # pytest settings
└── requirements.txt
```

## How to cite

If you use this repository in your work, please cite it as described in [CITATION.cff](CITATION.cff) (on GitHub: "Cite this repository").

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
