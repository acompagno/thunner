import pygtk
import gtk
import gst
import sys

from GUIAdapter import GUIAdapter
from GooglePlayMusicModule import GooglePlayMusicAdapter
from ThunnerLogger import ThunnerLogger
from GSTPlayer import GSTPlayer
from getpass import getpass
from operator import itemgetter
from collections import OrderedDict

config = {'debug' : True, 'email' : 'acompag@gmail.com', 'pass' : getpass()}
log = ThunnerLogger(config)
api = GooglePlayMusicAdapter(config, log)
player = GSTPlayer(log)
player.setMusicApi(api)
gui = GUIAdapter(config, log)

tree = api.generateTrees()
gui.drawTree(tree)
gui.displayCursor(0)
while True:
	a = gui.getScr().getch()
	log.debug(a)
	if a == 259: # up
		gui.scrollUp()
	elif a == 258: # Down
		gui.scrollDown()
	elif a == 260: # left 
		pass
	elif a == 261: # right
		gui.nextTree()
	else:
		break
gui.closeScr()

# api.dumpTree(tree, 0)
