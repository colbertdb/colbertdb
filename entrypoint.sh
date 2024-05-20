#!/bin/sh

# Create the directory
mkdir -p /src/.data

# Execute the command provided as arguments
exec "$@"