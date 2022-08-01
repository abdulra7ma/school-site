import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

LOGIN_PATH = reverse("auth:login")


@pytest.mark.django_db
def test_redirct_if_login_success(client: Client, user_account):
    user = user_account()

    data = {
        "phone_number": user.phone_number,
        "password": "super-secret-password",
    }

    user.set_password(data["password"])
    user.save()

    response = client.post(reverse("auth:login"), data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_login_wrong_credentials_failure(client):
    data = {
        "phone_number": "jane@example.com",
        "password": "super-secret-password",
    }  # nosec
    response = client.post(LOGIN_PATH, data)

    assert response.status_code == 200
    assertTemplateUsed(response, "authentication/login.html")
    assert "Phone Number or Password is not correct" in str(response.content)


@pytest.mark.django_db
def test_redirect_if_already_authenticated(auto_login_user):
    client, user = auto_login_user()

    # login user
    client.force_login(user)

    response = client.post(LOGIN_PATH)

    assert response.status_code == 302
