#!/bin/sh

# Directory to check
DATA_DIR="/src/.data/default"

# Check if the directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Initializing data directory"
  mkdir -p "$DATA_DIR"
fi
