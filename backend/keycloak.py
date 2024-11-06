import jwt
from jwt.exceptions import InvalidTokenError

def verify_access_token(token):
    print("Token to verify:", token)

    try:
        public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs9ygmrcHYyzkJCcTA8d5
dWi5zu34q0p/lqf2x3s5FAVL+O4b8E+jIiByHwc1rkFz6W3/OVy/dfImrUFM6HXt
YnL/z0KJ74phL5amp5AobwOLj0Zm5VWKfv/DQoitBadrgny48wd3YI5SLhmhE7Cl
Uia/G+/rnu6Ic3cdd8F9qQ5lDxE6rExmFWlXYaEa9nQm1dJqeOjjajR1UlTvbOAg
kDpCW3vFU96IqhxuP4eGnAK++heEg+Mn14iMoHY+SJIqkBt51Hi38LPA1pUxj9SQ
SU9BxecgPFl3aWhsBXCG8kbeikZQNvzOzxV9rWHON6F64wtrSouYVi3lpfpb+VhS
CwIDAQAB
-----END PUBLIC KEY-----"""

        # Decode the token without verifying audience
        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})
        print("Decoded token:", decoded_token)
        return decoded_token

    except InvalidTokenError as e:
        print("Invalid token error:", e)
        return None
    except Exception as e:
        print("Other exceptions:", e)
        return None

def process_request():
    # Example token to decode
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJzUEhTMGpwRU90SVFJWE1aVU5XSEh3Y2RZYlR3bnRGYmtxc1dHV0UxNDYwIn0.eyJleHAiOjE3MjI3NTU3OTIsImlhdCI6MTcyMjY2OTM5MiwiYXV0aF90aW1lIjoxNzIyNjY5Mzg5LCJqdGkiOiI2MTFiYWI0MC1lZGY2LTQwZDktOGU2Yi05MDc5Nzg0NWUxNTMiLCJpc3MiOiJodHRwOi8vMTcyLjE2LjEuMTAyOjgwODAvcmVhbG1zL2dyYWZhbmEiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMmY0YmQyZjEtY2Q0NC00ZjQ0LTk0NDktZmQ4ZTE5YjJjZWZiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYWMiLCJzaWQiOiIwM2QxY2YyYy0zNGQxLTRhMTktOWRkYy05ZDNkMzYyMDAzZDQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly8xNzIuMTYuMS41NjozMDAwIiwiaHR0cDovL2xvY2FsaG9zdDozMDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtZ3JhZmFuYSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBhZGRyZXNzIG9mZmxpbmVfYWNjZXNzIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJhZGRyZXNzIjp7fSwibmFtZSI6ImFhc3RoYSBndXB0YSIsInByZWZlcnJlZF91c2VybmFtZSI6Im9tZWdhIiwiZ2l2ZW5fbmFtZSI6ImFhc3RoYSIsImZhbWlseV9uYW1lIjoiZ3VwdGEiLCJlbWFpbCI6Im9tZWdhQGdtYWlsLmNvbSJ9.q3QrRd7GUCWwiewKIxDpBkA2i6udn42ZG6POYNmPmxKmRToc1qWYkdVaAxkJXK6Lii9WsYnGBKshslqw5tuQuXACqZpylp4Sz13_7xyIVd5O9_0U8diOR8nnG2a7f8wpE2kzJC3hBeFNSNDtwzGOdoz2gEjjYRlQ0_VHBP_fLrvSd0TB9fL3fMwwMDqQ0bb6fizAFlH4Pv5cv9oTWXxJOisJoBJP6fqXct7Gd5YGXFaqNI7A88F-rH2MrLS65svaCB-rHHR_OdpuOi7-q7six2_vpKkW5BbdHYdQFvUOR4Do-I_KlJ8IopovxDA9dXxh_ZZwL4GtZ9J2ujKPbT_nkQ'

    decoded_token = verify_access_token(token)
    if decoded_token:
        print("Token successfully decoded:", decoded_token)
        # Assuming you store user information in the token
        # request.user = decoded_token  # Uncomment this if `request` context is available
    else:
        print("Failed to decode token")

process_request()
