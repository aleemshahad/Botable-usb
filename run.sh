#!/bin/bash
# Launcher script for Bootable USB Creator

echo "=========================================="
echo "   Bootable USB Creator"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3 first."
    exit 1
fi

# Run the application
python3 "$(dirname "$0")/bootable_usb_creator.py"
