#!/usr/bin/env python3
"""
Test runner for CFG QODER project.

This script runs all tests and generates coverage reports.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """Run all tests with coverage reporting."""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🧪 Running CFG QODER Test Suite...")
    print("=" * 50)
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--verbose",
        "--tb=short",
        "-x"  # Stop on first failure for now
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nTest execution completed with return code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("\n📊 Coverage report generated:")
            print("  - HTML: htmlcov/index.html")
            print("  - XML: coverage.xml")
        else:
            print("❌ Some tests failed. Check output above.")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

def run_specific_test(test_file):
    """Run a specific test file."""
    cmd = [
        sys.executable, "-m", "pytest",
        f"tests/{test_file}",
        "--verbose",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        exit_code = run_specific_test(test_file)
    else:
        # Run all tests
        exit_code = run_tests()
    
    sys.exit(exit_code)