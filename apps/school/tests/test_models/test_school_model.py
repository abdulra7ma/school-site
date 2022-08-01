import pytest
from model_bakery import baker
from school.models import Class, School


@pytest.mark.django_db
def test_create_school_success():
    baker.make("School")
    assert School.objects.all().count() == 1

    school_name = "Test School"
    School.objects.create(name=school_name)
    assert School.objects.all().count() == 2


@pytest.mark.django_db
@pytest.mark.enable_signals
def test_create_school_and_classes():
    assert School.objects.all().count() == 0

    baked_school_object = baker.make("School")
    baked_classes_objects = baker.make("Class", _quantity=3)

    assert School.objects.all().count() == 2
    assert Class.objects.all().count() == 3
    assert baked_school_object.classes.count() == 0

    for cls in baked_classes_objects:
        baked_school_object.classes.add(cls)

    assert baked_school_object.classes.count() == 3


@pytest.mark.django_db
def test_delete_school_success():
    assert School.objects.all().count() == 0

    baker.make("School")
    assert School.objects.all().count() == 1

    School.objects.all().last().delete()
    assert School.objects.all().count() == 0
