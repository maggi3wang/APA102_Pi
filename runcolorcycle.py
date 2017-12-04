#!/usr/bin/env python3
"""Sample script to run a few colour tests on the strip."""
import colorschemes
import sys

NUM_LED = 60

while True:
    MY_CYCLE = colorschemes.Custom(num_led=NUM_LED, pause_value=0,
                               num_steps_per_cycle=100, num_cycles=sys.maxsize)
    MY_CYCLE.start()

print('Finished the test')
