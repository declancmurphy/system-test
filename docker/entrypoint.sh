#!/bin/sh

echo "Starting Xvfb for headless browser testing..."
Xvfb :99 -screen 0 1920x1080x24 &

echo "Using browser: ${BROWSER}"

# Execute test run using specified path in .env (to define scope)
pytest -s -vv ${ROOT_DIR}/tests/${TEST_PATH} --html=docs/reports/test_dummy_report.html

# Keep alive command for debug if specified in .env
if [ "$KEEP_ALIVE" == "1" ]; then
    tail -f /dev/null
fi