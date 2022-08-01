from django.db import IntegrityError
import pytest
from model_bakery import baker
from school.models import Class, School, Teacher
from django.contrib.auth.hashers import check_password


@pytest.mark.django_db
def test_teacher_school_success():
    assert Teacher.objects.count() == 0

    Teacher.objects.create(
        phone_number="012345878", email="email@test.com", full_name="test user"
    )

    assert Teacher.objects.count() == 1


@pytest.mark.django_db
def test_teacher_query_objects_create_teacher_password_has(test_password):
    assert Teacher.objects.count() == 0

    teacher = Teacher.objects.create_teacher(
        email="email@test.com", password=test_password
    )

    assert Teacher.objects.count() == 1
    assert check_password(test_password, teacher.password) is True


@pytest.mark.django_db(transaction=True)
def test_create_teacher_with_same_email_failure():
    assert Teacher.objects.all().count() == 0

    baked_teacher_object = baker.make("Teacher")
    assert Teacher.objects.all().count() == 1

    with pytest.raises(IntegrityError) as err:
        Teacher.objects.create(email=baked_teacher_object.email)

    assert Teacher.objects.all().count() == 1


@pytest.mark.django_db
def test_delete_teacher_success():
    assert Teacher.objects.all().count() == 0

    baker.make("Teacher")
    assert Teacher.objects.all().count() == 1

    Teacher.objects.all().last().delete()
    assert Teacher.objects.all().count() == 0
