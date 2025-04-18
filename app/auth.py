import os
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired, ChallengeRequired

SESSIONS_DIR = "app/sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

CLIENT = Client()
SESSION_FILE = f"{SESSIONS_DIR}/session.json"


def get_client():
    global CLIENT
    if os.path.exists(SESSION_FILE):
        CLIENT.load_settings(SESSION_FILE)
        CLIENT.login("placeholder", "placeholder")  # Replace with saved creds logic
    return CLIENT


async def login_instagram(username: str, password: str):
    try:
        CLIENT.login(username, password)
        CLIENT.dump_settings(SESSION_FILE)
        return True, "Login successful"
    except TwoFactorRequired:
        return False, "2FA required. Please login via browser manually."
    except ChallengeRequired:
        CLIENT.challenge_resolve()
        return False, "Challenge required. Please approve login in Instagram app."
    except Exception as e:
        return False, str(e)
