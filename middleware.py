from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.exceptions import InvalidToken

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        jwt_auth = JSONWebTokenAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
            request.user = user
        except InvalidToken:
            request.user = None
        response = self.get_response(request)
        return response
