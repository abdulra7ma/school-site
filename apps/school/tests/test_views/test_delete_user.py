import pytest
from django.urls import reverse
from model_bakery import baker
from pytest_django.asserts import assertTemplateUsed
from school.models import Student

DELETE_STUDENT_URL = lambda s_id: reverse("school:delete-student", kwargs={"student_id": s_id})


@pytest.mark.django_db
def test_delete_student_success(auto_login_user):
    client, _ = auto_login_user()

    assert Student.objects.count() == 0
    backed_student = baker.make("Student")

    assert Student.objects.count() == 1
    response = client.get(DELETE_STUDENT_URL(backed_student.pk))

    assert response.status_code == 302
    assert Student.objects.count() == 0


@pytest.mark.django_db
def test_delete_student_with_unexisting_student_id(auto_login_user):
    client, _ = auto_login_user()

    assert Student.objects.count() == 0
    response = client.get(DELETE_STUDENT_URL(3))

    assert response.status_code == 302

@pytest.mark.django_db
def test_delete_student_with_unauthenticated_user(client):
    assert Student.objects.count() == 0

    backed_student = baker.make("Student")
    assert Student.objects.count() == 1

    response = client.get(DELETE_STUDENT_URL(backed_student.pk))

    assert response.status_code == 302
    assert Student.objects.count() == 1

