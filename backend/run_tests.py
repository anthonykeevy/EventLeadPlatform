#!/usr/bin/env python3
"""
Test runner script for EventLead Platform
"""
import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """Run the test suite."""
    print("🧪 Running EventLead Platform Tests...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run pytest with specific options
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "--durations=10",  # Show 10 slowest tests
        "--markers=unit",  # Run unit tests by default
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"\n💥 Error running tests: {e}")
        return 1

def run_specific_tests(test_pattern: str):
    """Run specific tests matching a pattern."""
    print(f"🧪 Running tests matching: {test_pattern}")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    cmd = [
        sys.executable, "-m", "pytest",
        f"tests/{test_pattern}",
        "-v",
        "--tb=short",
        "--color=yes",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ Tests matching '{test_pattern}' passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

def run_auth_tests():
    """Run authentication tests specifically."""
    return run_specific_tests("test_auth_*.py")

def run_unit_tests():
    """Run only unit tests."""
    print("🧪 Running Unit Tests...")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-m", "unit",
        "-v",
        "--tb=short",
        "--color=yes",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All unit tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Unit tests failed with exit code {e.returncode}")
        return e.returncode

def run_integration_tests():
    """Run only integration tests."""
    print("🧪 Running Integration Tests...")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-m", "integration",
        "-v",
        "--tb=short",
        "--color=yes",
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All integration tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Integration tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "auth":
            exit_code = run_auth_tests()
        elif command == "unit":
            exit_code = run_unit_tests()
        elif command == "integration":
            exit_code = run_integration_tests()
        elif command == "help":
            print("Usage: python run_tests.py [command]")
            print("Commands:")
            print("  (no args) - Run all tests")
            print("  auth      - Run authentication tests")
            print("  unit      - Run unit tests only")
            print("  integration - Run integration tests only")
            print("  help      - Show this help message")
            exit_code = 0
        else:
            print(f"Unknown command: {command}")
            print("Use 'help' to see available commands")
            exit_code = 1
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)
