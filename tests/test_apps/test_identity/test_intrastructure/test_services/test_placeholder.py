from typing import TYPE_CHECKING
import httpretty

from server.apps.identity.intrastructure.services.placeholder import _serialize_user
from server.apps.identity.models import User
from server.apps.identity.intrastructure.services import placeholder
from server.common.django.types import Settings

if TYPE_CHECKING:
    from tests.plugins.identity.user import UserModel
    from tests.plugins.identity.placeholder import PlaceholderApiMock


def test_lead_create(
    mock_placeholder_api_factory: 'PlaceholderApiMock',
    placeholder_api_settings: Settings,
    user_model: 'UserModel',
    lead_id: int,
):
    """Test that we can create a new lead."""
    user = User(**user_model)
    mock_placeholder_api_factory(
        request_method=httpretty.POST,
        path='/users',
        response_body={'id': lead_id},
        request_body=_serialize_user(user),
    )

    response = placeholder.LeadCreate(
        api_url=placeholder_api_settings.PLACEHOLDER_API_URL,
        api_timeout=placeholder_api_settings.PLACEHOLDER_API_TIMEOUT,
    )(user=user)

    assert response.id == lead_id


