#!/usr/bin/env python3
"""Sample script to run a few colour tests on the strip."""
import colorschemes

NUM_LED = 60

MY_CYCLE = colorschemes.Custom(num_led=NUM_LED, pause_value=0,
                               num_steps_per_cycle=255, num_cycles=1000)
MY_CYCLE.start()

print('Finished the test')
