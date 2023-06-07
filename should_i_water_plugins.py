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
        #print(data)

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
