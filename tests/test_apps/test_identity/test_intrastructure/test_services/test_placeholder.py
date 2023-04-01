from typing import TYPE_CHECKING

from server.apps.identity.intrastructure.services import placeholder
from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import UserModelFactory


def test_serialize_user_no_date_of_birth(
    user_model_factory: 'UserModelFactory',
):
    """Test serialize user with no date of birth."""
    user = User(**user_model_factory(date_of_birth=None))

    serialized_user = placeholder._serialize_user(user)  # noqa: WPS437

    assert serialized_user['birthday'] == ''
