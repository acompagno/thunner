import sys
import random

from gmusicapi import Mobileclient
from gmusicapi import Webclient

class GooglePlayMusicAdapter:

	LOG_MESSAGE_SUCCESS = 'Logged in to %s client as %s'
	LOG_MESSAGE_FAIL = 'Failed logging in to %s client as %s'

	mobileClient = None
	webClient = None
	log = None
	deviceId = None 
	allSongs = None

	def __init__(self, config = None, log = None):
		if config == None or log == None:
			sys.exit()
		self.log = log
		self.initializeApi(config['email'], config['pass'])
		self.getDeviceId()

	def initializeApi(self, email, password):
		# Initialize and Log in to Mobile Client
	    self.mobileClient = Mobileclient()
	    isMobileClientLoggedIn = self.mobileClient.login(email, password)
	    self.log.debug((self.LOG_MESSAGE_SUCCESS if isMobileClientLoggedIn else self.LOG_MESSAGE_FAIL) % ('Mobile', email))
		# Initialize and Log in to Web Client
	    self.webClient = Webclient()
	    isWebClientLoggedIn = self.webClient.login(email, password)
	    self.log.debug((self.LOG_MESSAGE_SUCCESS if isMobileClientLoggedIn else self.LOG_MESSAGE_FAIL) % ('Web', email))
	    return isMobileClientLoggedIn and isWebClientLoggedIn

	def getDeviceId(self):
	    deviceIds = self.webClient.get_registered_devices()
	    deviceId = deviceIds[0]['id']
	    self.deviceId = deviceId[2:] if deviceId[:2] == '0x' else deviceId

	def getRandUrl(self):
		if self.allSongs == None:
			self.allSongs = self.mobileClient.get_all_songs()
		randomSong = random.choice(self.allSongs)
		streamUrl = self.mobileClient.get_stream_url(randomSong['id'], self.deviceId)
		return streamUrl, randomSong