from water_controller import Controller_Plugin, log

class Dummy_Controller(Controller_Plugin):
    def __init__(self,zone,opts):
        super().__init__(zone)
    def water_on(self):
        super().water_on()
    def water_off(self):
        super().water_off()

# this works for all blinka supported boards (raspberry pis etc)
# see https://circuitpython.org/blinka
class Blinka_GPIO(Controller_Plugin):
    def __init__(self,zone,opts):
        import board 
        import digitalio
        self.gpio = digitalio.DigitalInOut(opts["output_pin"])
        self.gpio.direction = digitalio.Direction.OUTPUT
        super().__init__(zone)

    def water_on(self):
        self.gpio.value = True
        super().water_on()
    def water_off(self):
        self.gpio.value = False
        super().water_off()
