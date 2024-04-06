FROM --platform=linux/amd64 node:lts-bookworm-slim

SHELL ["/bin/bash", "-c"]

# Install dependencies for both Nargo and FastAPI
RUN apt update && apt install -y curl bash git tar gzip libc++-dev python3 python3-pip

# Install Nargo
RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash

# Set PATH for Nargo
ENV PATH="/root/.nargo/bin:$PATH"

# Install FastAPI and Uvicorn
RUN pip3 install fastapi uvicorn

# Copy your FastAPI application code into the container
# Ensure your FastAPI application entry point is in app/main.py or adjust the COPY destination accordingly
COPY ./app /app

# Optional: If your Nargo and FastAPI services need to share files, ensure they are properly copied into the container
# COPY ./your_nargo_project /path/to/nargo_project
RUN noirup

# Override the default ENTRYPOINT to use a script that starts both services
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
