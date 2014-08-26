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
    trees = None
    multipleDisks = None

    def __init__(self, config, log):
        self.log = log
        self.initializeApi(config['email'], config['pass'])
        del config['pass']
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

    def getMultipleDisks(self):
        return set([song['album'] for song in self.allSongs if song.get('discNumber', 0) > 1])

    def getDeviceId(self):
        deviceIds = self.webClient.get_registered_devices()
        deviceId = deviceIds[0]['id']
        self.deviceId = deviceId[2:] if deviceId[:2] == '0x' else deviceId

    def getUrlForSong(self, song):
        streamUrl = self.mobileClient.get_stream_url(song['id'], self.deviceId)
        self.log.debug('Got url for song %s \n\t URL - %s' % (song['title'], streamUrl))
        return streamUrl

    def getAllSongs(self):
        if self.allSongs is None:
            self.allSongs = self.mobileClient.get_all_songs()
        if self.multipleDisks is None:
            self.multipleDisks = self.getMultipleDisks()
        return self.allSongs

    def generateTrees(self):
        if self.trees is not None:
            return self.trees

        allSongs = self.getAllSongs()

        albums = {}
        artists = {}
        songs = {'__FLAGS__' : ['LOWEST_LEVEL', 'SONGS']}

        for song in allSongs:
            songAlbum = self.getAlbumForSong(song)
            songTitle = self.addPadding(self.getTitleForSong(song), songs)
            songs[songTitle] = song
            if songAlbum not in albums:
                albums[songAlbum] = {'__FLAGS__' : ['LOWEST_LEVEL', 'SONGS']}
            songTitle = self.addPadding(songTitle.strip(), albums[songAlbum])
            albums[songAlbum][songTitle] = song

        # Sort albums tree using an OrderedDict
        albums = OrderedDict(sorted(albums.items(), key=lambda s: s[0]))

        for album in albums:
            albums[album] = OrderedDict(sorted(albums[album].items(), key=lambda s: self.getTrackNumberForSong(s[1])))
            albumArtist = self.getArtistForSong(albums[album].values()[-1])
            if albumArtist not in artists:
                artists[albumArtist] = {}
            artists[albumArtist][album] = (albums[album])

        self.trees = {'__FLAGS__': ['ROOT_LEVEL'],
                      'Artists': artists,
                      'Albums': albums,
                      'Songs':  songs}
        return self.trees

    def addPadding(self, title, pool):
        while title in pool:
            title += ' '
        return title

    def getSongsForTree(self, tree, songs):
        treeFlags = tree.get('__FLAGS__', [])
        lowestLevel = 'LOWEST_LEVEL' in treeFlags
        songLevel = 'SONGS' in treeFlags
        # There shouldnt be any more song levels after a song level
        if songLevel:
            songs += [song for song in tree.values() if type(song) is not list]
        elif not lowestLevel:
            for subTree in tree.items():
                if subTree[0] != '__FLAGS__':
                    self.getSongsForTree(subTree[1], songs)

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
        albumName = song['album'] if 'album' in song and len(song['album']) > 0 else 'Unknown Album'
        discNumber = '' if albumName not in self.multipleDisks else ' Disc %s' % song['discNumber']
        return albumName + discNumber

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

    """ 
        DEBUG METHOD DO NOT USE
        Recursively dumps the given tree to the terminal
        This will break the GUIAdapter 
    """
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

    """
        DEBUG METHOD DO NOT USE
        Returns the stream URL for a random song
    """
    def getRandomUrl(self):
        if self.allSongs is None:
            self.getAllSongs()
        return self.getUrlForSong(random.choice(self.allSongs))