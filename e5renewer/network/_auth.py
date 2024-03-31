import time


MAX_FIXUP = 30  # Allow (0,30] seconds elder than now

auth_token = ""


def setup_auth(token: str):
    global auth_token
    auth_token = token


def check_auth(authentication: str) -> bool:
    if auth_token:
        return authentication == auth_token
    return False


def check_outdate(timestamp: int) -> bool:
    timestamp_now = int(time.time() * 1000)
    return timestamp > 0 and (0 < timestamp_now - timestamp <= MAX_FIXUP * 1000)
