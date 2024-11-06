# your_app_name/authentication.py
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
# from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
load_dotenv() 

class JWTAuthentication():
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Extract the token from the header
            token = auth_header.split(' ')[1]

            public_key = os.getenv('PUBLIC_KEY')
            if not public_key:
                raise AuthenticationFailed("Public key not found in environment variables")

            # Verify the token
            decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})
            
            # Assuming the username is in the 'preferred_username' claim or similar
            username = decoded_token.get('preferred_username') or decoded_token.get('sub')
            if not username:
                raise AuthenticationFailed("Username not found in token")

            # Assuming the roles are in the 'realm_access' claim under 'roles'
            roles = decoded_token.get('realm_access', {}).get('roles', [])
            if not roles:
                raise AuthenticationFailed("Roles not found in token")

            # Attach user information to the request for later use
            request.user = {
                'username': username,
                'roles': roles
            }

            return (request.user, decoded_token)

        except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
            raise AuthenticationFailed(f"Invalid token error: {str(e)}")
        except Exception as e:
            raise AuthenticationFailed(f"Other exceptions: {str(e)}")

        return None
