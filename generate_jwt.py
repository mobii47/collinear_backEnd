import os
import jwt
from dotenv import load_dotenv

load_dotenv()
AUTH_TOKEN_SECRET = os.environ.get("AUTH_TOKEN_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")


def generate_jwt_token(email):
    """
    Encode a JWT token with the given session id

    Args:
        email (string): email

    Returns:
        string: jwt token
    """
    return jwt.encode(
        {"id": email},
        AUTH_TOKEN_SECRET,
        algorithm=JWT_ALGORITHM,
    )

def jwt_verification(email, token):
    try:
        decoded_jwt = jwt.decode(token, AUTH_TOKEN_SECRET, algorithms=[JWT_ALGORITHM])
        if email == decoded_jwt["id"]:
            return True
        return False
    except Exception as e:
        logging.error(f"JWT Decode error: {e}")
        return False