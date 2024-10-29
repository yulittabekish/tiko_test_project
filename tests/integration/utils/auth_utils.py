import datetime

from django.conf import settings

from tokens_auth.services import TokenService, TokenType


def get_auth_headers(user):
    token = TokenService().create_token(
        user.id,
        TokenType.ACCESS,
        datetime.timedelta(hours=int(settings.ACCESS_TOKEN_LIFETIME)),
    )
    return {"Authorization": f"Bearer {token}"}
