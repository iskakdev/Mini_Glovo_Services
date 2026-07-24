import os
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')


class JWTUser:
    def __init__(self, user_id, username=None, status=None):
        self.id = user_id
        self.pk = user_id
        self.username = username
        self.status = status
        self.is_authenticated = True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истёк')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Некорректный токен')
        user_id = payload.get('sub')
        if user_id is None:
            raise AuthenticationFailed('Некорректный токен')
        return (
            JWTUser(
                int(user_id),
                username=payload.get('username'),
                status=payload.get('status'),
            ),
            token,
        )