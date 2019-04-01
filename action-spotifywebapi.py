#!/usr/bin/env python3
# coding: utf8

import configparser
from hermes_python.hermes import Hermes
import spotipy
from spotipy import oauth2
import re
import unicodedata
import importlib
import json


MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


_sp_client = None
_volume_add = 10


i18n = None
EXCEPTION_MSG = None


# Snips function
class SnipsConfigParser(configparser.ConfigParser):
    def to_dict(self):
        return {section: {option_name: option
                          for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with open(configuration_file) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        print('[Error] IOError: {}'.format(e))
        return dict()


# Spotify Web API function
def _exception_spotify(spotify_exception, action=None):
    """
    Manage message of exception return by spotify
    :param spotify_exception: SpotifyException object
    :param action: Name of the function who call this function
    :return:
    """
    action = '[{}]'.format(action) if action else ''
    print('[Exception error]{} Spotify error: {}'.format(action, spotify_exception))
    msg = spotify_exception.msg
    if msg.find('\n') != -1:
        msg = msg.split('\n')[1].strip()

    if msg in i18n.EXCEPTION_MSG_DICT:
        text = i18n.EXCEPTION_MSG_DICT[msg]
    else:
        print('[Exception error]{} No have translate for this msg error: {}'.format(action, msg))
        text = i18n.DEFAULT_EXCEPTION
    global EXCEPTION_MSG
    EXCEPTION_MSG = text


def _simple_end(hermes, intentMessage, text=''):
    """
    Send end of session to snips with text or error message
    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :param text: text say by snips default it's error msg and if not: nothing
    :return: None
    """
    global EXCEPTION_MSG
    if EXCEPTION_MSG:
        text = EXCEPTION_MSG
    hermes.publish_end_session(intentMessage.session_id, text)
    EXCEPTION_MSG = None


def _get_cached_token(username, client_id, client_secret,
                      redirect_uri="http://localhost/", scope='', cache_path=None):
    """
    Return the token from cache file
    :param username: username of the premium spotify account
    :param client_id: client_id of the spotify app
    :param client_secret: client_secret of the spotify app
    :param redirect_uri: redirect_uri of the spotify app
    :param scope: scope need to use
    :param cache_path: path of the token file
    :return: token
    """
    if not cache_path:
        cache_path = '.cache-{}'.format(username.lower())
    sp_oauth = oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                   redirect_uri=redirect_uri, scope=scope, cache_path=cache_path)
    token_info = sp_oauth.get_cached_token()

    if token_info:
        return token_info['access_token']
    else:
        return None


def _get_current_volume():
    """
    Call Spotify Web API to get the current volume of the main device
    :return: current volume
    """
    try:
        r = _sp_client.current_playback()
        if r:
            return r['device']['volume_percent']
    except spotipy.client.SpotifyException as e:
        _exception_spotify(e, '_get_current_volume')


def _set_volume(volume_percent):
    """
    Call Spotify Web API to set the current volume of the main device
    :param volume_percent:
    :return:
    """
    print('[_set_volume] input volume_percent: {}'.format(volume_percent))
    if volume_percent > 100:
        volume_percent = 100
    elif volume_percent < 0:
        volume_percent = 0

    volume_percent = int(volume_percent)
    print('[_set_volume] set volume_percent: {}'.format(volume_percent))
    try:
        _sp_client.volume(volume_percent)
    except spotipy.client.SpotifyException as e:
        _exception_spotify(e, '_set_volume')


def _search_first(query, type_search='track'):
    """
    Query Spotify Web API to get the first result of search and return the uri
    :param query: Artist name, album name or track name
    :param type_search: artist, album, track
    :return: uri
    """
    print('Search {}: {}'.format(type_search, query))
    try:
        results = _sp_client.search(q='{}:{}'.format(type_search, query), type=type_search, limit=1)
    except spotipy.client.SpotifyException as e:
        _exception_spotify(e, '_search_first')
        return None

    items = results['{}s'.format(type_search)]['items']
    if len(items) < 1:
        print('Search not items found for {}: {}'.format(type_search, query))
        return None
    item = items[0]
    print('Search found a item for {}: {} \t>\t{} - {}'.format(type, query, item['name'], item['uri']))
    return item['uri']


####################
# Intent function
####################


# Volumes
def volumeUp(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    if intentMessage.slots and intentMessage.slots.volume:
        v_add = intentMessage.slots.volume[0].slot_value.value.value
    else:
        v_add = _volume_add
    v = _get_current_volume()
    if v:
        _set_volume(v + v_add)
    else:
        print('No playback')
    _simple_end(hermes, intentMessage)


def volumeDown(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    if intentMessage.slots and intentMessage.slots.volume:
        v_add = intentMessage.slots.volume[0].slot_value.value.value
    else:
        v_add = _volume_add
    v = _get_current_volume()
    if v:
        _set_volume(v - v_add)
    else:
        print('No playback')
    _simple_end(hermes, intentMessage)


def volumeSet(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    if intentMessage.slots.volume:
        v = intentMessage.slots.volume[0].slot_value.value.value
        _set_volume(v)
    else:
        print('No slots volume found')
    _simple_end(hermes, intentMessage)


# Manage playback
def previousSong(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    _sp_client.previous_track()
    _simple_end(hermes, intentMessage)


def nextSong(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    _sp_client.next_track()
    _simple_end(hermes, intentMessage)


def resumeMusic(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    try:
        _sp_client.start_playback()
    except spotipy.client.SpotifyException as e:
        _exception_spotify(e, 'resumeMusic')
    _simple_end(hermes, intentMessage)


def speakerInterrupt(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    try:
        _sp_client.pause_playback()
    except spotipy.client.SpotifyException as e:
        _exception_spotify(e, 'speakerInterrupt')
    _simple_end(hermes, intentMessage)


# Play
def playAlbum(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    # Snips part
    if intentMessage.slots.album:
        album_name = intentMessage.slots.album[0].slot_value.value.value

        # Spotify part
        uri = _search_first(album_name, 'album')
        if uri:
            try:
                _sp_client.start_playback(context_uri=uri, uris=None)
                hermes.publish_end_session(intentMessage.session_id, i18n.PLAY_ALBUM.format(album_name))
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'playAlbum')
                _simple_end(hermes, intentMessage)
    else:
        print('No slots album found')
        _simple_end(hermes, intentMessage, text=i18n.NO_SLOT_ALBUM)


def playArtist(hermes, intentMessage):
    # Snips part
    if intentMessage.slots.artist:
        artist_name = intentMessage.slots.artist[0].slot_value.value.value

        # Spotify part
        uri = _search_first(artist_name, 'artist')
        if uri:
            try:
                _sp_client.start_playback(context_uri=uri, uris=None)
                hermes.publish_end_session(intentMessage.session_id, i18n.PLAY_ARTIST.format(artist_name))
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'playArtist')
                _simple_end(hermes, intentMessage)
    else:
        print('No slots artist found')
        _simple_end(hermes, intentMessage,  text=i18n.NO_SLOT_ARTIST)


def playSong(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    # Snips part
    if intentMessage.slots.song:
        song_name = intentMessage.slots.song[0].slot_value.value.value

        # Spotify part
        uri = _search_first(song_name, 'track')
        if uri:
            try:
                _sp_client.start_playback(context_uri=None, uris=[uri])
                hermes.publish_end_session(intentMessage.session_id, i18n.PLAY_SONG.format(song_name))
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'playSong')
                _simple_end(hermes, intentMessage)
    else:
        print('No slots song found')
        _simple_end(hermes, intentMessage, text=i18n.NO_SLOT_SONG)


# TODO crate a list with playlist find and ask to user
def playPlaylist(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    # Snips part
    if intentMessage.slots.playlist:
        playlist_name = intentMessage.slots.playlist[0].slot_value.value.value

        pattern = '.*?{}.*?'.format(playlist_name.replace(' ', '[ -_]*?'))
        print('Search playlist pattern: {}'.format(pattern))

        regex = re.compile(pattern, flags=re.IGNORECASE)

        playlist_match = []
        results = _sp_client.current_user_playlists()

        for item in results['items']:
            if regex.search(item['name']):
                print('Add playlist to playlist_match: {}'.format(item['name']))
                playlist_match.append(item)

        playlist_match_name = [item['name'] for item in playlist_match]
        print('playlist_match: {}'.format(playlist_match_name))
        len_playlist_match = len(playlist_match)
        if len_playlist_match > 0:
            print('Play the first playlist: {}'.format(playlist_match[0]['name']))
            uri = playlist_match[0]['uri']
            try:
                _sp_client.start_playback(context_uri=uri, uris=None)
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'playPlaylist')
            # Try to ask to user > for the next version
            # text = u"J'ai trouvé {} playlist correspondante dit moi la quel vous souhaitez: {}".format(
            #                     len_playlist_match, ', '.join(playlist_match_name))
            # hermes.publish_continue_session(intentMessage.session_id, text, ['Tealque:playPlaylist'])
        else:
            print('Playlist not find')
            _simple_end(hermes, intentMessage, text=i18n.PLAYLIST_NOT_FOUND.format(playlist_name))
    else:
        print('No slots playlist found')
        _simple_end(hermes, intentMessage, text=i18n.NO_SLOT_PLAYLIST)


# Info
def getInfos(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    currently_playing = _sp_client.currently_playing()
    if currently_playing:
        track = currently_playing['item']['name']
        album = currently_playing['item']['album']['name']
        artists = [artist['name'] for artist in currently_playing['item']['artists']]
        print('getInfos track: {}, album: {}, artist: {}'.format(track, album, artists))
        # gen artist text
        a = ', '.join(artists)
        if a.find(',') != -1:
            i = a.rindex(',')
            artists_text = "{} et{}".format(a[:i], a[i + 1:])
        else:
            artists_text = a
        print('artists_text: {}'.format(artists_text))
        _simple_end(hermes, intentMessage, text=i18n.GET_INFO.format(track, artists_text, album))
    else:
        print('No track currently playing')
        _simple_end(hermes, intentMessage, text=i18n.NO_SONG_CURRENTLY_PLAYING)


def addSong(hermes, intentMessage):
    """

    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    currently_playing = _sp_client.currently_playing()
    if currently_playing:
        uri = currently_playing['item']['uri']
        _sp_client.current_user_saved_tracks_add([uri])
        _simple_end(hermes, intentMessage, text=i18n.ADD_SONG.format(currently_playing['item']['name']))
    else:
        _simple_end(hermes, intentMessage, text=i18n.NO_SONG_CURRENTLY_PLAYING)


# Function
def modeEnable(hermes, intentMessage):
    """
    Enable shuffle or repeapt mode
    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """
    if intentMessage.slots.mode:
        mode = intentMessage.slots.mode[0].slot_value.value.value

        # Mode Shuffle
        if mode == 'shuffle':
            try:
                _sp_client.shuffle(state=True)
                print('shuffleEnable')
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'shuffleEnable')
        # Mode Repeat
        elif mode == 'repeat':
            try:
                # state - track, context, or off
                # Get current playback to see the actual repeat state
                c = _sp_client.current_playback()
                if c['repeat_state'] == 'off':
                    state = 'context'
                elif c['repeat_state'] == 'context':
                    state = 'track'
                else:
                    state = 'context'

                _sp_client.repeat(state=state)
                print('repeatEnable with state: {} (old state: {})'.format(state, c['repeat_state']))
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'repeatEnable')
        else:
            print('Unknown mode: {}'.format(mode))

        _simple_end(hermes, intentMessage)
    else:
        print('No slots mode found')
        _simple_end(hermes, intentMessage, text=i18n.NO_SLOT_MODE)


def modeDisable(hermes, intentMessage):
    """
    Disable shuffle or repeapt mode
    :param hermes: message manager of snips
    :param intentMessage: intent message incoming from snips broker
    :return: void
    """

    if intentMessage.slots.mode:
        mode = intentMessage.slots.mode[0].slot_value.value.value

        # Mode Shuffle
        if mode == 'shuffle':
            try:
                _sp_client.shuffle(state=False)
                print('shuffleDisable')
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'shuffleEnable')
        # Mode Repeat
        elif mode == 'repeat':
            try:
                # state - track, context, or off
                _sp_client.repeat(state='off')
                print('repeatDisable')
            except spotipy.client.SpotifyException as e:
                _exception_spotify(e, 'repeatEnable')
        else:
            print('Unknown mode: {}'.format(mode))

        _simple_end(hermes, intentMessage)
    else:
        print('No slots mode found')
        _simple_end(hermes, intentMessage, text=i18n.NO_SLOT_MODE)


if __name__ == "__main__":

    # Use the assistant's language.
    with open("/usr/share/snips/assistant/assistant.json") as json_file:
        language = json.load(json_file)["language"]

    i18n = importlib.import_module("translations." + language)

    # Defined default redirect uri
    redirect_uri = r'http://localhost/'

    # Defined default scope
    scope = ''
    # Play music and control playback on your other devices.
    scope += ' streaming'
    # Control playback on your Spotify clients and Spotify Connect devices.
    scope += ' user-modify-playback-state user-read-currently-playing user-read-playback-state'
    # Access your saved tracks and albums.
    scope += ' user-library-read'
    # Access your private playlist
    scope += ' playlist-read-private'
    # Modify your playlist and private playlist
    scope += ' playlist-modify playlist-modify-private'

    # Default init conf
    username = None
    client_id = None
    client_secret = None

    # Read the config
    config = read_configuration_file("./config.ini")
    if config.get("secret") is not None:
        username = config["secret"].get("username", None)
        client_id = config["secret"].get("client_id", None)
        client_secret = config["secret"].get("client_secret", None)
        redirect_uri = config["secret"].get("redirect_uri", r'http://localhost/')

    # Check options
    if not client_id or not client_secret:
        print("[Error] No client_id, client_secret or redirect_uri found, it's need for connection !\n\
        To get this create a APP and set allowed redirect_uri on:\n\
        https://developer.spotify.com/my-applications/#!/applications")
        exit(2)

    # Check username
    if not username:
        print("[Error] No username found, it's need for connection !")
        exit(2)

    token = _get_cached_token(username=username, client_id=client_id, client_secret=client_secret,
                              redirect_uri=redirect_uri, scope=scope,
                              cache_path='.cache-{}'.format(username.lower()))

    print('Get the cached token: OK')
    if not token:
        print("[Error] No cached token find ! Gen the token with:\npython token-generator.py")
        exit(3)

    _sp_client = spotipy.Spotify(auth=token)

    with Hermes(MQTT_ADDR) as h:
        h.subscribe_intent('Tealque:volumeUp', volumeUp)\
            .subscribe_intent('Tealque:volumeDown', volumeDown)\
            .subscribe_intent('Tealque:volumeSet', volumeSet)\
            .subscribe_intent('previousSong', previousSong)\
            .subscribe_intent('nextSong', nextSong)\
            .subscribe_intent('resumeMusic', resumeMusic)\
            .subscribe_intent('speakerInterrupt', speakerInterrupt)\
            .subscribe_intent('Tealque:playAlbum', playAlbum)\
            .subscribe_intent('Tealque:playArtist', playArtist)\
            .subscribe_intent('Tealque:playSong', playSong)\
            .subscribe_intent('Tealque:playPlaylist', playPlaylist)\
            .subscribe_intent('getInfos', getInfos)\
            .subscribe_intent('addSong', addSong)\
            .subscribe_intent('Tealque:modeEnable', modeEnable)\
            .subscribe_intent('Tealque:modeDisable', modeDisable)\
            .loop_forever()
