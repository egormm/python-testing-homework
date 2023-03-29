from http import HTTPStatus
from typing import TYPE_CHECKING

import httpretty
import pytest
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from django.test import Client

    from tests.plugins.identity.placeholder import PlaceholderApiMock
    from tests.plugins.identity.user import UserDetails, UserDetailsAssertion


pytestmark = [
    pytest.mark.django_db,
]


def test_change_user(
    saved_user: 'User',
    client: 'Client',
    user_details: 'UserDetails',
    assert_user_details: 'UserDetailsAssertion',
    mock_placeholder_api_factory: 'PlaceholderApiMock',
):
    """Test user change."""
    client.force_login(saved_user)
    mock_placeholder_api_factory(
        request_method=httpretty.PATCH,
        path='/users/{lead_id}'.format(lead_id=saved_user.lead_id),
        response_body={},
        response_status=HTTPStatus.OK,
    )
    response = client.post(
        reverse('identity:user_update'),
        data=user_details,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('location') == reverse('identity:user_update')
    assert_user_details(saved_user.email, user_details)
