# import requests
# import jwt
# from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed

# class JWTAuthentication(BaseAuthentication):
#     KEYCLOAK_URL = "http://172.16.1.158:8080/realms/master"

#     def get_public_key(self):
#         # Fetch OpenID configuration
#         openid_config_url = f"{self.KEYCLOAK_URL}/.well-known/openid-configuration"
#         response = requests.get(openid_config_url)
#         response.raise_for_status()
#         jwks_url = response.json()['jwks_uri']

#         # Fetch JWKS
#         response = requests.get(jwks_url)
#         response.raise_for_status()
#         jwks = response.json()

#         # Extract public key
#         keys = jwks['keys']
#         if not keys:
#             raise AuthenticationFailed("No keys found in JWKS")

#         # Assuming there's only one key, you might need to handle multiple keys scenario
#         key = keys[0]
#         public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
#         return public_key

#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return None

#         try:
#             # Extract the token from the header
#             token = auth_header.split(' ')[1]


#             # Get the public key
#             public_key = self.get_public_key()
#             print("public_key,",public_key)

#             # Verify the token
#             decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})
#             return (None, decoded_token)

#         except (InvalidTokenError, ExpiredSignatureError, DecodeError) as e:
#             raise AuthenticationFailed(f"Invalid token error: {str(e)}")
#         except Exception as e:
#             raise AuthenticationFailed(f"Other exceptions: {str(e)}")

#         return None





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
