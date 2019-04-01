# coding: utf8
# Exception
EXCEPTION_MSG_DICT = {
    "Player command failed: No active device found":
        "Désolé une erreur c'est produite: Aucun équipement actif n'a été trouvé",
    "The access token expired":
        "Désolé une erreur c'est produite: le token d'acces a expiré",
    "Player command failed: Cannot control device volume":
        "Désolé une erreur c'est produite: Je ne peux pas contrôler l'équipement actif "
}

DEFAULT_EXCEPTION = "Désolé une erreur c'est produite lors de cette action"

# No slot
NO_SLOT_ALBUM = "Je ne sais pas quel album jouer"
NO_SLOT_ARTIST = "Je ne sais pas quel artiste jouer"
NO_SLOT_SONG = "Je ne sais pas quelle musique jouer"
NO_SLOT_PLAYLIST = "Je ne sais pas quelle playlist jouer"
NO_SLOT_MODE = "Je ne sais pas quel mode activer"

# Error
NO_SONG_CURRENTLY_PLAYING = "Il n'y a pas de musique en cours d'écoute"
PLAYLIST_NOT_FOUND = "Je n'ai pas trouver de playlist correspondant à: {}"

# SUCCESS
PLAY_ALBUM = "Je met l'album: {}"
PLAY_ARTIST = "Je met l'artiste: {}"
PLAY_SONG = "Je met la musique: {}"
PLAY_PLAYLIST = "Je met la playlist: {}"
GET_INFO = "Vous écoutez: {} interprété par {} de l'album {}"
ADD_SONG = "J'ai sauvegarder dans vos titre: {}"
