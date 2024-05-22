#!/bin/sh

# Create the directory
mkdir -p /src/.data

# Run the warming script
python /src/scripts/warm.py

# Execute the command provided as arguments
exec "$@"