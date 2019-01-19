#!/usr/bin/env python2
# coding: utf-8


# Exception
EXCEPTION_MSG_DICT = {
    "Player command failed: No active device found": 
        u"Sorry player command failed: No active device found",
    "The access token expired":
        u"Sorry the access token expired and the command failed"
}

DEFAULT_EXCEPTION = u"Sorry command has failed for this action"

# No slot
NO_SLOT_ALBUM = u"I do not know which album to play"
NO_SLOT_ARTIST = u"I do not know which artist to play"
NO_SLOT_SONG = u"I do not know which song to play"
NO_SLOT_PLAYLIST = u"I do not know which playlist to play"
NO_SLOT_MODE = u"I do not know which mode to activate"

# Error
NO_SONG_CURRENTLY_PLAYING = u"No song currently playing"
PLAYLIST_NOT_FOUND = u"I don' find playlist corresponding to: {}"   # {} > playlist name

# SUCCESS
PLAY_ALBUM = u"I play the album: {}"                                # {} > album
PLAY_ARTIST = u"I play the artist: {}"                              # {} > artists
PLAY_SONG = u"I play the song: {}"                                  # {} > song
PLAY_PLAYLIST = u"I play the playlist: {}"                          # {} > playlist
GET_INFO = u"You listen: {} interpreted by {} from the album {}"    # {} > song, {} > artists, {} > album
ADD_SONG = u"I save the song: {}"                                   # {} > song to save
