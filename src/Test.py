import pygtk
import gtk
import gst
import sys

from GooglePlayMusicModule import GooglePlayMusicAdapter
from ThunnerLogger import ThunnerLogger
from getpass import getpass

gtk.gdk.threads_init()
config = {'debug' : True, 'email' : 'acompag@gmail.com', 'pass' : getpass()}
log = ThunnerLogger(config)
api = GooglePlayMusicAdapter(config, log)


def nextSong():
	songUrl, song = api.getRandUrl()
	log.debug('Playing new song - %s' % song['title'])
	player.set_state(gst.STATE_READY)
	player.set_property('uri', songUrl)
	player.set_state(gst.STATE_PLAYING)

def onMessage(bus, message):
	messageType = message.type
	log.debug('New message from player of type %s' % messageType)
	if messageType == gst.MESSAGE_EOS:
		log.debug
		nextSong()


player = gst.element_factory_make("playbin", "player")

#listen for tags on the message bus; tag event might be called more than once
bus = player.get_bus()
bus.enable_sync_message_emission()
bus.add_signal_watch()
bus.connect('message', onMessage)
nextSong()

while True:
	usrInput = raw_input('enter something: ')
	if usrInput == 'e':
		sys.exit()
	elif usrInput == 'pause':
		player.set_state(gst.STATE_PAUSED)
	elif usrInput == 'play':
		player.set_state(gst.STATE_PLAYING)
	elif usrInput == 'n':
		nextSong()