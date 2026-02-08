#!/usr/bin/env python3
"""
Quick test to verify Loom is working.
"""
import subprocess
import sys

def test_loom():
    """Run basic Loom commands to verify installation."""
    print("🧵 Testing Loom Pattern Weaver...")
    
    tests = [
        ["loom", "--version"],
        ["loom", "--help"],
        ["loom", "graph-stats"],
    ]
    
    for test in tests:
        print(f"\nRunning: {' '.join(test)}")
        try:
            result = subprocess.run(test, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Success")
            else:
                print(f"❌ Failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n🎉 All tests passed! Loom is working correctly.")
    return True

if __name__ == "__main__":
    if test_loom():
        sys.exit(0)
    else:
        sys.exit(1)
