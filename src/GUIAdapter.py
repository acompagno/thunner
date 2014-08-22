import locale 
import curses

class GUIAdapter:

    FOOTER_HEIGHT = 2
    HEADER_HEIGHT = 2

    log  = None
    config = None
    stdScr = None
    encoding = None
    colors = None
    colorMap = None
    gstPlayer = None 
    musicApi = None
    currentTree = None
    cursorPosition = 0
    currentDisplayListStart = 0
    currentDisplayListEnd = 0
    fullDisplayList = None
    displayListSize = 0

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

    def drawLineAtY(self, y, width = None):
        if width == None:
            height, width = self.stdScr.getmaxyx()
        for i in range(1, width - 1):
            self.stdScr.addch(y, i, curses.ACS_HLINE)

    def drawTree(self, tree):
        self.currentTree = tree
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
        height, width = self.stdScr.getmaxyx()
        self.displayListSize = len(displayList)
        self.clearList()
        for index, item in enumerate(displayList):
            nameLimit = len(item) if len(item) < width - 3 else width - 3
            self.stdScr.addstr(self.HEADER_HEIGHT + 1 + index, 3, item[:nameLimit])

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

    def clearList(self):
        height, width = self.stdScr.getmaxyx()
        usableHeight = height - self.FOOTER_HEIGHT - self.HEADER_HEIGHT - 1
        for i in range(self.HEADER_HEIGHT + 1, usableHeight):
            self.clearLine(i)

    """ Movement """
    def scrollDown(self):
        if self.cursorPosition == self.displayListSize - 1 and self.currentDisplayListEnd < len(self.fullDisplayList):
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
        cursorPosition = self.cursorPosition + self.currentDisplayListStart
        self.log.debug('Selected Item for next Tree: %s' % self.fullDisplayList[cursorPosition])
        self.drawTree(self.currentTree[self.fullDisplayList[cursorPosition]])

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



"""
    Addiction
    1986
    Insomnia [Guitar By Mike Hartnett]
    Tuffest Man Alive
    Guitar Solo
    The Jig Is Up
    What They Gonna Do Feat Sean Paul
    Have U Seen Her (ft. Hit Skrewface)
    The Purge (Feat. Tyler The Creator, Kurupt)
    Black Republican feat. Jay-Z
    Thugnificense (Prod. By Erick Arc Elliott)
    He Man
    It's Raw (feat. Action Bronson)
    Ruthless Villain
    Shoguns (feat. Cappadonna & Vinnie Paz)
    Now Or Neva (Bonus Track)
    Understand (feat. Dice Raw & Greg Porn)
    Every Ghetto (Bonus Track)
    Free My Soul
    true love (chief featuring sene & blu)
    Webbie Flow (U Like)
    Intercontinental Champion
    The Team
    Rather Be With You (Bonus)
    All of the Lights
    The West
    Cut You Off (To Grow Closer)
    Fresh Ta Def
    Can't Cry
    Peso [Prod. By ASAP Ty Beats]
    Interlude (That's Love)
    Don't Worry
    Clyde Smith
    X Chords
    Hunnid Stax (feat. ScHoolboy Q)
    Cradle Rock (feat. Left Eye & Booster)
    So Appalled (feat. RZA, Jay-Z, Pusha T, Swizz Beatz & Cyhi the Prynce)
    Shooting Guns (featuring Kidd Kidd & Twane)
    Dre Day
    Undying Love
    Skybourne (feat. Smoke DZA & Big K.R.I.T.)
    Buggin' Out
    Love Session (Feat. Ruff Endz)
    Ifhy
    Need U Bad (Remix)
    Death By Numbers
    Africa Must Wake Up Ft. K'naan
    We Ball Feat Kendrick Lamar (Prod By Chase N Cashe)
    48
    Sunshine
    Yesterday
    Smoke Again (ft. Ab-Soul)
    Greatest Rapper Ever
    Maxine (Feat. Raekwon)
    Hate (feat. Kanye West) 
    II. Zealots of Stockholm (Free Information)
    Last Real Nigga Alive
    R4 Theme Song
    Quote Me
    U.B.R. (Unauthorized Biography Of Rakim)
    Wassup [Prod. By Clams Casino]
    Deeper (Instrumental)
    Molliwopped
    Do It Again [Put Ya Hands Up] (feat Beanie Sigel & Amil)
    I Will
    Can't Get Enough (feat. Trey Songz)
    I Got Drank (Freestyle) (Bonus Track)
    Deadly Medley (Feat. Royce Da 5'9, Elzhi)
    The Big Payback [Prod. By Big K.R.I.T.]
    See No Evil (Feat. Kendrick Lamar And Tank)
    Drift Away [Prod. By Pro Logic]
    PMW (All I Really Need) feat. ScHoolboy Q
    Joy
    The Last Stretch
    the richers (tiron featuring asher roth & blu)

"""