import logging

log_level = logging.INFO
log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'

# check meteostat for location nearest me and if it has rained 5mm or more
# in the past 24 hours, skip the current watering
rained_lately = ('should_i_water_plugins','Meteostat_Rain_Check',
        {'latitude'          : 33.858740179964144,
         'longitude'         : -84.2213734421551,
         'rain_search_hours' : 24,
         'rain_limit_mm'     : 5 } )

# only water one hour after sunrise to one hour before sundown
is_sun_up = ('should_i_water_plugins','Sun_Check',
        {'latitude'          : 33.858740179964144,
         'longitude'         : -84.2213734421551,
         'start'             : [ 'sunrise', { 'hours': +1 }],
         'end'               : [ 'sunset', { 'hours': -1 }] })

# only water during hotest four hours of the day
is_hotest_part_of_day = ('should_i_water_plugins','Sun_Check',
        {'latitude'          : 33.858740179964144,
         'longitude'         : -84.2213734421551,
         'start'             : [ 'noon', { 'hours': -1 }],
         'end'               : [ 'noon', { 'hours': +3 }] })

always_water = ('should_i_water_plugins','Always_Water',{})
never_water = ('should_i_water_plugins','Never_Water',{})

should_i_water_plugins1 = [ always_water, rained_lately, is_hotest_part_of_day ]
should_i_water_plugins2 = [ always_water, never_water ]

controller1 = ('controller_plugins','Dummy_Controller', {})
#import board
#controller2 = ('blinka','Blinka_GPIO', {'output_pin': board.D23 })

# water every minute for 22 secs between 8am and 3pm
duration1 = {'seconds' : 22 }
cron1 = {'hour':'8-14', 'minute':'*/1','misfire_grace_time':5 }
# apscheduler jobs scaling tested with 100 zones
scheduler1 = ('scheduler_plugins','Cron', duration1, cron1)

# water every 5 minutes for 15 secs between 3pm and midnight
duration2 = {'seconds' : 15 }
cron2 = { 'hour':'15-23', 'minute':'*/1','misfire_grace_time':5 }
scheduler2 = ('scheduler_plugins','Cron', duration2, cron2)

# complex cron schedule
# water every 2 minutes for 15 secs between 12pm and 3pm and
# water every 5 minutes for 15 secs between 3pm and midnight
multi_cron = [cron1, cron2]
schedule3 = ('scheduler_plugins','Cron', duration2, multi_cron) 

# water every minute for 10 secs
#scheduler3 = ('scheduler_plugins','Interval', 
#        {'seconds' : 10 },
#        { 'minutes' : 1 })

#scheduler2 = ('dummy_scheduler_plugin','Dummy_Scheduler', {})

zones = [ ('box1',controller1, schedule3, should_i_water_plugins1), 
          ('box2',controller1, schedule3, never_water), 
        ]

#zones = [ ('box1',controller1, scheduler1, should_i_water_plugins1) ]
