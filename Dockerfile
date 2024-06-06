# Use the nvidia/cuda:12.4.1-devel-ubuntu22.04 as the base image
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Set the environment variable to noninteractive to avoid prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list, install necessary packages including Python 3.11, and clean up
RUN apt-get update && \
    apt-get install -y software-properties-common curl wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv python3-pip pipx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the PATH environment variable to include pipx binaries
ENV PATH="/root/.local/bin:${PATH}"

# Install conda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Create a new Conda environment and install faiss-gpu
RUN conda create -y -n myenv python=3.11 pytorch::faiss-gpu && \
    conda clean -ya

# Activate the Conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Set the PATH environment variable to include the Conda environment binaries
ENV PATH="/opt/conda/envs/myenv/bin:$PATH"

# Install Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Set the working directory
WORKDIR /src

# Copy the application code
COPY . /src/

# Install the main dependencies using Poetry
RUN poetry install --no-dev

# Set environment variables for CUDA
ENV GIT_PYTHON_REFRESH="quiet"
ENV LD_LIBRARY_PATH="/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH"
ENV TORCH_CUDA_ARCH_LIST="8.0 8.6 8.7"

# Ensure the entrypoint script is executable
RUN chmod +x /src/scripts/entrypoint.sh && \
    chmod +x /src/scripts/warm.py

ENTRYPOINT ["/src/scripts/entrypoint.sh"]
CMD ["uvicorn", "colbertdb.server.main:app", "--host", "0.0.0.0", "--port", "8080"]
