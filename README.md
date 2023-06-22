# water-controller

I purchased a cheap hose controller for my garden. It worked ok, but was not flexible enough to do all the things I want. Here are my goals:

* highly scalable to many zones (hundreds of zones)
* each zone can be individually tested to make sure it works
* flexible system that waters a zone only when wanted or needed
* plugins for scheduling
* plugins for to decide whether to water or not
* plugins for controllers to turn water on and off 

If you want a web interface with simple configuration, this is not the project for you.

# Scheduling Plugins

Scheduling plugins control when watering should occur.

## Interval

The *interval plugin* allows for scheduling of watering for an interval defined using weeks, days, hours, minutes, or seconds. See [here](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/interval.html?highlight=interval). Examples:

* water once per day 
* water every other day
* water once per week
* water every 11 seconds

## cron

The *cron plugin* allows for much more control over scheduling. See [here](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html?highlight=cron) for more detail. One or more cron schedules can be combined to make extremely specific and complex schedules. Examples:

* water every minute
* water every odd hour all day
* water every hour only on Tuesdays
* water every even hour between 6am and 11am, on Wednesdays, during the month of July (crazy specific)

# Should I Water Plugins

Once a schedule fires a watering job, zero or more plugins decide whether or not that job waters a specific zone. The first plugin to fail means the current scheduled watering should be skipped for this zone. You can configure as many plugins as you want and they always run in the order given. When combined with the schedulers above, this allows for really specific waterings like:

* From November through December, water zone 1 every 17 minutes for 22 seconds, but only during the hotest part of the day, and only if it hasn't rained 5mm or more during the past 24 hours

## Has it Rained

This plugin grabs X hours of data from Meteostat for the weather station nearest the location provided and checks to see if the total percipitation is over the limit in mm you provide.

This plugin can be used multiple times if you like to check for total rain amounts over the last 8 hours, 24 hours, week... whatever you choose.

## Sun Check

This plugin uses the astral library with dawn, dusk, noon, sunrise, and sunset as points in time for the location you provide at your time of year along with offsets so you can do things like:

* water only while the sun is up
* water only during the hotest part of the day from 1 hour before noon to 3 hours after noon. Note that *noon* is NOT 12pm and that the local time for *noon* shifts daily.

## other possible plugins

Moisture sensors like resistive or capacitive could be added as plugins. These don't seem very dependable, so I have not implemented them yet.

Rain sensors could be added to give an exact rain amount in your location. I have a Meteostat weather station a couple of miles away, so I don't really need this.

Temperature would be easy. I'd guess that most people don't want to water if it is freezing.

# Controller Plugins

Controllers turn the water on and off. Each controller is connected to one or more relays that control a valve.

## Raspberry PIs and much more

Blinka controllers include a vast [list](https://circuitpython.org/blinka) of single board computers.

