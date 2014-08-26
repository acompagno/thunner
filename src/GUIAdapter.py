import locale 
import curses

class GUIAdapter:

    FOOTER_HEIGHT = 2
    HEADER_HEIGHT = 2

    # ThunnerLogger object
    log  = None
    # GSTPlayer object 
    gstPlayer = None 
    # Music Api Object
    musicApi = None
    # Holds the configuration dict for the application
    config = None
    
    # Holds the SCR where the GUI is being displayed
    stdScr = None
    # Holds the current encoding of the terminal
    encoding = None
    # Holds the current tree being displayed
    currentTree = None
    # Holds the current cursor position in relation to the displayable list
    cursorPosition = 0
    # The starting index of the list being displayed in relation to fullDisplayList
    currentDisplayListStart = 0
    # The ending index of the list being displayed in relation to fullDisplayList
    currentDisplayListEnd = 0
    # List containing all items of the tree currently being displayed
    fullDisplayList = None
    # Number of items currently being displayed
    displayListSize = 0

    # Path to current tree being displayed
    path = []

    def __init__(self, config, log):
        self.config = config
        self.log = log
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

    def writeStr(self, y, x, string):
        self.stdScr.addstr(y, x, string.encode(self.encoding))

    def writeChar(self, y, x, char):
        self.stdScr.addch(y, x, char)

    def drawLineAtY(self, y, width = None):
        if width is None:
            height, width = self.stdScr.getmaxyx()
        for i in range(1, width - 1):
            self.writeChar(y, i, curses.ACS_HLINE)

    def drawTree(self, tree):
        self.currentTree = tree
        height, width = self.stdScr.getmaxyx()
        usableHeight = height - self.FOOTER_HEIGHT - self.HEADER_HEIGHT - 1
        displayList = tree.keys()
        if '__FLAGS__' in displayList:
            displayList.remove('__FLAGS__')
            self.flags = tree['__FLAGS__']
        else:
            self.flags = []
        self.fullDisplayList = displayList
        if len(displayList) > usableHeight:
            displayList = displayList[:usableHeight]
        self.currentDisplayListEnd = len(displayList)
        self.drawList(displayList)

    def drawList(self, displayList):
        height, width = self.stdScr.getmaxyx()
        self.displayListSize = len(displayList)
        self.clearList()
        for index, item in enumerate(displayList):
            nameLimit = len(item) if len(item) < width - 3 else width - 3
            self.writeStr(self.HEADER_HEIGHT + 1 + index, 3, item[:nameLimit])

    def drawHeader(self):
        self.drawLineAtY(self.HEADER_HEIGHT)
        self.clearLine(1)
        self.writeStr(1, 1, ' > '.join(['thunner'] + self.path))

    def drawFooter(self):
        height, width = self.stdScr.getmaxyx()
        self.drawLineAtY(height - self.FOOTER_HEIGHT)
        self.writeStr(height - 1, 1, 'Playing')

    def displayCursor(self, cursorPosition):
        self.cursorPosition = cursorPosition
        realCursorHeight = self.getRealCursorPosition(cursorPosition)
        self.writeStr(realCursorHeight, 1, '*')

    def removeCursor(self):
        realCursorHeight = self.getRealCursorPosition(self.cursorPosition)
        self.writeStr(realCursorHeight, 1, ' ')

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
        self.writeStr(y , x, ' ' * (width - x))

    def clearList(self):
        height, width = self.stdScr.getmaxyx()
        usableHeight = height - self.FOOTER_HEIGHT
        for i in range(self.HEADER_HEIGHT + 1, usableHeight):
            self.clearLine(i, x = 2)

    def getFromDict(self, dataDict, mapList):
        return reduce(lambda d, k: d[k], mapList, dataDict)

    """ Movement """
    def scrollDown(self):
        if self.cursorPosition == self.displayListSize - 1 and self.currentDisplayListEnd < len(self.fullDisplayList):
            self.moveListDown()
        elif self.cursorPosition < self.displayListSize - 1:
            self.removeCursor()
            self.displayCursor(self.cursorPosition + 1)

    def scrollUp(self):
        if self.currentDisplayListStart > 0 and self.cursorPosition == 0:
            self.moveListUp()
        elif self.cursorPosition > 0:
            self.removeCursor()
            self.displayCursor(self.cursorPosition - 1)

    def nextTree(self):
        if 'LOWEST_LEVEL' in self.flags:
            self.log.debug("Already on lowest level can't move to next subtree")
            return
        cursorPosition = self.cursorPosition + self.currentDisplayListStart
        self.log.debug('Selected Item for next Tree: %s' % self.fullDisplayList[cursorPosition])
        newTreeName = self.fullDisplayList[cursorPosition]
        self.path.append(newTreeName)
        self.drawHeader()
        self.drawTree(self.currentTree[newTreeName])
        self.removeCursor()
        self.displayCursor(0)

    def lastTree(self):
        if 'ROOT_LEVEL' in self.flags:
            self.log.debug("Already on root level can't move back")
            return
        self.log.debug('Moving back to %s tree' % 'root' if len(self.path) < 2 else self.path[-2])
        del self.path[-1]
        self.drawHeader()
        self.drawTree(self.getFromDict(self.musicApi.generateTrees(), self.path))
        self.removeCursor()
        self.displayCursor(0)

    def refresh(self):
        self.stdScr.clear()
        self.drawHeader()
        self.drawTree(self.currentTree)
        self.displayCursor(self.cursorPosition)
        self.drawFooter()

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