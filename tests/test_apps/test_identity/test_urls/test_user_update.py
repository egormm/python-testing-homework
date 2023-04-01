from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

    from server.apps.identity.models import User

pytestmark = [pytest.mark.django_db]


def test_user_update_form_logged_user(
    client: 'Client',
    saved_user: 'User',
) -> None:
    """Test user update form for logged user."""
    client.force_login(saved_user)

    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
    assert 'Редактировать профиль' in response.content.decode('utf-8')


def test_user_update_form_not_logged_user(
    client: 'Client',
    saved_user: 'User',
) -> None:
    """Test user update form for not logged user."""
    response = client.get(reverse('identity:user_update'))

    assert response.status_code == HTTPStatus.FOUND
