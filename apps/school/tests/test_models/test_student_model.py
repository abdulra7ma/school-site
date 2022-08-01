import pytest
from django.db.utils import IntegrityError
from model_bakery import baker
from school.models import School, Student, Teacher


@pytest.mark.django_db
def test_create_student_success():
    baker.make("Student")
    assert Student.objects.all().count() == 1

    Student.objects.create(
        full_name="full_name",
        email="abdo@a.com",
        date_of_birth="2004-09-04",
        student_class="test-class",
        address="test-address",
        floor=4,
    )

    assert Student.objects.all().count() == 2


@pytest.mark.django_db(transaction=True)
def test_create_school_failure():
    assert Student.objects.all().count() == 0

    with pytest.raises(IntegrityError) as exc_info:
        Student.objects.create()

    assert Student.objects.all().count() == 0


@pytest.mark.django_db
def test_update_student_success():
    baked_student = baker.make("Student")
    baked_teacher = baker.make("Teacher")

    assert Student.objects.all().count() == 1
    assert Teacher.objects.all().count() == 1
    assert baked_student.updated_by != baked_teacher

    baked_student.updated_by = baked_teacher

    # before saving into databse
    assert Student.objects.get(pk=baked_student.pk).updated_by != baked_teacher

    baked_student.save()

    # after saving to database
    assert Student.objects.get(pk=baked_student.pk).updated_by == baked_teacher


@pytest.mark.django_db
def test_delete_student_success():
    assert Student.objects.all().count() == 0

    baker.make("Student")
    assert Student.objects.all().count() == 1

    Student.objects.all().last().delete()
    assert Student.objects.all().count() == 0
