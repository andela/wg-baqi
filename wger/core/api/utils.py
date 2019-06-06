""".

Handle :
    - Authentication via jwt
"""

import jwt
from wger import settings_global as settings
from rest_framework.authtoken.models import Token


def gen_token(user_obj):
    """Generate jwt auth token."""
    try:
        token = Token.objects.get(user=user_obj)
    except Token.DoesNotExist:
        token = False

    if not token:
        token = Token.objects.create(user=user_obj)

    return {'token': str(token)}


def decode_token(request):
    """Decode auth token on login."""
    try:
        token = request.auth.decode()
    except Exception:
        return {'status': 401, 'message': 'Token is missing'}

    payload = jwt.decode(token, settings.SECRET_KEY)
    user = payload['user_id']

    return {'status': 200, 'user': user}
