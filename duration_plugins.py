from water_controller import Duration_Plugin, log
import datetime

# static duration, does not change, pass in any options
# that can be used with Datetime.timedelta
class Static_Duration(Duration_Plugin):
    def __init__(self,zone,opts):
        super().__init__(zone)
        self.opts = opts
        
    def duration(self):
        return datetime.timedelta(**self.opts)

# interesting to have a flow measurement where it reads the flow
# and sets a time based on flow. this way you could pass in the
# number of liters or gallons of water.
