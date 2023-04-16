import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

# Turning asynchronous generators into asynchronous context managers.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
):
    """Create user with the given email and password.

    It is possible to create a superuser by passing the is_superuser=True
    argument.
    """
    try:
        # Get the asynchronous session object.
        async with get_async_session_context() as session:
            # Getting an object of the SQLAlchemyUserDatabase class.
            async with get_user_db_context(session) as user_db:
                # Getting an object of the UserManager class.
                async with get_user_manager_context(user_db) as user_manager:
                    # Create a user.
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
                    print(f'Administrator user ({email}) successfully created')
    # If there is already such a user, do nothing.
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Create superuser on first run.

    A coroutine that checks whether the data for the superuser is specified in
    the settings. If so, then the create_user coroutine is called to create
    the superuser.
    """
    if (settings.first_superuser_email is not None and
            settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
