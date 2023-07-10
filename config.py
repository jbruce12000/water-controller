import logging
import board

log_level = logging.INFO
log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'

# location is used in a few plugins
my_lat = 33.858740179964144
my_lon = -84.2213734421551

# check meteostat for location nearest me and if it has rained 5mm or more
# in the past 24 hours, skip the current watering
rained_lately = ('should_i_water_plugins','Meteostat_Rain_Check',
        {'latitude'          : my_lat,
         'longitude'         : my_lon,
         'rain_search_hours' : 24,
         'rain_limit_mm'     : 5 } )

# check meteostat for location nearest me and if avg relative humidity
# over the past search_hours is above threshold ,skip the current watering
is_humidity_low = ('should_i_water_plugins','Meteostat_Humidity_Check',
        {'latitude'          : my_lat,
         'longitude'         : my_lon,
         'search_hours'      : 1,
         'avg_humidity_below': 97 } )

# only water one hour after sunrise to one hour before sundown
is_sun_up = ('should_i_water_plugins','Sun_Check',
        {'latitude'          : my_lat,
         'longitude'         : my_lon,
         'start'             : [ 'sunrise', { 'hours': +1 }],
         'end'               : [ 'sunset', { 'hours': -1 }] })

# only water during hotest four hours of the day
is_hotest_part_of_day = ('should_i_water_plugins','Sun_Check',
        {'latitude'          : my_lat,
         'longitude'         : my_lon,
         'start'             : [ 'noon', { 'hours': -1 }],
         'end'               : [ 'noon', { 'hours': +3 }] })

# only water if its above freezing
is_above_freezing = ('should_i_water_plugins','Meteostat_Temp_Check',
        {'latitude'          : my_lat,
         'longitude'         : my_lon,
         'search_hours'      : 24,
         'avg_temp_above': 0 } )

# check if a storage tank has water
#storage_tank1_has_water = ('should_i_water_plugins','Tank_Check',
#        {'name'              : 'rain-storage-1',
#         'input_pin'         : board.D22 })

# good for testing
always_water = ('should_i_water_plugins','Always_Water',{})

# good for disabling watering of a zone, but still making sure
# the schedule is set correctly and all plugins work as expected
never_water = ('should_i_water_plugins','Never_Water',{})

should_i_water_plugins1 = [ is_above_freezing, is_hotest_part_of_day ]
should_i_water_plugins2 = [ always_water, never_water ]

controller1 = ('controller_plugins','Dummy_Controller', {})
#controller2 = ('blinka','Blinka_GPIO', {'output_pin': board.D23 })

# water every minute for 22 secs between 8am and 3pm
duration_22s = ('duration_plugins','Static_Duration', {'seconds' : 22 })
cron1 = {'hour':'8-14', 'minute':'*/1','misfire_grace_time':5 }
# apscheduler jobs scaling tested with 100 zones
scheduler1 = ('scheduler_plugins','Cron', cron1)

# water every 5 minutes for 15 secs between 3pm and midnight
duration_15s = ('duration_plugins','Static_Duration',{'seconds' : 15 })
cron2 = { 'hour':'15-23', 'minute':'*/1','misfire_grace_time':5 }
scheduler2 = ('scheduler_plugins','Cron', cron2)

# complex cron schedule
# water every 2 minutes for 15 secs between 12pm and 3pm and
# water every 5 minutes for 15 secs between 3pm and midnight
multi_cron = [cron1, cron2]
schedule3 = ('scheduler_plugins','Cron', multi_cron) 

# water every minute for 10 secs
every_minute = ('scheduler_plugins','Interval',{ 'minutes' : 1 })

#scheduler2 = ('dummy_scheduler_plugin','Dummy_Scheduler', {})

zones = [ ('box1',controller1,schedule3,duration_15s,should_i_water_plugins1), 
          ('box2',controller1,schedule3,duration_15s,should_i_water_plugins2), 
          ('box3',controller1,every_minute,duration_22s,is_sun_up), 
        ]
