import hashlib

def fingerprint(ip: str, user_agent: str) -> str:
    raw = ip + user_agent
    return hashlib.sha256(raw.encode()).hexdigest()