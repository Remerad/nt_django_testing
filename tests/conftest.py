import pytest
from rest_framework.test import APIClient
from model_bakery import baker

#Заведите фикстуры:

# для api-client'а
@pytest.fixture()
def client():
    return APIClient()


# для фабрики курсов
@pytest.fixture()
def course_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)

    return factory


# для фабрики студентов
@pytest.fixture()
def student_factory():
    def factory(**kwargs):
        return baker.make('Student', **kwargs)

    return factory