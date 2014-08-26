import sys

from GUIAdapter import GUIAdapter
from GooglePlayMusicModule import GooglePlayMusicAdapter
from ThunnerLogger import ThunnerLogger
from getpass import getpass

config = {'debug' : True, 'email' : 'acompag@gmail.com', 'pass' : getpass()}
log = ThunnerLogger(config)
api = GooglePlayMusicAdapter(config, log)
# player = GSTPlayer(log)
# player.setMusicApi(api)
gui = GUIAdapter(config, log)

tree = api.generateTrees()
gui.drawTree(tree)
gui.displayCursor(0)
gui.setMusicApi(api)

for i in api.multipleDisks:
    log.debug(i)

while True:
    a = gui.getScr().getch()
    # log.debug(a)
    if a == 259: # up
        gui.scrollUp()
    elif a == 258: # Down
        gui.scrollDown()
    elif a == 260: # left
        gui.lastTree()
    elif a == 261: # right
        gui.nextTree()
    elif a == -1 or a == 410:
        gui.refresh()
    else:
        break

gui.closeScr()
allSongs = api.getAllSongs()


# api.dumpTree(tree, 0)