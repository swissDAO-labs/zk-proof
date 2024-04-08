FROM --platform=linux/amd64 node:lts-bookworm-slim

SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt update && apt install -y curl bash git tar gzip libc++-dev python3 python3-pip python3-venv

# Install Nargo
RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash
ENV PATH="/root/.nargo/bin:$PATH"

# Run noirup command to install Nargo
RUN noirup

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install FastAPI and Uvicorn in the virtual environment
RUN pip install --upgrade pip && pip install flask fastapi uvicorn

# Copy your FastAPI application code into the container
COPY . /app

WORKDIR /app

# Copy Nargo.toml into the container
COPY Nargo.toml /app/Nargo.toml

# Your other Dockerfile instructions...

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
