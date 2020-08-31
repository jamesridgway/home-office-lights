#!/usr/bin/env python3

# -------------------------------------------------------------------------------------------------
# Basic script for turning off the lights.
# -------------------------------------------------------------------------------------------------

from strip_manager import StripManager

if __name__ == '__main__':
    strip_manager = StripManager.default()
    strip_manager.clear()
