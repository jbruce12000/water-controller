from water_controller import Should_I_Water_Plugin, log

class Always_Water(Should_I_Water_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
    def water_now(self):
        return True

class Never_Water(Should_I_Water_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
    def water_now(self):
        return False

##############################################################################
# add something like this to config.py
#
#    ('meteostat_rain_plugin','Meteostat_Rain_Check',
#        {'latitude'          : 33.858740179964144,
#         'longitude'         : -84.2213734421551,
#         'rain_search_hours' : 24,
#         'rain_limit_mm'     : 5 } )
#
# This plugin can be used multiple times if you like. That way you can
# do things like check the last 8 hours and then check that last 24 hours
# for a different limit etc.
class Meteostat_Rain_Check(Should_I_Water_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        self.lat = opts["latitude"]
        self.lon = opts["longitude"]
        self.rain_search_hours = opts["rain_search_hours"]
        self.rain_limit = opts["rain_limit_mm"]
        self.station = self.get_nearby_weather_station()

    def water_now(self):
        from datetime import datetime, timedelta
        from meteostat import Hourly
        start = datetime.now() - timedelta(hours=self.rain_search_hours)
        end = datetime.now()

        # Get hourly data
        data = Hourly(self.station, start, end)
        data = data.fetch()
        # print(data)

        if (data.prcp.sum() >= self.rain_limit):
            log.info("%s - rainfall of %dmm in past %d hours at or over %dmm limit" %(self.zone, data.prcp.sum(), self.rain_search_hours, self.rain_limit))
            return False
        log.info("%s - rainfall of %dmm in past %d hours below %dmm limit" %(self.zone, data.prcp.sum(), self.rain_search_hours, self.rain_limit))
        return True

    def get_nearby_weather_station(self):
        from meteostat import Stations
        stations = Stations()
        stations = stations.nearby(self.lat, self.lon)
        return stations.fetch(1)

#################################################################
# if it's X hours after sunrise and Y hours before sunset, water
# set something like this in config.py
#
# is_sun_up = ('should_i_water_plugins','Sun_Check',
#         {'latitude'          : 33.858740179964144,
#          'longitude'         : -84.2213734421551,
#          'start'             : [ 'sunrise', { 'hours': +1 }],
#          'end'               : [ 'sunset', { 'hours': -1 }] })
#
# start and end can contain any of 'dawn','dusk','noon','sunrise','sunset'
# the offsets are datetime.timedelta and added to start and end. you could use
# minutes or seconds etc.
class Sun_Check(Should_I_Water_Plugin):
    def __init__(self,zone,opts):
        super().__init__()
        self.zone = zone
        self.lat = opts["latitude"]
        self.lon = opts["longitude"]
        self.start = opts['start'][0]
        self.start_offset = opts['start'][1]
        self.end = opts['end'][0]
        self.end_offset = opts['end'][1]
        self.set_location()

    def set_location(self):
        self.get_timezone()
        from astral import LocationInfo
        self.loc = LocationInfo(name=self.zone,
                   latitude=self.lat,
                   longitude=self.lon,
                   timezone=self.tz)

    def get_timezone(self):
        import timezonefinder 
        tf = timezonefinder.TimezoneFinder()
        timezone_str = tf.certain_timezone_at(lat=self.lat, lng=self.lon)
        self.tz = timezone_str

    def water_now(self):
        import datetime
        from astral.sun import sun
        now = datetime.datetime.now()
        times = sun(self.loc.observer, now, tzinfo=self.loc.timezone)
        #import pdb; pdb.set_trace()
        #for key in ['dawn', 'dusk', 'noon', 'sunrise', 'sunset']:
        #    log.info('%s : %s' % (key,times[key]))
        now = now.replace(tzinfo=times['sunrise'].tzinfo)
        t1 = times[self.start] + datetime.timedelta(**self.start_offset)
        t2 = times[self.end] + datetime.timedelta(**self.end_offset)
        if (now >= t1) and (now <= t2):
            log.info("%s - sun check: %s between %s and %s" % (self.zone,now,t1,t2))
            return True
        log.info("%s - sun check: %s not between %s and %s" % (self.zone,now,t1,t2))
        return False
