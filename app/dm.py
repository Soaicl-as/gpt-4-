import asyncio
from app.utils import log
from instagrapi import Client


async def start_campaign(client: Client, target: str, message: str, mode: str, limit: int, delay: float):
    users = []
    try:
        user_id = client.user_id_from_username(target)
        if mode == "followers":
            users = client.user_followers(user_id)
        else:
            users = client.user_following(user_id)
    except Exception as e:
        return {"error": f"Could not fetch user list: {str(e)}"}

    sent = 0
    for uid, user in list(users.items())[:limit]:
        try:
            client.direct_send(message, [uid])
            sent += 1
            log(f"Sent to @{user.username}")
            await asyncio.sleep(delay)
        except Exception as e:
            log(f"Failed to send to @{user.username}: {e}")
            continue

    return {"sent": sent, "attempted": limit}
