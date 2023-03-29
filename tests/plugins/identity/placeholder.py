import json
from collections.abc import Callable
from datetime import date
from typing import TYPE_CHECKING, Any, Protocol, final
from urllib.parse import urljoin

import httpretty
import pytest
from httpretty.http import HttpBaseClass
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from tests.plugins.identity.user import UserDetails


def date_of_birth_to_birthday(date_of_birth: str) -> str:
    """Convert date of birth to birthday."""
    return date.fromisoformat(date_of_birth).strftime('%d.%m.%Y')


@pytest.fixture()
def placeholder_api_url(mf) -> str:
    """Placeholder API URL."""
    return mf('internet.url')


@pytest.fixture()
def placeholder_api_timeout(mf) -> int:
    """Placeholder API timeout."""
    return mf('random.randint', a=1, b=5)


@pytest.fixture()
def placeholder_api_settings(
    settings,
    placeholder_api_url,
    placeholder_api_timeout,
) -> None:
    """Placeholder API URL."""
    settings.PLACEHOLDER_API_URL = placeholder_api_url
    settings.PLACEHOLDER_API_TIMEOUT = placeholder_api_timeout
    return settings


@final
class PlaceholderApiMock(Protocol):  # type: ignore[misc]
    """Protocol for mocking Placeholder API."""

    def __call__(
        self,
        request_method: HttpBaseClass,
        path: str,
        response_body: dict[str, Any],
        response_status: int,
    ) -> None:
        """Mock Placeholder API."""


ApiCallableBody: TypeAlias = Callable[
    [Any, str, dict[str, Any]],
    tuple[int, dict[str, Any], str],
]


def _placeholder_body_factory(
    user_details: 'UserDetails',
    response_status: int,
    response_body: dict[str, Any],
) -> ApiCallableBody:
    def request_callback(request, uri, response_headers):  # noqa: WPS430
        """Check request body."""
        assert json.loads(request.body) == {
            'name': user_details['first_name'],
            'last_name': user_details['last_name'],
            'birthday': date_of_birth_to_birthday(
                user_details['date_of_birth'],
            ),
            'city_of_birth': user_details['address'],
            'position': user_details['job_title'],
            'email': user_details['email'],
            'phone': user_details['phone'],
        }
        return (
            response_status,
            response_headers,
            json.dumps(response_body),
        )
    return request_callback


@pytest.fixture()
def mock_placeholder_api_factory(
    placeholder_api_settings: None,
    placeholder_api_url: str,
    user_details: 'UserDetails',
) -> PlaceholderApiMock:
    """Mock Placeholder API factory."""
    def factory(
        request_method: HttpBaseClass,
        path: str,
        response_body: dict[str, Any],
        response_status: int,
    ) -> None:
        """Mock Placeholder API."""
        httpretty.register_uri(
            request_method,
            urljoin(placeholder_api_url, path),
            body=_placeholder_body_factory(
                user_details,
                response_status,
                response_body,
            ),
            content_type='application/json',
        )
    return factory
