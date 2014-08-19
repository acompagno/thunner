import locale 
import curses

class GUIAdapter:

    FOOTER_HEIGHT = 2
    HEADER_HEIGHT = 2

    config = None
    stdScr = None
    encoding = None
    colors = None
    colorMap = None
    gstPlayer = None 
    musicApi = None
    cursorPosition = 0
    currentDisplayListStart = 0
    currentDisplayListEnd = 0
    fullDisplayList = None
    displayListSize = 0

    def __init__(self, config):
        self.config = config
        locale.setlocale(locale.LC_ALL, '')
        self.encoding = locale.getpreferredencoding()
        self.stdScr = self.initScr()
        self.drawHeader()
        self.drawFooter()

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

    def drawTree(self, tree):
        height, width = self.stdScr.getmaxyx()
        usableHeight = height - self.FOOTER_HEIGHT - self.HEADER_HEIGHT - 1
        displayList = tree.keys()
        if '__FLAGS__' in displayList:
            displayList.remove('__FLAGS__')
        self.fullDisplayList = displayList
        if len(displayList) > usableHeight:
            displayList = displayList[:usableHeight]
        self.currentDisplayListEnd = len(displayList)
        self.drawList(displayList)

    def drawList(self, displayList):
        self.displayListSize = len(displayList)
        for index, item in enumerate(displayList):
            self.clearLine(self.HEADER_HEIGHT + 1 + index, x = 2)
            self.stdScr.addstr(self.HEADER_HEIGHT + 1 + index, 3, item)

    def drawHeader(self):
        self.drawLineAtY(self.HEADER_HEIGHT)
        self.stdScr.addstr(1, 1, 'thunner >')

    def drawFooter(self):
        height, width = self.stdScr.getmaxyx()
        self.drawLineAtY(height - self.FOOTER_HEIGHT)
        self.stdScr.addstr(height - 1, 1, 'Playing')

    def displayCursor(self, cursorPosition):
        realCursorHeight = self.getRealCursorPosition(cursorPosition)
        self.stdScr.addstr(realCursorHeight, 1, '*')

    def removeCursor(self):
        realCursorHeight = self.getRealCursorPosition(self.cursorPosition)
        self.stdScr.addstr(realCursorHeight, 1, ' ')

    def getRealCursorPosition(self, cursorPosition):
        return self.HEADER_HEIGHT + cursorPosition + 1

    def moveList(self, start, end):
        self.currentDisplayListStart = start
        self.currentDisplayListEnd = end
        self.drawList(self.fullDisplayList[start:end])

    def moveListDown(self):
        self.moveList(self.currentDisplayListStart + 1, self.currentDisplayListEnd + 1)

    def moveListUp(self):
        self.moveList(self.currentDisplayListStart - 1, self.currentDisplayListEnd - 1)

    def clearLine(self, y, x = 0):
        height, width = self.stdScr.getmaxyx()
        self.stdScr.addstr(y , x, ' ' * (width - x))

    """ Movement """
    def scrollDown(self):
        if self.cursorPosition == self.displayListSize - 1 and self.currentDisplayListEnd < len(self.fullDisplayList) - 1:
            self.moveListDown()
        elif self.cursorPosition < self.displayListSize - 1:
            self.removeCursor()
            self.cursorPosition += 1
            self.displayCursor(self.cursorPosition)

    def scrollUp(self):
        if self.currentDisplayListStart > 0 and self.cursorPosition == 0:
            self.moveListUp()
        elif self.cursorPosition > 0:
            self.removeCursor()
            self.cursorPosition -= 1
            self.displayCursor(self.cursorPosition)

    def nextTree(self):
        pass

    def lastTree(self):
        pass

    """ Getters and setters """

    def setPlayer(self, gstPlayer):
        self.gstPlayer = gstPlayer

    def setMusicApi(self, musicApi):
        self.musicApi = musicApi
    
    def getFooterHeight(self):
        return self.FOOTER_HEIGHT

    def getHeaderHeight(self):
        return self.HEADER_HEIGHT

    def getScr(self):
        return self.stdScr