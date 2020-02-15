"""
The purpose of that script is for testing and debug.
It displays information detected about your system, and
at the system time validate that the code work properly
"""

import helpers.environment as env
import helpers.vstudio as vstudio
import helpers.winsdk as winsdk

env.test_print()
vstudio.test_print()
winsdk.test_print()