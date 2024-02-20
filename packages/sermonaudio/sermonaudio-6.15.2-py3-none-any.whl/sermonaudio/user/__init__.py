from enum import Enum, unique

__all__ = ["requests.User"]  # pragma: no cover


@unique
class UserRoles(Enum):
    """Roles a user may have."""

    TRANSLATOR = 1
    ADMINISTRATOR = 2
    VIDEOWALL = 3


@unique
class BroadcasterUserRoles(Enum):
    """Roles a user may have."""

    ADMINISTRATOR = 2
    UPLOADER = 3
