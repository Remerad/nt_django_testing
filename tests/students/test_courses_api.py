import pytest
from django.urls import reverse
from pprint import pprint
from students.models import Course, Student
from tests.conftest import course_factory, student_factory


# Фикстуры лежат в conftest.py в каталоге выше.
# Добавьте следующие тест-кейсы:

# проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_first_curse(client, course_factory):
    course_factory(_quantity=8)    # создаем курс через фабрику
    course_first = Course.objects.first()
    url = reverse('courses-detail', args=(course_first.id, ))   # строим урл и делаем запрос через тестовый клиент
    response = client.get(url)
    #pprint(response.data)
    assert response.status_code == 200
    assert response.data['id'] == course_first.id   # проверяем, что вернулся именно тот курс, который запрашивали
    assert response.data['name'] == course_first.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_curses_list(client, course_factory):
    course_factory(_quantity=8)# аналогично – сначала вызываем фабрики,
    url = reverse('courses-list')
    response = client.get(url)   #затем делаем запрос
    #pprint(response.data)
    assert response.status_code == 200
    assert len(response.data) == 8 #и проверяем результат


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_course_filtered_by_id(client, course_factory):
    course_factory(_quantity=8)    # создаем курсы через фабрику,
    course_first = Course.objects.first()
    url = reverse("courses-list")+f'?id={course_first.id}'  # передать id одного курса в фильтр,
    response = client.get(url)
    #pprint(response.data)
    assert response.status_code == 200
    assert response.data[0].get('id') == course_first.id    # проверить результат запроса с фильтром


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_course_filtered_by_name(client, course_factory):
    course_factory(_quantity=8)
    course_first = Course.objects.first()
    url = reverse("courses-list")+f'?name={course_first.name}'
    response = client.get(url)
    #pprint(response.data)
    assert response.status_code == 200
    assert response.data[0].get('name') == course_first.name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    url = reverse("courses-list")
    data = {'name': 'IZO',
            'stundents': []}
# здесь фабрика не нужна, готовим JSON-данные и создаем курс
    response = client.post(url, data)
    #pprint(response.data)
    assert response.status_code == 201


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course_factory(_quantity=8)# сначала через фабрику создаем,
    course_up = Course.objects.first()
    url = reverse("courses-detail", args=(course_up.id, ))
    data_update = {'name': 'maths'} #потом обновляем JSON-данными
    response = client.patch(url, data_update)
    #pprint(response.data.get('name'))
    assert response.status_code == 200
    assert response.data.get('name') == 'maths'


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=8)
    course_up = Course.objects.first()
    url = reverse("courses-detail", args=(course_up.id, ))
    data_update = {'name': 'maths'}
    response = client.delete(url, data_update)
    #pprint(response.data)
    assert response.status_code == 204