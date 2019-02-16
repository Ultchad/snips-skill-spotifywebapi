#!/usr/bin/env python2
# coding: utf-8


# Exception
EXCEPTION_MSG_DICT = {
    "Player command failed: No active device found":
        u"Désolé une erreur c'est produite: Aucun équipement actif n'a été trouvé",
    "The access token expired":
        u"Désolé une erreur c'est produite: le token d'acces a expiré"
}

DEFAULT_EXCEPTION = u"Désolé une erreur c'est produite lors de cette action"

# No slot
NO_SLOT_ALBUM = u"Je ne sais pas quel album jouer"
NO_SLOT_ARTIST = u"Je ne sais pas quel artiste jouer"
NO_SLOT_SONG = u"Je ne sais pas quelle musique jouer"
NO_SLOT_PLAYLIST = u"Je ne sais pas quelle playlist jouer"
NO_SLOT_MODE = u"Je ne sais pas quel mode activer"

# Error
NO_SONG_CURRENTLY_PLAYING = u"Il n'y a pas de musique en cours d'écoute"
PLAYLIST_NOT_FOUND = u"Je n'ai pas trouver de playlist correspondant à: {}"

# SUCCESS
PLAY_ALBUM = u"Je met l'album: {}"
PLAY_ARTIST = u"Je met l'artiste: {}"
PLAY_SONG = u"Je met la musique: {}"
PLAY_PLAYLIST = u"Je met la playlist: {}"
GET_INFO = u"Vous écoutez: {} interprété par {} de l'album {}"
ADD_SONG = u"J'ai sauvegarder dans vos titre: {}"
