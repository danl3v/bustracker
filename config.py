'''
config.py
Daniel Levy

This is the configuration file for Bus Tracker.
'''

######## IMPORTS #######
import curses, os

####### CONSTANTS ######
MIN_UPDATE_DELAY = 10 # predictions will updated no more often than this many seconds (so we can be nice to nextbus server)
MAX_UPDATE_DELAY = 60 # predictions will updated at least every this many seconds
BAUDRATE_THRESHOLD = 10000 # changes the interface for lower performance machines to reduce flickering
ROWS, COLUMNS = map(int, os.popen('stty size', 'r').read().split()) # get the width of the terminal

########## TXT #########
TITLE = 'AC TRANSIT BUS ARRIVALS'
LINE_TITLE_TEXT_COLOR = curses.COLOR_BLACK
LINE_TITLE_HIGHLIGHT_COLOR = curses.COLOR_GREEN

######### STOPS ########
STOPS = [ # the stops to track
	{
	 'title':'Line 18 at Everett to Downtown Oakland',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=18&d=18_90_1&s=1017490',
	 'time_to_stop':[{'walking':11}]
	},
	{
	 'title':'Line V at Everett to San Francisco',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=V&d=V_57_1&s=1017490',
	 'time_to_stop':[{'walking':11}]
	},
	{
	 'title':'Line NX at Park Blvd to San Francisco',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=NX&d=NX_36_1&s=1007240',
	 'time_to_stop':[{'walking':23, 'driving':11}]
	},
	{
	 'title':'Line 18 at Park Blvd to Downtown Oakland',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=18&d=18_90_1&s=1030500',
	 'time_to_stop':[{'walking':23, 'driving':11}]
	},
	{
	 'title':'Line NL at Park Blvd to San Francisco',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=NL&d=NL_146_1&s=1007240',
	 'time_to_stop':[{'walking':23, 'driving':11}]
	},
	{
	 'title':'Line 57 at Park Blvd to Emeryville',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=57&d=57_197_1&s=1007240',
	 'time_to_stop':[{'walking':23, 'driving':11}]
	},
	{
	 'title':'Line 58L at Park Blvd to Downtown Oakland',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=58L&d=58L_22_1&s=1007240',
	 'time_to_stop':[{'walking':23, 'driving':11}]
	},
	{
	 'title':'Line 18 at Everett to Montclair',
	 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=18&d=18_96_0&s=1017480',
	 'time_to_stop':[{'walking':11}]
	},
]