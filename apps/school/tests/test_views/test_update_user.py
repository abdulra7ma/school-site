from copy import deepcopy

import pytest
from django.urls import reverse
from model_bakery import baker
from pytest_django.asserts import assertTemplateUsed
from school.models import Student

UPDATE_STUDENT_URL = lambda s_id: reverse("school:edit-student", kwargs={"student_id": s_id})
UPDATE_DATA = {"full_name": "updated full_name"}


@pytest.mark.django_db
def test_update_student_success(auto_login_user):
    client, _ = auto_login_user()

    assert Student.objects.count() == 0

    backed_student = baker.make("Student")
    assert Student.objects.count() == 1

    data = deepcopy(UPDATE_DATA)
    data.update(
        [
            ("email", backed_student.email),
            ("date_of_birth", backed_student.date_of_birth),
            ("student_class", backed_student.student_class),
            ("address", backed_student.address),
            ("floor", backed_student.floor),
        ]
    )


    response = client.post(UPDATE_STUDENT_URL(backed_student.pk), data)

    assert response.status_code == 302
    assert Student.objects.count() == 1
    assert Student.objects.get(pk=backed_student.pk).full_name == data["full_name"]


@pytest.mark.django_db
def test_update_student_with_unexisting_student_id(auto_login_user):
    client, _ = auto_login_user()

    assert Student.objects.count() == 0
    response = client.get(UPDATE_STUDENT_URL(3))

    assert response.status_code == 302
    assert Student.objects.count() == 0

