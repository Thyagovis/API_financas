from fastapi import Cookie, HTTPException
from jose import JWTError

from core.security import decode_token


def get_current_user(access_token: str = Cookie(None)):
    print("token: ", access_token)
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(access_token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

    return int(user_id)