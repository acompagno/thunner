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
gui = GUIAdapter(config)

tree = api.generateTrees()
gui.drawTree(tree['Songs'])
gui.displayCursor(0)
while True:
	a = gui.getScr().getch()
	log.debug(a)
	if a == 259:
		gui.scrollUp()
	elif a == 258:
		gui.scrollDown()
	else:
		break
gui.closeScr()

# api.dumpTree(tree, 0)
