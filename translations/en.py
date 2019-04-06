# coding: utf8
# Exception
EXCEPTION_MSG_DICT = {
    "Player command failed: No active device found":
        "Sorry player command failed: No active device found",
    "The access token expired":
        "Sorry the access token expired and the command failed",
    "Player command failed: Cannot control device volume":
        "Sorry player command failed: Cannot control device volume"
}

DEFAULT_EXCEPTION = "Sorry command has failed for this action"

# No slot
NO_SLOT_ALBUM = "I do not know which album to play"
NO_SLOT_ARTIST = "I do not know which artist to play"
NO_SLOT_SONG = "I do not know which song to play"
NO_SLOT_PLAYLIST = "I do not know which playlist to play"
NO_SLOT_MODE = "I do not know which mode to activate"

# Error
NO_SONG_CURRENTLY_PLAYING = "No song currently playing"
PLAYLIST_NOT_FOUND = "I don' find playlist corresponding to: {}"   # {} > playlist name

# SUCCESS
PLAY_ALBUM = "I play the album: {}"                                # {} > album
PLAY_ARTIST = "I play the artist: {}"                              # {} > artists
PLAY_SONG = "I play the song: {}"                                  # {} > song
PLAY_PLAYLIST = "I play the playlist: {}"                          # {} > playlist
# {} > song, {} > artists, {} > album
GET_INFO = "You listen: {} interpreted by {} from the album {}"
# {} > song to save
ADD_SONG = "I save the song: {}"
