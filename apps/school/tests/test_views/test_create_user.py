import pytest
from django.db.utils import IntegrityError
from model_bakery import baker
from school.models import School, Student, Teacher
from django.urls import reverse


CREATE_STUDENT_URL = reverse("school:add-student")

@pytest.mark.django_db
def test_teacher_school_success(auto_login_user):
    client, user = auto_login_user()

    data = 
    
    response = client.post()