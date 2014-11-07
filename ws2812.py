import gc
import pyb


class WS2812:
    """
    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
    of LEDs. Example of use:

    chain = WS2812(spi_bus=1, led_count=4)
    data = [
        (255, 0, 0),    # red
        (0, 255, 0),    # green
        (0, 0, 255),    # blue
        (85, 85, 85),   # white
    ]
    chain.show(data)
    """
    buf_bytes = (0x11, 0x13, 0x31, 0x33)

    def __init__(self, spi_bus=1, led_count=1, intensity=1, disable_irq=True):
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        * disable_irq = disable IRQ while sending data over SPI
        """
        self.led_count = led_count
        self.intensity = intensity
        self.disable_irq = disable_irq

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count * 3 * 4
        self.buf = bytearray(self.buf_length)

        # SPI init
        self.spi = pyb.SPI(spi_bus, pyb.SPI.MASTER, baudrate=3200000, polarity=0, phase=1)

        # turn LEDs off
        self.show([])

    def show(self, data):
        """
        Sends RGB data. Expected data = [(R, G, B), ...] where R, G and B are
        intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Sends buffer over SPI.
        """
        if self.disable_irq:
            pyb.disable_irq()
            self.spi.send(self.buf)
            pyb.enable_irq()
        else:
            self.spi.send(self.buf)
        gc.collect()

    def fill_buf(self, data):
        """
        Fills buffer with bytes.
        """
        i = 0
        for byte in self.data_to_bytes(data):
            self.buf[i] = byte
            i += 1
        # turn off the rest of the LEDs
        while i < self.buf_length:
            self.buf[i] = self.buf_bytes[0]
            i += 1

    def data_to_bytes(self, data):
        """
        Converts data to bytes. Note: Order of colors is changed from RGB to GRB
        because WS2812 LED has GRB order of colors.
        """
        for red, green, blue in data:
            for byte in self.color_to_bytes(green):
                yield byte
            for byte in self.color_to_bytes(red):
                yield byte
            for byte in self.color_to_bytes(blue):
                yield byte

    def color_to_bytes(self, color):
        """
        Yields 4 buffer bytes representing color value (1 byte for each 2 bits).
        """
        color = int(color * self.intensity)
        for i in range(4):
            yield self.buf_bytes[(color & 0xC0) >> 6]
            color <<= 2
