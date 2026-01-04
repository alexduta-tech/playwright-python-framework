@echo off
REM Simple helper to build the image and keep the container running.
echo Building and starting playwright test framework container...

REM Build the Docker image using docker-compose.yml (creates image playwright_framework from service playwright_tests definition)
docker compose build

REM Start the service in detached/background mode so it stays running
docker compose up -d playwright_tests

echo.
REM Short usage hints: how to run tests and stop the service
echo Container is now running in the background!
echo.
echo To run tests in the running container, use:
echo    docker compose exec playwright_tests pytest -m smoke
echo.
echo To stop and remove containers, networks, and default volumes:
echo    docker compose down
echo.

pause