import pygtk
import gtk
import gst
import sys

from Queue import Queue

class GSTPlayer:

	player = None
	bus = None
	log = None
	queue = None
	currentSong = None
	musicApi = None

	def __init__(self, log = None):
		if log == None:
			sys.exit()
		self.log = log

		# Initialize GTK threads
		gtk.gdk.threads_init()
		# Create Gst player
		self.player = gst.element_factory_make("playbin", "player")
		self.bus = self.player.get_bus()
		self.bus.enable_sync_message_emission()
		self.bus.add_signal_watch()
		self.bus.connect('message', self.messageHandler)
		# Initialize song queue
		self.queue = Queue()

	def setMusicApi(self, musicApi):
		self.musicApi = musicApi

	def messageHandler(self, bus, message):
		messageType = message.type
		if messageType == gst.MESSAGE_EOS:
			self.log.debug('Finished playing song %s' % self.currentSong['title'])
			if self.queue.empty():
				self.log.debug('Finished queue')
				self.sleepPlayer()
				self.player.set_property('uri', None)
			else:
				self.next()

	def sleepPlayer(self):
		self.setPlayerState(gst.STATE_READY)

	def playSong(self, song):
		self.log.debug('Playing song - %s' % song['title'])
		if not self.player.get_state() == gst.STATE_READY:
			self.sleepPlayer()
		self.currentSong = song
		self.player.set_property('uri', self.musicApi.getUrlForSong(song))
		self.play()

	def setPlayerState(self, state):
		self.player.set_state(state)
		self.log.debug('Set player to state %s' % state.value_name)

	def addSongToQueue(self, song):
		wasOriginallyEmpty =  self.queue.empty()
		self.queue.put(song)
		self.log.debug('Added song to queue - %s' % song['title'])

	# CONTROL MUSIC 
	def pause(self):
		self.setPlayerState(gst.STATE_PAUSED)

	def play(self):
		if self.player.get_property('uri') == None and not self.queue.empty():
			self.next()
		else:
			self.setPlayerState(gst.STATE_PLAYING)

	def toggle(self):
		pass

	def next(self):
		if self.queue.empty():
			self.log.debug("Can't skip to next song. Queue is empty.")
			return
		self.playSong(self.queue.get())

	def back(self):
		pass