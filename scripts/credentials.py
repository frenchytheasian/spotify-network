import os

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()

def set_client_creds():
    os.environ["SPOTIPY_CLIENT_ID"] = os.getenv("ID")
    os.environ["SPOTIPY_CLIENT_SECRET"] = os.getenv("SECRET")

def set_oauth_creds():
    os.environ["SPOTIPY_REDIRECT_URI"] = os.getenv("REDIRECT_URI")
    os.environ["SPOTIPY_CLIENT_ID"] = os.getenv("ID")
    os.environ["SPOTIPY_CLIENT_SECRET"] = os.getenv("SECRET")

def get_auth_manager():
    set_client_creds()
    return SpotifyClientCredentials()

def get_oauth_manager():
    set_oauth_creds()
    return SpotifyOAuth(scope="user-library-read")