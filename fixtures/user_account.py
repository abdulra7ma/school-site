import pytest
from model_bakery import baker

__all__ = ["user_account", "auto_login_user", "test_password"]


@pytest.fixture()
def user_account(db):  # pylint: disable=unused-argument
    def _user(**kwargs):
        return baker.make("school.Teacher", **kwargs)

    return _user


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def auto_login_user(db, client, user_account, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = user_account()
            user.set_password(test_password)
            user.save()
        client.force_login(user)
        return client, user

    return make_auto_login
