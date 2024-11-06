# # keycloak_middleware.py
# from django.utils.deprecation import MiddlewareMixin
# from keycloak import KeycloakOpenID
# from django.conf import settings
# from django.http import JsonResponse

# class KeycloakMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.keycloak_openid = KeycloakOpenID(
#             server_url=settings.KEYCLOAK_SERVER_URL,
#             client_id=settings.KEYCLOAK_CLIENT_ID,
#             realm_name=settings.KEYCLOAK_REALM,
#             client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
#         )

#     def __call__(self, request):
#         if 'Authorization' not in request.headers:
#             return JsonResponse({'error': 'Authorization header missing'}, status=401)

#         auth_header = request.headers['Authorization']
#         token = auth_header.split(' ')[1]

#         try:
#             options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
#             self.keycloak_openid.decode_token(token, key=settings.KEYCLOAK_CLIENT_SECRET, options=options)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=401)

#         return self.get_response(request)
