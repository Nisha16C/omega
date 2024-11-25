# your_app_name/authentication.py
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
load_dotenv() 


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        print("a",auth_header)
        if not auth_header:
            return None

        try:
            # Extract the token from the header
            token = auth_header.split(' ')[1]
            print("t",token)

            public_key = os.getenv('PUBLIC_KEY')
            if not public_key:
                raise AuthenticationFailed("Public key not found in environment variables")

            # Verify the token
            decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})
            print("decoded-token",decoded_token)
            return (None, decoded_token)

        except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
            raise AuthenticationFailed(f"Invalid token error: {str(e)}")
        except Exception as e:
            raise AuthenticationFailed(f"Other exceptions: {str(e)}")

        return None
