"""This module contains a few concrete colour cycles to play with"""
import pyowm
import math
import RPi.GPIO as GPIO
import time
import os

from colorcycletemplate import ColorCycleTemplate

class StrandTest(ColorCycleTemplate):
    """Runs a simple strand test (9 LEDs wander through the strip)."""

    color = None

    def init(self, strip, num_led):
        self.color = 0x000000  # Initialize with black

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        # One cycle = The 9 Test-LEDs wander through numStepsPerCycle LEDs.
        if current_step == 0:
            self.color >>= 8  # Red->green->blue->black
        if self.color == 0:
            self.color = 0xFF0000  # If black, reset to red
        len = 9
        if num_led - 1 < len:
            len = num_led - 1 
        # The head pixel that will be turned on in this cycle
        head = (current_step + len) % num_steps_per_cycle
        tail = current_step # The tail pixel that will be turned off
        strip.set_pixel_rgb(head, self.color)  # Paint head
        strip.set_pixel_rgb(tail, 0)  # Clear tail

        return 1 # Repaint is necessary


class TheaterChase(ColorCycleTemplate):
    """Runs a 'marquee' effect around the strip."""
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        # One cycle = One trip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # Note: For a smooth transition between cycles, numStepsPerCycle must
        # be a multiple of 7
        start_index = current_step % 7 # One segment is 2 blank, and 5 filled
        color_index = strip.wheel(int(round(255/num_steps_per_cycle *
                                            current_step, 0)))
        for pixel in range(num_led):
            # Two LEDs out of 7 are blank. At each step, the blank
            # ones move one pixel ahead.
            if ((pixel+start_index) % 7 == 0) or ((pixel+start_index) % 7 == 1):
                strip.set_pixel_rgb(pixel, 0)
            else: strip.set_pixel_rgb(pixel, color_index)
        return 1


class RoundAndRound(ColorCycleTemplate):
    """Runs three LEDs around the strip."""

    def init(self, strip, num_led):
        strip.set_pixel_rgb(0, 0xFF0000)
        strip.set_pixel_rgb(1, 0xFF0000, 5) # Only 5% brightness
        strip.set_pixel_rgb(2, 0xFF0000)

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        # Simple class to demonstrate the "rotate" method
        strip.rotate()
        return 1




class Solid(ColorCycleTemplate):
    """Paints the strip with one colour."""

    def init(self, strip, num_led):
        for led in range(0, num_led):
            strip.set_pixel_rgb(led,0xFFFFFF,5) # Paint 5% white

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        # Do nothing: Init lit the strip, and update just keeps it this way
        return 0



class Rainbow(ColorCycleTemplate):
    """Paints a rainbow effect across the entire strip."""
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        # One cycle = One trip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # -> LED 0 goes from index 0 to 254 in numStepsPerCycle cycles.
        #     So it might have to step up more or less than one index
        #     depending on numStepsPerCycle.
        # -> The other LEDs go up to 254, then wrap around to zero and go up
        #     again until the last one is just below LED 0. This way, the
        #     strip always shows one full rainbow, regardless of the
        #     number of LEDs
        scale_factor = 255 / num_led # Index change between two neighboring LEDs
        start_index = 255 / num_steps_per_cycle * current_step # LED 0
        for i in range(num_led):
            # Index of LED i, not rounded and not wrapped at 255
            led_index = start_index + i * scale_factor
            # Now rounded and wrapped
            led_index_rounded_wrapped = int(round(led_index, 0)) % 255
            # Get the actual color out of the wheel
            pixel_color = strip.wheel(led_index_rounded_wrapped)
            strip.set_pixel_rgb(i, pixel_color)
        return 1 # All pixels are set in the buffer, so repaint the strip now
    
    

class Custom(ColorCycleTemplate):
    
    GPIO.setmode(GPIO.BOARD)
    numThermometerLEDs = 0
    
    def init(self, strip, num_led):
        global numThermometerLEDs
        owm = pyowm.OWM('ae594305a07bf60780bb6bb61cce49a8')
        observation = owm.weather_at_place("Cambridge, US")
        w = observation.get_weather()
        temperature = w.get_temperature('fahrenheit')['temp']
        print(temperature)
        numThermometerLEDs = math.floor(temperature / 10)
        print(numThermometerLEDs)
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        global numThermometerLEDs
        #define the pin that goes to the circuit
        pin_to_circuit = 7
        count = 0
      
        #Output on the pin for 
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)

        #Change the pin back to input
        GPIO.setup(pin_to_circuit, GPIO.IN)
      
        #Count until the pin goes high
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
            count += 1

        photoresistor_threshold = 1500
        if (count < photoresistor_threshold) :     
            numTempLeds = 10      
            
            for led in range(0, numThermometerLEDs):
                strip.set_pixel_rgb(led, 0x00FFFF, 5)
            
            for led in range(numThermometerLEDs, numTempLeds) :
                strip.set_pixel_rgb(led, 0xFFFFFF, 5)
                
            # Do nothing: Init lit the strip, and update just keeps it this way
            num_led -= numTempLeds
            scale_factor = 255 / (num_led - 2 * numTempLeds) # Index change between two neighboring LEDs
            start_index = 255 / num_steps_per_cycle * current_step # LED 0
            for i in range(num_led):
                i+= numTempLeds
                # Index of LED i, not rounded and not wrapped at 255
                led_index = start_index + i * scale_factor
                # Now rounded and wrapped
                led_index_rounded_wrapped = int(round(led_index, 0)) % 255
                # Get the actual color out of the wheel
                pixel_color = strip.wheel(led_index_rounded_wrapped)
                strip.set_pixel_rgb(i, pixel_color)
                
            os.system('vcgencmd display_power 1')   # Turns monitor on
        else :
            for led in range(60) :                  
                strip.set_pixel_rgb(led, 0x000000, 0)
            os.system('vcgencmd display_power 0')   # Turns monitor off

        return 1
    
