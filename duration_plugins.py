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
