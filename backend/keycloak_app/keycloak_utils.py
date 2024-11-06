# import requests
# from jwt import PyJWKClient
# import jwt
# from django.conf import settings
# from cryptography.hazmat.primitives import serialization

# def get_jwks_url():
#     keycloak_config = settings.KEYCLOAK_CONFIG
#     jwks_url = f"{keycloak_config['SERVER_URL']}/realms/{keycloak_config['REALM']}/protocol/openid-connect/certs"
#     print("jwks_url:", jwks_url)
#     return jwks_url

# def fetch_jwks():
#     jwks_url = get_jwks_url()
#     response = requests.get(jwks_url)
#     response.raise_for_status()
#     print(f"JWKS fetched from {jwks_url}: {response.json()}")
#     return response.json()

# def get_signing_key(token):
#     jwks_url = get_jwks_url()
#     jwks_client = PyJWKClient(jwks_url)
#     signing_key = jwks_client.get_signing_key_from_jwt(token)
    
#     # Converting to PEM format
#     public_key_pem = signing_key.key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     ).decode('utf-8')
    
#     print(f"Public key (PEM format):\n{public_key_pem}")
#     return public_key_pem

# def verify_token(token):
#     try:
#         print(f"Verifying token: {token}")
#         public_key = get_signing_key(token)
#         print(f"Public key used for verification:\n{public_key}")
#         decoded_token = jwt.decode(
#             token, 
#             public_key, 
#             algorithms=["RS256"], 
#             # audience=settings.KEYCLOAK_CONFIG['CLIENT_ID']
#             # audience= ["account"]
#         )
#         print(f"Decoded token: {decoded_token}")
#         return decoded_token
#     except jwt.ExpiredSignatureError:
#         print("Token has expired")
#         return None
#     except jwt.InvalidTokenError as e:
#         print(f"Invalid token: {e}")
#         return None
