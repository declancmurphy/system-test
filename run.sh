#!/bin/bash

# Export absolute paths for use in scripts and framework setup, execution and teardown
# ROOT_DIR is the repo root directory 'system-test'
export ROOT_DIR="$(dirname "$(realpath "$0")")"
export REPORTS_DIR="${ROOT_DIR}/reports"
export REPORT_ARCHIVE_DIR="${ROOT_DIR}/report_archive"
export COMPOSE_FILE="${ROOT_DIR}/docker/docker-compose.yml"

# Load other environment variables from '.env'
export $(grep -v '^#' ${ROOT_DIR}/.env | xargs)

# Print configured vars
echo "Running tests: $TEST_PATH"
echo "Browser: $BROWSER"
echo "Headless mode: $HEADLESS"

# Clear previously generated report (that would have been archived)
rm -rf "${REPORTS_DIR}"
mkdir -p "${REPORTS_DIR}"

# Containerised run if LOCAL set to 0
if [ "$LOCAL" == "0" ]; then

  # for headful display forwarding
  xhost +local:docker

  # Check if REBUILD is set to 1 and rebuild without cache if so
  if [ "$REBUILD" == "1" ]; then
    echo "Rebuilding Docker images with no cache..."
    docker-compose -f "$COMPOSE_FILE" build --no-cache
  fi

  # Start services using Docker Compose
  docker-compose -f "$COMPOSE_FILE" up --build -d

  # Retrieve container process name for wait
  export CONTAINER_NAME=$(docker-compose -f "$COMPOSE_FILE" ps -q test-runner)

  # Stream logs out
  docker-compose logs -f test-runner &

  # blocks until execution completes/ret exit code (see entrypoit.sh)
  docker wait $CONTAINER_NAME && 

  # Copy report out from container after execution
  if [ "$(docker inspect -f '{{.State.ExitCode}}' test-runner)" == "0" ]; then
      docker cp test-runner:/system-test/docs/reports/. "${REPORTS_DIR}"
  else
      echo "Test execution failed. No reports copied."
  fi

  # Cleanup - teardown containers
  docker-compose down

elif [ "$LOCAL" == "1" ]; then
  # LOCAL=1 (add poetry/pyenv capability here: see "Improvements" in README)

  # Execute tests with specified test tag/path
  python3 -m pytest -v ${ROOT_DIR}/tests/${TEST_PATH} --html=reports/test_report.html

fi

# Create archived report to prevent future run override
CURRDATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "${REPORT_ARCHIVE_DIR}"
zip -r "${REPORT_ARCHIVE_DIR}/${CURRDATE}.zip" "${REPORTS_DIR}" > /dev/null 2>&1