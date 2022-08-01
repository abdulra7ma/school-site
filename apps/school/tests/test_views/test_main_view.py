from copy import deepcopy

import pytest
from django.urls import reverse
from model_bakery import baker
from school.models import Student

MAIN_URL = reverse("school:school-index")


@pytest.mark.django_db
def test_get_main_page_success(auto_login_user):
    client, _ = auto_login_user()
    response = client.get(MAIN_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_main_page_with_unauthenticated_request(client):
    response = client.get(MAIN_URL)

    assert response.status_code == 302
