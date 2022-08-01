from copy import deepcopy

import pytest
from django.urls import reverse
from model_bakery import baker
from school.models import Student

STUDENTS_LIST_URL = reverse("school:students-list")


@pytest.mark.django_db
def test_get_students_table_success(auto_login_user):
    client, _ = auto_login_user()

    assert Student.objects.count() == 0

    backed_students = baker.make("Student", _quantity=6)
    assert Student.objects.count() == 6

    response = client.get(STUDENTS_LIST_URL)

    # print(response.content.decode("utf-8"))

    assert response.status_code == 200
    assert backed_students[0].full_name in response.content.decode("utf-8")

    


@pytest.mark.django_db
def test_get_students_table_with_unauthenticated_request(client):
    assert Student.objects.count() == 0

    response = client.get(STUDENTS_LIST_URL)

    assert response.status_code == 302

