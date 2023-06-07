#!/usr/bin/env python
import time
import logging
import config
import sys
from datetime import timedelta,datetime

logging.basicConfig(level=config.log_level, format=config.log_format)
log = logging.getLogger("water-controller")
log.info("Starting water controller")

class Should_I_Water_Plugin(object):
    def __init__(self):
        pass
    def water_now(self):
        # children must implement this
        # must return True or False
        pass

class Controller_Plugin(object):
    def __init__(self):
        pass
    def water_on(self):
        # children must implement this
        # must turn water on
        pass
    def water_off(self):
        # children must implement this
        # must turn water on
        pass

class Scheduler_Plugin(object):
    def __init__(self):
        pass

class Zone(object):
    def __init__(self,config):
        self.name = config[0]
        self.controller_config = config[1]
        self.scheduler_config = config[2]
        self.should_i_water_config = config[3]
        self.controller = self.load_controller()
        self.scheduler = self.load_scheduler()
        self.should_i_water_plugins = self.load_should_i_water_plugins()

    def load_controller(self):
        (module_name,class_name,opts) = self.controller_config
        my_module = __import__(module_name)
        my_class = getattr(my_module, class_name)
        return my_class(self,opts)

    def load_scheduler(self):
        (module_name,class_name,duration,opts) = self.scheduler_config
        my_module = __import__(module_name)
        my_class = getattr(my_module, class_name)
        self.duration = duration
        #return my_class(self.water_on,opts)
        return my_class(self,opts)

    def load_should_i_water_plugins(self):
        #import pdb;pdb.set_trace()
        plugins = []
        if type(self.should_i_water_config) is list:
            for (module_name,class_name,opts) in self.should_i_water_config:
                my_module = __import__(module_name)
                my_class = getattr(my_module, class_name)
                my_instance = my_class(self,opts)
                plugins.append(my_instance)
        else:
            (module_name,class_name,opts) = self.should_i_water_config
            my_module = __import__(module_name)
            my_class = getattr(my_module, class_name)
            my_instance = my_class(self,opts)
            plugins.append(my_instance)
        return plugins

    def should_i_water(self):
        for plugin in self.should_i_water_plugins:
            if plugin.water_now() == False:
                return False
        return True

    def water_on(self):
        if self.should_i_water() == False:
            log.info("%s - water skipping" % self)
            return
        self.controller.water_on()
        log.info("%s - water on duration=%ds" % (self,timedelta(**self.duration).seconds))
        time.sleep(timedelta(**self.duration).seconds)
        self.water_off()

    def water_off(self):
        self.controller.water_off()
        log.info("%s - water off" % self)

    def __str__(self):
        return "zone %s" % self.name

class Water_Controller(object):

    def __init__(self,zones):
        self.zone_config = zones
        self.zones = []
        self.load_zones()

    def load_zones(self):
        for z_config in self.zone_config:
            z = Zone(z_config)
            self.zones.append(z)
        log.info("%d zone[s] loaded" % len(self.zones))

class Test_Zone(object):

    def __init__(self,zones,zone_name):
        self.zone_config = zones
        self.zone = None
        self.test_zone(zone_name)

    def test_zone(self, searchfor):
        for z_config in self.zone_config:
            if z_config[0] == searchfor:
                test_scheduler = ('scheduler_plugins', 'Interval',
                    {'seconds' : 10 }, 
                    {'seconds' : 20, 'start_date': datetime.now()+timedelta(seconds=1)})
                always_water = ('should_i_water_plugins','Always_Water',{})
                #import pdb; pdb.set_trace()
                self.zone = Zone((z_config[0], z_config[1],
                    test_scheduler, always_water))
        if self.zone is None:
            log.error("zone %s not found" % searchfor)
            sys.exit()

if __name__== "__main__":
    import optparse
    parser = optparse.OptionParser("usage: water-controller.py --test zone_name")
    parser.add_option("-t", "--test", dest="test_zone",
        type="string", help="zone name to test. on 10s then off 10s forever.")
    (options, args) = parser.parse_args()

    if options.test_zone:
        test = Test_Zone(config.zones, options.test_zone)
    else:
        wc = Water_Controller(config.zones)

    while True:
      time.sleep(1)
