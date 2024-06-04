# Use the nvidia/cuda:12.4.1-devel-ubuntu22.04 as the base image
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Set the environment variable to noninteractive to avoid prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list, install necessary packages including Python 3.11, and clean up
RUN apt-get update && \
    apt-get install -y software-properties-common curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv python3-pip pipx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the PATH environment variable to include pipx binaries
ENV PATH="/root/.local/bin:${PATH}"

# Install Poetry using pipx
RUN pipx install poetry && \
    pipx inject poetry poetry-plugin-bundle

# Set the working directory
WORKDIR /src

# Copy the application code
COPY . /src/

# Create a virtual environment and install the main dependencies using Poetry
RUN poetry bundle venv --python=/usr/bin/python3.11 --only=main /venv

# Download and extract the ColBERTv2.0 checkpoints
RUN mkdir -p .checkpoints && \
    curl https://downloads.cs.stanford.edu/nlp/data/colbert/colbertv2/colbertv2.0.tar.gz | tar xvz -C .checkpoints

# Set environment variables for the virtual environment and CUDA
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:${PATH}"
ENV GIT_PYTHON_REFRESH="quiet"
ENV LD_LIBRARY_PATH="/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH"
ENV TORCH_CUDA_ARCH_LIST="8.0 8.6 8.7"

# Ensure the entrypoint script is executable
RUN chmod +x /src/scripts/entrypoint.sh && \
    chmod +x /src/scripts/warm.py

ENTRYPOINT ["/src/scripts/entrypoint.sh"]
CMD ["uvicorn", "colbertdb.server.main:app", "--host", "0.0.0.0", "--port", "8080"]
