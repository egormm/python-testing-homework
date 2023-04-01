from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client

pytestmark = [pytest.mark.django_db]


def test_login_form(client: 'Client') -> None:
    """Test login form."""
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK
    assert 'Войти в личный кабинет' in response.content.decode('utf-8')
