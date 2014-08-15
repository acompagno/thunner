import pygtk
import gtk
import gst
import sys

from GooglePlayMusicModule import GooglePlayMusicAdapter
from ThunnerLogger import ThunnerLogger
from GSTPlayer import GSTPlayer
from getpass import getpass

config = {'debug' : True, 'email' : 'acompag@gmail.com', 'pass' : getpass()}
log = ThunnerLogger(config)
api = GooglePlayMusicAdapter(config, log)
player = GSTPlayer(log)
player.setMusicApi(api)

for i in range(10):
	url , song = api.getRandUrl()
	player.addSongToQueue(song)

player.play()

while True:
	usrInput = raw_input('waitin')
	if usrInput == 'n':
		player.next()
	elif usrInput == 'p':
		player.toggle()
	elif usrInput == 'e':
		sys.exit()