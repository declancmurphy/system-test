# Dockerfile used to build the test environment/container, using python docker image
FROM python:3.10-slim

# Set working directory
WORKDIR /system-test

# Install dependencies for tests (listed in "dependencies.txt" at the root of this repo)
COPY apt_dependencies.txt /system-test/apt_dependencies.txt
RUN pip install --no-cache-dir -r apt_dependencies.txt

# Install browsers and their respective webdrivers & xvfb for headless
RUN apt-get update && apt-get install -y \
    wget xvfb \
    chromium-browser chromium-chromedriver 

# Set entry point 
COPY docker/entrypoint.sh /system-test/entrypoint.sh
RUN chmod +x /system-test/entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]
