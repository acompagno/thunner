import locale 
import curses

class GUIAdapter:

    config = None
    stdScr = None
    encoding = None
    colors = None
    colorMap = None
    gstPlayer = None 
    musicApi = None

    def __init__(self, config):
        self.config = config
        locale.setlocale(locale.LC_ALL, '')
        self.encoding = locale.getpreferredencoding()
        self.stdScr = self.initScr()

    def initScr(self):
        stdScr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdScr.keypad(1)
        return stdScr

    def closeScr(self):
        curses.nocbreak()
        self.stdScr.keypad(0)
        curses.echo()
        curses.endwin()

    def drawLineAtY(self, y, width = None):
        if width == None:
            height, width = self.stdScr.getmaxyx()
        for i in range(1, width - 1):
            self.stdScr.addch(y, i, curses.ACS_HLINE)

    def drawHeader():
        pass

    def setPlayer(self, gstPlayer):
        self.gstPlayer = gstPlayer

    def setMusicApi(self, musicApi):
        self.musicApi = musicApi