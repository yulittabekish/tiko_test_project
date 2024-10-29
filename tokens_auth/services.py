from enum import Enum

import jwt
from django.conf import settings
from typing import Optional

import jwt
import datetime


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenService:
    @staticmethod
    def create_token(
        user_id: int, token_type: TokenType, lifetime: datetime.timedelta
    ) -> str:
        """Create a JWT token with specified user ID, type, and lifetime.

        Args:
            user_id (int): The ID of the user for whom the token is generated.
            token_type (TokenType): Type of the token (access or refresh).
            lifetime (datetime.timedelta): Lifetime of the token.

        Returns:
            str: Encoded JWT token string.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.UTC) + lifetime,
            "iat": datetime.datetime.now(datetime.UTC),
            "type": token_type.value,
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def decode_token(token: str, token_type: TokenType) -> Optional[dict]:
        """Decode and validate a JWT token.

        Args:
            token (str): Encoded JWT token string.
            token_type (TokenType): Expected type of the token (e.g., access or refresh).

        Returns:
            Optional[Dict]: Decoded payload if the token is valid and type matches, otherwise None.

        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is invalid or cannot be decoded.
        """
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            if payload.get("type") != token_type.value:
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def generate_token_pair(self, user_id: int) -> dict:
        """Generate a pair of access and refresh tokens for the specified user.

        Args:
            user_id (int): The ID of the user for whom tokens are generated.

        Returns:
            dict: A dictionary containing the access and refresh tokens.
        """
        access_token = self.create_token(
            user_id,
            TokenType.ACCESS,
            datetime.timedelta(hours=int(settings.ACCESS_TOKEN_LIFETIME)),
        )
        refresh_token = self.create_token(
            user_id,
            TokenType.REFRESH,
            datetime.timedelta(hours=int(settings.REFRESH_TOKEN_LIFETIME)),
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    def validate_access_token(self, token: str) -> Optional[dict]:
        """Validate the access token and return its decoded payload if valid.

        Args:
            token (str): The access token to validate.
        Returns:
            Optional[dict]: The decoded payload if the token is valid; otherwise, None.
        """
        return self.decode_token(token, TokenType.ACCESS)

    def validate_refresh_token(self, token: str) -> Optional[dict]:
        """Validate the refresh token and return its decoded payload if valid.

        Args:
            token (str): The refresh token to validate.
        Returns:
            Optional[dict]: The decoded payload if the token is valid; otherwise, None.
        """
        return self.decode_token(token, TokenType.REFRESH)
