
from rest_framework.authtoken.models import Token


def get_token(user):
    # ToDo: do not use try except here
    try:
        user_token = user.auth_token.key
    except:
        user_token = Token.objects.create(user=user)
    return user_token
