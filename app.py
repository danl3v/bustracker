'''
app.py
Daniel Levy

A terminal app to show nextbus arrival times.
ctrl-c to quit

Future:
-if we want to use speech, can use pyttsx
-only update individual lines when required instead of updating all lines
-add in a line manager to manage bookmarked lines (use threading)
-update_delay at bottom of screen should 
'''

######## IMPORTS #######
from BeautifulSoup import BeautifulStoneSoup
import urllib, time, curses
from config import *

##### SETUP WINDOW #####
stdscr = curses.initscr()
baudrate = curses.baudrate()

begin_x = 0 ; begin_y = 0
height = 3 ; width = COLUMNS
headscr = curses.newwin(height, width, begin_y, begin_x)

begin_x = 0 ; begin_y = 3
height = ROWS - 5 ; width = COLUMNS
mainscr = curses.newwin(height, width, begin_y, begin_x)

begin_x = 0 ; begin_y = ROWS - 1
height = 2 ; width = COLUMNS
footscr = curses.newwin(height, width, begin_y, begin_x)

curses.start_color()
curses.init_pair(1, LINE_TITLE_TEXT_COLOR, LINE_TITLE_HIGHLIGHT_COLOR)

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
                headscr.addstr(TITLE.center(COLUMNS))
                if baudrate < BAUDRATE_THRESHOLD:
                    headscr.addstr(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()).center(COLUMNS))
                    footscr.clear()
                    footscr.addstr('[updating...]'.center(COLUMNS))
                    footscr.noutrefresh()
                else:
                    headscr.addstr(time.strftime("Last Updated: %a, %d %b %Y %H:%M:%S", time.localtime()).center(COLUMNS))
                headscr.noutrefresh()
                curses.doupdate()
                update_delay = print_predictions(stops)
                if update_delay < MIN_UPDATE_DELAY:
                    update_delay = MIN_UPDATE_DELAY
            else:
                time.sleep(1)
                update_delay -= 1
                if baudrate < BAUDRATE_THRESHOLD:
                    headscr.clear()
                    headscr.addstr(TITLE.center(COLUMNS))
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
            print "The application quit unexpectedly. Your terminal might be too small or you resized the terminal while Bus Tracker was running."
            exit()

######### MAIN #########
def main():
    nextbus_app(STOPS)

if __name__ == "__main__":
    main()