# -*- coding: utf-8 -*-

import pyb
import math

from ws2812 import WS2812


ring = WS2812(spi_bus=1, led_count=16, intensity=0.1)


def data_generator(led_count):
    data = [(0, 0, 0) for i in range(led_count)]
    step = 0
    while True:
        red = int((1 + math.sin(step * 0.1324)) * 127)
        green = int((1 + math.sin(step * 0.1654)) * 127)
        blue = int((1 + math.sin(step * 0.1)) * 127)
        data[step % led_count] = (red, green, blue)
        yield data
        step += 1


for data in data_generator(ring.led_count):
    ring.show(data)
    pyb.delay(100)
