#!/usr/bin/env python3
"""
Test script to verify keyboard input handling.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from live_display import CrossPlatformInput

def test_keyboard_input():
    """Test keyboard input handling."""
    print("Testing Keyboard Input...")
    print("Press keys to test (ESC to exit):")
    print("  - Arrow keys (← →)")
    print("  - F key")
    print("  - P key")
    print("  - Q key")
    print("  - Any other key")
    print()

    input_handler = CrossPlatformInput()

    try:
        input_handler.setup()
        print("✓ Terminal setup complete")
        print("✓ Ready for input (press ESC to exit)")
        print()

        while True:
            key = input_handler.get_key()
            if key:
                if key == '\x1b':
                    # Check for arrow key sequence
                    next_key = input_handler.get_key()
                    if next_key == '[':
                        arrow_key = input_handler.get_key()
                        if arrow_key:
                            if arrow_key == 'D':
                                print("✓ Left arrow key detected")
                            elif arrow_key == 'C':
                                print("✓ Right arrow key detected")
                            elif arrow_key == 'A':
                                print("✓ Up arrow key detected")
                            elif arrow_key == 'B':
                                print("✓ Down arrow key detected")
                            else:
                                print(f"✓ Unknown arrow key: {repr(arrow_key)}")
                        else:
                            print("✓ ESC key detected (exiting)")
                            break
                    else:
                        print(f"✓ ESC sequence: {repr(next_key)}")
                elif key in ['f', 'F']:
                    print("✓ F key detected")
                elif key in ['p', 'P']:
                    print("✓ P key detected")
                elif key in ['q', 'Q']:
                    print("✓ Q key detected")
                else:
                    print(f"✓ Key pressed: {repr(key)}")

    except KeyboardInterrupt:
        print("\n✓ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input_handler.cleanup()
        print("\n✓ Terminal cleanup complete")
        print("✓ Test finished")

if __name__ == "__main__":
    test_keyboard_input()
