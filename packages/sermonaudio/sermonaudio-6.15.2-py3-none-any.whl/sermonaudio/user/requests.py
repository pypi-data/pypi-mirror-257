from typing import Optional
from sermonaudio import API, models


class User(API):
    """The User class provides methods for interacting with the /site/users API.

    Typical use of this class involves performing a login via User.login(), which establishes a
    login session. Calls to other methods in the class are authenticated automatically by the login
    session cookie.

    The alternative to establishing a login session with User.login() is to use set_access_token()
    to set an access token and to set the `use_cookie_auth` parameter to False in calls to class
    methods requiring authentication. When `use_cookie_auth` is False, the framework will pass the
    registered access token to the API via an Authentication header.
    """

    @classmethod
    def login(cls, username: str, password: str, **kwargs) -> models.LoginResponse:
        """Attempts to login with `username` and `password`"""

        response = cls.post(f"/v2/site/users/{username}/login", json={"password": password}, **kwargs)

        if response.ok:
            result = models.LoginResponse.parse(response.json())
            return result
        else:
            models.raise_api_exception(response)

    @classmethod
    def get_user(cls, use_cookie_auth: bool = True, **kwargs) -> models.SiteUser:
        """Retrieve user details."""

        response = cls.get("/v2/site/users", use_cookie_auth=use_cookie_auth, **kwargs)

        if response.ok:
            return models.SiteUser.parse(response.json())
        else:
            models.raise_api_exception(response)

    @classmethod
    def refresh(cls, refresh_token: Optional[str] = None, **kwargs) -> str:
        """Attempt to acquire a new access token using `refresh_token`

        If no `refresh_token` is supplied, attempts to use refresh token in session cookie
        """

        json = {"refresh_token": refresh_token} if refresh_token else None
        response = cls.post("/v2/site/users/refresh", json=json, **kwargs)

        if response.ok:
            access_token = response.json()["access_token"]

            return access_token
        else:
            models.raise_api_exception(response)
