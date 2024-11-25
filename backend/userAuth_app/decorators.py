from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import KeycloakUser

def validate_keycloak_id(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Check if the decorator has been applied
        if not hasattr(func, '_validate_keycloak_id_applied'):
            print("Error: validate_keycloak_id decorator is missing!")  # Log the error
            return Response(
                {"error": "This API requires validate_keycloak_id decorator."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Extract `keycloak_id` from the request headers or body
            keycloak_id = request.headers.get('Keycloak-ID') or request.data.get('keycloak_id')
            print("Received keycloak_id:", keycloak_id)  # Print the keycloak_id received in the request

            if not keycloak_id:
                print("No keycloak_id provided")  # Print if keycloak_id is missing
                return Response({"error": "keycloak_id is required for authorization."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the `keycloak_id` exists in the database
            user = KeycloakUser.objects.filter(keycloak_id=keycloak_id).first()
            if not user:
                print(f"Invalid keycloak_id: {keycloak_id}")  # Print if the keycloak_id is invalid
                return Response({"error": "Invalid keycloak_id. User not authorized."}, status=status.HTTP_403_FORBIDDEN)

            # Attach the user to the request for downstream use
            request.user = user
            print(f"User validated: {user.username}")  # Print the username of the validated user

            # Call the original function if validation passes
            return func(request, *args, **kwargs)

        except Exception as e:
            print(f"Error in validate_keycloak_id decorator: {str(e)}")  # Print if there's an error in the decorator
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Mark the function as having the decorator applied
    setattr(func, '_validate_keycloak_id_applied', True)
    
    return wrapper
