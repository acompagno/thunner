import sys
import random

from gmusicapi import Mobileclient
from gmusicapi import Webclient
from collections import OrderedDict

class GooglePlayMusicAdapter:

    LOG_MESSAGE_SUCCESS = 'Logged in to %s client as %s'
    LOG_MESSAGE_FAIL = 'Failed logging in to %s client as %s'

    mobileClient = None
    webClient = None
    log = None
    deviceId = None 
    allSongs = None

    def __init__(self, config, log):
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

    def getUrlForSong(self, song):
        streamUrl = self.mobileClient.get_stream_url(song['id'], self.deviceId)
        self.log.debug('Got url for song %s \n\t URL - %s' % (song['title'], streamUrl))
        return streamUrl

    def getAllSongs(self):
        if self.allSongs == None:
            self.allSongs = self.mobileClient.get_all_songs()
        return self.allSongs

    def generateTrees(self):
        allSongs = self.getAllSongs()

        albums = {}
        artists = {}
        songs = {'__FLAGS__' : ['LOWEST_LEVEL', 'SONGS']}

        for song in allSongs:
            songAlbum = self.getAlbumForSong(song)
            songTitle = self.getTitleForSong(song)
            songs[songTitle] = song
            if songAlbum not in albums:
                albums[songAlbum] = {'__FLAGS__' : ['LOWEST_LEVEL', 'SONGS']}
            albums[songAlbum][songTitle] = song

        for album in albums:
            albums[album] = OrderedDict(sorted(albums[album].items(), key=lambda s: self.getTrackNumberForSong(s[1])))
            albumArtist = self.getArtistForSong(albums[album].values()[-1])
            if albumArtist not in artists:
                artists[albumArtist] = {}
            artists[albumArtist][album] = (albums[album])

        return {'__FLAGS__' : ['ROOT_LEVEL'],
                'Artists'   :  artists,
                'Albums'    :  albums,
                'Songs'     :  songs }


    def getSongsForTree(self, tree):
        pass

    # Get song information 
    def getTitleForSong(self, song):
        return song['title']

    def getArtistForSong(self, song):
        if not type(song) is dict:
            return -1
        albumArtist = song['albumArtist']
        artist = song['artist']
        if albumArtist != '':
            return albumArtist
        elif artist != '':
            return artist
        else:
            return 'Unknown Artist'

    def getAlbumForSong(self, song):
        if not type(song) is dict:
            return -1
        return song['album'] if 'album' in song else 'Unknown Album'

    def getTrackNumberForSong(self, song):
        if not type(song) is dict:
            return -1
        return song['trackNumber'] if 'trackNumber' in song else -1

    def songToString(self, song):
        if not type(song) is dict:
            return -1
        songTitle = self.getTitleForSong(song)
        songArtist = self.getArtistForSong(song)
        return '%s - %s' % (songArtist, songTitle)

    """DEBUG METHODS """
    def getRandUrl(self):
        if self.allSongs == None:
            self.allSongs = self.mobileClient.get_all_songs()
        randomSong = random.choice(self.allSongs)
        streamUrl = self.mobileClient.get_stream_url(randomSong['id'], self.deviceId)
        return streamUrl, randomSong

    def dumpTree(self, tree, level):
        treeFlags = tree.get('__FLAGS__', [])
        lowestLevel = 'LOWEST_LEVEL' in treeFlags
        indentation  = '\t' * level
        print '%sTree Flags - %s' % (indentation, treeFlags)
        for items in tree.items():
            if items[0] == '__FLAGS__':
                continue
            print '%s%s' % (indentation, items[0])
            if not lowestLevel:
                self.dumpTree(items[1], level + 1)