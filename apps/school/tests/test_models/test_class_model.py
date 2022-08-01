import pytest
from model_bakery import baker
from school.models import Class, School, Teacher
from django.db.utils import IntegrityError


@pytest.mark.django_db
@pytest.mark.enable_signals
def test_create_class_success():
    assert Class.objects.all().count() == 0

    baked_class = baker.make("Class")

    assert Class.objects.all().count() == 1
    assert Class.objects.all().last().name == baked_class.name
    assert School.objects.all().count() == 1
    assert Teacher.objects.all().count() == 1


@pytest.mark.django_db(transaction=True)
def test_create_class_failure():
    assert Class.objects.count() == 0

    with pytest.raises(IntegrityError) as exc_info:
        Class.objects.create(name="test-class")

    assert Class.objects.count() == 0


@pytest.mark.django_db
def test_class_school_success():
    assert Class.objects.all().count() == 0

    baker.make("Class")
    assert Class.objects.all().count() == 1

    Class.objects.all().last().delete()
    assert Class.objects.all().count() == 0
