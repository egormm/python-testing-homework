import enum
import json
from urllib.parse import urljoin

import pytest

from typing import final, Protocol, Any
from mimesis import Internet

import httpretty
from httpretty.http import HttpBaseClass

from server.common.django.types import Settings


@pytest.fixture()
def placeholder_api_settings(mf) -> Settings:
    """Placeholder API URL."""
    return Settings(
        PLACEHOLDER_API_URL=mf('internet.url'),
        PLACEHOLDER_API_TIMEOUT=mf('random.randint', a=1, b=5),
    )


@final
class PlaceholderApiMock(Protocol):
    """Protocol for mocking Placeholder API."""

    def __call__(
        self,
        request_method: HttpBaseClass,
        path: str,
        body: dict[str, Any],
    ) -> None:
        """Mock Placeholder API."""


@pytest.fixture()
def mock_placeholder_api_factory(
    placeholder_api_settings: Settings,
) -> PlaceholderApiMock:
    """Mock Placeholder API factory."""
    def factory(
        request_method: HttpBaseClass,
        path: str,
        request_body: dict[str, Any],
        response_body: dict[str, Any]
    ) -> None:
        """Mock Placeholder API."""
        def request_callback(request, uri, response_headers):
            """Check request body."""
            assert json.loads(request.body) == request_body
            return [200, response_headers, json.dumps(response_body)]

        httpretty.register_uri(
            request_method,
            urljoin(
                placeholder_api_settings.PLACEHOLDER_API_URL,
                path,
            ),
            body=request_callback,
            content_type='application/json',
        )
    return factory
