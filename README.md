MicroPython WS2812 driver
=========================

MicroPython driver for WS2812, WS2812B, and compatible RGB LEDs. These are
popular RGB LEDs used for example in AdaFruit NeoPixels rings, strips, boards,
etc.

Driver has been tested with up to 240 LEDs (4m of NeoPixels stripe) but it
should work with much more LEDs.

Installation
------------

Copy `ws2812.py` file to your pyboard.

Usage
-----

```
from ws2812 import WS2812
chain = WS2812(spi_bus=1, led_count=4)
data = [
    (255, 0, 0),    # red
    (0, 255, 0),    # green
    (0, 0, 255),    # blue
    (85, 85, 85),   # white
]
chain.show(data)
```

There are files `example_simple.py` and `example_advanced.py` prepared for
NeoPixels ring (or similar) with 16 RGB LEDs. If you have it connected to SPI
bus 1 then just copy `example_simple.py` or `example_advanced.py` as `main.py`
to your pyboard and reset your pyboard.

Video of `example_advanced.py` in action: http://youtu.be/ADYxiG40UJ0

`example_240_leds.py` are some animations for 4 meters of NeoPixels strip with
240 RGB LEDs. In action video: http://youtu.be/vb5l3h1-TqA

Wiring
------

WS2812 driver is using SPI bus. Connect your LED's input wire to the SPI bus 1
MOSI (pin X8 on pyboard) or SPI bus 2 MOSI (pin Y8 on pyboard). Connect LED's
power and ground wires to VIN and GND on pyboard. The same applies for LED
rings, stripes, etc. (they have always one input wire).

USB may be insufficient for powering lots of RGB LEDs. You may need to use
additional power source.

More info & Help
----------------

You can check more about the MicroPython project here: http://micropython.org

Discussion about this driver: http://forum.micropython.org/viewtopic.php?f=5&t=394

Changelog
---------

* 1.3 - Allow updating only part of the buffer; re-add send_buf
* 1.2 - Disable IRQ feature removed. (It's not neccesary in newer versions of
  MicroPython.)
* 1.1 - Speed optimisations.
* 1.0 - First release.
