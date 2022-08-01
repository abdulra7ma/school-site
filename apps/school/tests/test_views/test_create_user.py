from copy import deepcopy

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from school.models import Student

CREATE_STUDENT_URL = reverse("school:add-student")
STUDENT_DATA = {
    "full_name": "test_user",
    "email": "email@test.com",
    "date_of_birth": "2004-09-08",
    "student_class": "test class",
    "address": "test-address",
    "floor": 5,
}


@pytest.mark.django_db
def test_create_student_success(auto_login_user):
    client, user = auto_login_user()

    assert Student.objects.count() == 0

    response = client.post(CREATE_STUDENT_URL, STUDENT_DATA)

    assert response.status_code == 302
    assert Student.objects.count() == 1
    assertTemplateUsed("students.html")


@pytest.mark.django_db
def test_create_student_with_uncomplete_data(auto_login_user):
    client, _ = auto_login_user()

    data = deepcopy(STUDENT_DATA)
    del data["full_name"]

    assert Student.objects.count() == 0

    response = client.post(CREATE_STUDENT_URL, data)
    assert response.status_code == 200
    assert "This field is required." in response.content.decode("utf-8")


@pytest.mark.django_db
def test_create_student_with_unvalid_date(auto_login_user):
    client, _ = auto_login_user()

    data = deepcopy(STUDENT_DATA)
    data["date_of_birth"] = "22"

    assert Student.objects.count() == 0

    response = client.post(CREATE_STUDENT_URL, data)
    assert response.status_code == 200
    assert "Enter a valid date." in response.content.decode("utf-8")
