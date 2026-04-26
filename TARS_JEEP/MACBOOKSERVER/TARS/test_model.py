#!/usr/bin/env python3
"""
Test script for TARS model behaviors in console mode.
Runs predefined commands and checks responses.
"""

import subprocess
import sys
import time

def run_test(command, expected_contains):
    """Send command to TARS console and check response."""
    print(f"\nTesting: '{command}'")
    try:
        # Start TARS in console mode
        proc = subprocess.Popen(
            [sys.executable, 'main.py', '--console'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for ready
        time.sleep(5)  # Adjust for warmup

        # Send command
        proc.stdin.write(command + '\n')
        proc.stdin.flush()

        # Read output
        output, error = proc.communicate(timeout=30)

        print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

        # Check if expected in output
        if expected_contains.lower() in output.lower():
            print("✓ PASS")
            return True
        else:
            print("✗ FAIL")
            return False

    except Exception as e:
        print(f"Test failed: {e}")
        return False
    finally:
        proc.terminate()

# Test cases
tests = [
    ("hello", "Hello, I am TARS"),
    ("time", "current time"),
    ("what is 2+2", "4"),
    ("exit", "Shutting down"),
]

if __name__ == "__main__":
    print("Running TARS model tests...")
    passed = 0
    for cmd, exp in tests:
        if run_test(cmd, exp):
            passed += 1
    print(f"\n{passed}/{len(tests)} tests passed.")