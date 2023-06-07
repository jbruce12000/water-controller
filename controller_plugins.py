from water_controller import Controller_Plugin, log

class Dummy_Controller(Controller_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        self.water_off()
    def water_on(self):
        pass
    def water_off(self):
        pass

# this works for all blinka supported boards (raspberry pis etc)
# see https://circuitpython.org/blinka
class Blinka_GPIO(Controller_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        import board 
        import digitalio
        self.gpio = digitalio.DigitalInOut(opts["output_pin"])
        self.gpio.direction = digitalio.Direction.OUTPUT
        self.water_off()

    def water_on(self):
        self.gpio.value = True
    def water_off(self):
        self.gpio.value = False
