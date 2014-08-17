import pygtk
import gtk
import gst
import sys

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

# allSongs = api.mobileClient.get_all_songs()

# # albums = set([api.getAlbumForSong(song) for song in songs])


# for song in allSongs:
# 	songAlbum = api.getAlbumForSong(song)
# 	songTitle = api.getTitleForSong(song)
# 	songs[songTitle] = song
# 	if songAlbum not in albums:
# 		albums[songAlbum] = {'__FLAGS__' : ['LOWEST_LEVEL', 'SONGS']}
# 	albums[songAlbum][songTitle] = song

# for album in albums:
# 	albums[album] = OrderedDict(sorted(albums[album].items(), key=lambda s: api.getTrackNumberForSong(s[1])))
# 	albumArtist = api.getArtistForSong(albums[album].values()[-1])
# 	if albumArtist not in artists:
# 		artists[albumArtist] = {}
# 	artists[albumArtist][album] = (albums[album])

tree = api.generateTrees()
artists = tree['Artists']
albums = tree['Albums']
songs = tree['Songs']

api.dumpTree(tree, 0)
# for a in artists:
# 	print a
# 	for album in artists[a]:
# 		print '\t%s' % album
# 		for songIndex in artists[a][album]:
# 			if songIndex == '__FLAGS__':
# 				print '\t\tTree Flags - %s' % artists[a][album][songIndex]
# 				continue
# 			song = artists[a][album][songIndex]
# 			print '\t\t%s) %s' % (api.getTrackNumberForSong(song), api.getTitleForSong(song))