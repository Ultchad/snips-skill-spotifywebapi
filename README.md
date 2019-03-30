# SpotifyWebApi french skill for Snips

_First: Sorry for my english!_

This app need a **Spotify Premium account** and **create a APP** on Spotify Console

- The app it's requirements to use the SpotifyWebApi
- The premium account it's requirements of SpotifyWebApi to control other device (Playback, Volume, Get information of currently playing)

With this app you can control any spotify devices, who's connected with your premium account, to spotify network

## Installation with Sam

The easiest way to use this Action is to install it with [Sam](https://snips.gitbook.io/getting-started/installation)

`sam install actions -g https://github.com/Ultchad/snips-skill-spotifywebapi.git`

## Manual installation

- Clone the repository on your Pi
- Run `setup.sh` (it will create a virtualenv, install the dependencies in it and rename config.ini.default to config.ini)
- Enter information in config.ini (username, client_id, client_secret, redirect_uri)
- activate the virtual environement with this command:`. ./venv/bin/activate`. For deactivate run command: `deactivate`
- Generate token with ./token-generator.py
- Run `action-spotifywebapi.py`

## Get client_id, client_secret, redirect_uri

Register your app at [My Applications](https://developer.spotify.com/my-applications/#!/applications)

After creation on setting of your enter redirect_uri (example: 'http://localhost/' is the default on this app)
Warning: for redirect_uri http://localhost/ and http://localhost is not the same (the later '/' is missing) you can enter some redirect_uri


Now you can enter on the App or on config.ini client_id, client_secret, redirect_uri and your username

## Gen the token

### From the script on snips device

- Go to the app dir (default: /var/lib/snips/skills/snips-skill-spotifywebapi/)
- activate the virtual environement with this command:`. ./venv/bin/activate`. For deactivate run command: `deactivate`
- Run `setup.sh` (it will create a virtualenv, install the dependencies in it and rename config.ini.default to config.ini)
- Generate token with ./token-generator.py
  - copy the URL on your browser
  - when you redirect on your redirect_uri, copy the complete url and paste on script
  - the script generate the token on .cache-USERNAME
  
### From your computer

- copy token-generator.py , requirements.txt and config.ini your computer:
- complete the config.ini
- install dependencies:
```
python -m pip install -r requirements.txt
```
- run the script
```
python token-generator.py
```
- Normally  the script run automatically on your browser the URL to approve your app
- When you redirect on your redirect_uri, copy the complete url and paste on script
  - the script generate the token on .cache-USERNAME copy this file on your app dir to your snips device 
  (default: /var/lib/snips/skills/snips-skill-spotifywebapi/)

