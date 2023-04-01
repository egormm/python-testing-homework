from typing import TYPE_CHECKING

from server.apps.identity.intrastructure.services.placeholder import _serialize_user
from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import UserModelFactory


def test_serialize_user_no_date_of_birth(user_model_factory: 'UserModelFactory') -> None:
    user = User(**user_model_factory(date_of_birth=None))

    serialized_user = _serialize_user(user)

    assert serialized_user['birthday'] == ''
