from rest_framework.authentication import TokenAuthentication

class CustomHeaderTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Check specifically for our custom header 'HTTP_X_AUTH_TOKEN'
        # Django converts 'X-Auth-Token' to 'HTTP_X_AUTH_TOKEN' in META
        token = request.META.get('HTTP_X_AUTH_TOKEN')
        if not token:
            return super().authenticate(request)
        
        # If found, manually split "Token <key>"
        try:
            # We expect header: "Token 9944b09..."
            key = token.split()[1] 
        except (IndexError, AttributeError):
            return None

        return self.authenticate_credentials(key)