from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


# Define the transport: we will transfer the token
# via HTTP request header Authorization: Bearer.
# Specify the URL of the endpoint to get the token.
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# Define the strategy: store the token as a JWT.
def get_jwt_strategy() -> JWTStrategy:
    # To a special class from the application settings
    # pass the secret word used to generate the token.
    # The second argument is the token expiration date in seconds.
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


# Create an authentication backend object with the selected parameters.
auth_backend = AuthenticationBackend(
    name="jwt",  # Arbitrary backend name (must be unique).
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Here you can describe your password validation conditions.

    On successful validation, the function returns nothing.
    On validation error, a special error class will be called
    InvalidPasswordException.
    """

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Password should be at least 3 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    # An example of a method for actions after successful user registration.
    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        # Here it would be possible to configure the sending of the letter.
        pass


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
