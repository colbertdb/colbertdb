# Use Python 3.12 as the base image for the builder stage
FROM python:3.11-slim-bookworm as builder

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes wget tar pipx && \
    rm -rf /var/lib/apt/lists/*

# Set the PATH environment variable to include pipx binaries
ENV PATH="/root/.local/bin:${PATH}"

# Install Poetry using pipx
RUN pipx install poetry && \
    pipx inject poetry poetry-plugin-bundle

# Set the working directory
WORKDIR /src

# Copy the current directory contents into the container
COPY . .

# Conditionally create a virtual environment and install the main dependencies using Poetry
RUN if [ "$ENV" = "production" ]; then poetry bundle venv --python=/usr/bin/python3 --only=main /venv; else poetry bundle venv --python=/usr/bin/python3 /venv; fi

# Download and extract the ColBERTv2.0 checkpoints
RUN mkdir -p .checkpoints && \
    wget -qO- https://downloads.cs.stanford.edu/nlp/data/colbert/colbertv2/colbertv2.0.tar.gz | tar xvz -C .checkpoints

# Copy and run the initialization script
COPY initialize_data.sh /src/

# Use Python 3.12 as the base image for the final stage
FROM python:3.11

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:${PATH}"
ENV GIT_PYTHON_REFRESH="quiet"

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy the application code and checkpoints from the builder stage
COPY --from=builder /src/colbertdb /src/colbertdb
COPY --from=builder /src/.checkpoints /src/.checkpoints
COPY --from=builder /src/initialize_data.sh /src/initialize_data.sh

# Set the working directory
WORKDIR /src

# Install necessary runtime dependencies
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3.11-dev && \
    rm -rf /var/lib/apt/lists/*


# Run the initialization script
RUN chmod +x /src/initialize_data.sh && /src/initialize_data.sh
