'''
A terminal app to show nextbus arrival times
By Daniel Levy
ctrl-c to quit

If we want to use speech, can use pyttsx
Can use threading too to have a more interactive interface with custom routes, optional voice, etc
'''

from BeautifulSoup import BeautifulStoneSoup
import urllib, time, os, curses

######## CONFIG ########
MAX_UPDATE_DELAY = 60 # the predictions will updated at least this many seconds
BAUDRATE_THRESHOLD = 10000 # changes the interface for lower performance machines to reduce flickering
ROWS, COLUMNS = map(int, os.popen('stty size', 'r').read().split()) # get the width of the terminal

##### SETUP WINDOW #####
stdscr = curses.initscr()
baudrate = curses.baudrate()

begin_x = 0 ; begin_y = 0
height = 3 ; width = COLUMNS
headscr = curses.newwin(height, width, begin_y, begin_x)

begin_x = 0 ; begin_y = 3
height = 20 ; width = COLUMNS
mainscr = curses.newwin(height, width, begin_y, begin_x)

begin_x = 0 ; begin_y = ROWS - 1
height = 2 ; width = COLUMNS
footscr = curses.newwin(height, width, begin_y, begin_x)

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

###### FUNCTIONS #######
def get_prediction(url):
	'''Go to url and returns the prediction data.'''
	file = urllib.urlopen(url)
	xml = file.read()
	file.close()
	return xml
	
def parse_prediction(prediction):
	'''Return a parsed a prediction.'''
	soup = BeautifulStoneSoup(prediction, selfClosingTags=['prediction'])
	predictions = soup.findAll('prediction')
	return sorted(predictions, key=lambda x: int(x['minutes']))

def get_leave_at(time_to_stop, minutes):
	'''Return the string that tells user when to leave to catch the bus.'''
	minutes = int(minutes)
	string = ""
	for modes in time_to_stop:
		for mode in modes:
			if modes[mode] > minutes:
				string += mode + ": missed, "
			elif modes[mode] == minutes:
				string += mode + ": LEAVE NOW!, "
			else:
				string += mode + ": leave in " + str(minutes - modes[mode]) + "m, "
	return string[:-2]

def print_prediction(stop, prediction):
	'''Print a parsed prediction.'''
	predictions = parse_prediction(prediction)
	mainscr.addstr(stop['title'].ljust(COLUMNS), curses.color_pair(1))
	update_delay = MAX_UPDATE_DELAY
	if predictions:
		for prediction in predictions:
			local_update_delay = int(prediction['seconds']) - int(prediction['minutes']) * 60
			if local_update_delay < update_delay:
				update_delay = local_update_delay
			if prediction['minutes'] == "0":
				mainscr.addstr('Arriving' + ' (' + get_leave_at(stop['time_to_stop'], prediction['minutes']) + ')\n')
			else:
				mainscr.addstr(prediction['minutes'] + ' minutes (' + get_leave_at(stop['time_to_stop'], prediction['minutes']) + ')\n')
	else:
		mainscr.addstr('no prediction\n')
	mainscr.addstr('\n')
	return update_delay

def print_predictions(stops):
	'''Print predictionss for each of the stops.'''
	mainscr.clear()
	update_delay = MAX_UPDATE_DELAY
	for stop in stops:
		prediction = get_prediction(stop['url'])
		local_update_delay = print_prediction(stop, prediction)
		if local_update_delay < update_delay:
			update_delay = local_update_delay
	mainscr.noutrefresh()
	return update_delay
	
def nextbus_app(stops):
	'''Start up the app given a set of stops and print the predictions to the screen.'''
	update_delay = 0
	while True:
		try:
			if update_delay <= 0:
				headscr.clear()
				headscr.addstr('AC TRANSIT BUS ARRIVALS'.center(COLUMNS))
				if baudrate < 10000:
					headscr.addstr(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()).center(COLUMNS))
					footscr.clear()
					footscr.addstr('[updating...]'.center(COLUMNS))
					footscr.noutrefresh()
				else:
					headscr.addstr(time.strftime("Last Updated: %a, %d %b %Y %H:%M:%S", time.localtime()).center(COLUMNS))
				headscr.noutrefresh()
				update_delay = print_predictions(stops)
			else:
				time.sleep(1)
				update_delay -= 1
				if baudrate < 10000:
					headscr.clear()
					headscr.addstr('AC TRANSIT BUS ARRIVALS'.center(COLUMNS))
					headscr.addstr(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()).center(COLUMNS))
					headscr.noutrefresh()
					footscr.clear()
					footscr.addstr(('[next update in ' + str(update_delay) + 's]').center(COLUMNS))
					footscr.noutrefresh()
			curses.doupdate()
		except KeyboardInterrupt: # ctrl-c to close the program
			curses.endwin()
			exit()
		except:
			curses.endwin()
			print "The application quit unexpectedly because I am incompentent at programming. Damn Curses!"
			exit()

######### MAIN #########
def main():
	stops = [
		{
		 'title':'Line 18 at Everett to Downtown Oakland',
		 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=18&d=18_90_1&s=1017490&ts=1017670',
		 'time_to_stop':[{'walking':10}]
		},
		{
		 'title':'Line V at Everett to San Francisco',
		 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=V&d=V_57_1&s=1017490&ts=1017670',
		 'time_to_stop':[{'walking':10}]
		},
		{
		 'title':'Line NX at Park Blvd to San Francisco',
		 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=NX&d=NX_36_1&s=1007240&ts=1015230',
		 'time_to_stop':[{'walking':23, 'driving':10}]
		},
		{
		 'title':'Line NL at Park Blvd to San Francisco',
		 'url':'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=actransit&r=NL&d=NL_146_1&s=1007240&ts=1014760',
		 'time_to_stop':[{'walking':23, 'driving':10}]
		},
	]
	nextbus_app(stops)

if __name__ == "__main__":
	main()