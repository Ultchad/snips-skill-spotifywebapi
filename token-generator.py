#!/usr/bin/env python2
# coding: utf-8

import spotipy
import spotipy.util as util
import ConfigParser
import argparse
import logging


logging.basicConfig()
logger = logging.getLogger("TokenGenerator")


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name:
                option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with open(configuration_file) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate token for SpotifyWebApi')
    
    parser.add_argument('-c', '--config', dest='config', type=str, default='config.ini',
                        help='Path to Snips SpotifyWebApi config')
    parser.add_argument('-u', '--user', '--username', dest='username', type=str, default=None,
                        help='Username to acount of spotify')
    
    parser.add_argument('--id', '--client-id', dest='client_id', type=str, default=None,
                        help='client_id of your app on spotify devloper')
    parser.add_argument('--secret', '--client-secret', dest='client_secret', type=str, default=None,
                        help='client_secret of your app on spotify devloper')
    parser.add_argument('-r', '--redirect-uri', dest='redirect_uri', type=str, default=None,
                        help='redirect_uri of your app on spotify devloper')
    parser.add_argument('-s', '--scope', dest='scope', type=str, default=None, help='Scope for API write')
    
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Set verbose mode')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Set debug mode')    
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)
        
    if args.debug:
        logger.setLevel(logging.DEBUG)    
    
    # Defined scope
    scope = ''
    # Play music and control playback on your other devices.
    scope += ' streaming'
    # Control playback on your Spotify clients and Spotify Connect devices.
    scope += ' user-modify-playback-state user-read-currently-playing user-read-playback-state'
    # Access your saved tracks and albums.
    scope += ' user-library-read user-library-modify'
    # Access your private playlist
    scope += ' playlist-read-private'
    # Modify your playlist and private playlist
    scope += ' playlist-modify playlist-modify-private'
    
    # Defined config
    username = None
    client_id = None
    client_secret = None
    redirect_uri = None
        
    config = read_configuration_file(args.config)
    if config.get("secret") is not None:        
        username = config["secret"].get("username", None)
        client_id = config["secret"].get("client_id", None)
        client_secret = config["secret"].get("client_secret", None)
        redirect_uri = config["secret"].get("redirect_uri", None)
    
    # If command line option use 
    username = args.username if args.username else username
    client_id = args.client_id if args.client_id else client_id
    client_secret = args.client_secret if args.client_secret else client_secret
    scope = args.scope if args.scope else scope
    # noinspection PyPep8
    redirect_uri = args.redirect_uri if args.redirect_uri else redirect_uri
    
    logger.debug('username: {}'.format(username))
    logger.debug('client_id: {}, client_secret: {}'.format(client_id, client_secret))
    logger.debug('redirect_uri: {}'.format(redirect_uri))
    
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
        
    # Defined cache file
    cache_path = '.cache-{}'.format(username.lower())
    username = username.lower()
    logger.debug('cache_path: {}'.format(cache_path))
    
    logger.info('Try to gen token with util.prompt_for_user_token')
    # Get the tocken
    token = util.prompt_for_user_token(username=username,
                                       client_id=client_id, client_secret=client_secret,
                                       scope=scope, redirect_uri=redirect_uri)
    logger.info('Token generation OK with util.prompt_for_user_token')
    
    logger.info('Try to use token get current_user')
    sp = spotipy.Spotify(auth=token)
    result = sp.current_user()
    # json.dumps(result, indent=2)
    logger.info('use token ok (get current_user)')
    
    print('Token gen and test OK: {}'.format(cache_path))    
