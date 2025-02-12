from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@example.com")
        self.course = Course.objects.create(
            name="DevOps", description="Курс для обучения профессии DevOps", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Обучающее видео 1",
            course=self.course,
            owner=self.user,
            url="https://www.youtube.com/watch?v=8sv-6AN0_cg",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """
        Тест на получение данных урока.
        """
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """
        Тест на создание урока.
        """
        url = reverse("materials:lesson_create")
        data = {"name": "Обучающее видео 2", "course": self.course.pk, "url": "https://www.youtube.com/1"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """
        Тест на редактирование урока.
        """
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Урок 3", "course": self.course.pk, "url": "https://www.youtube.com/3"}
        response = self.client.put(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок 3")

    def test_lesson_delete(self):
        """
        Тест на удаление урока.
        """
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """
        Тест на получение списка уроков.
        """
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": self.lesson.preview,
                    "url": self.lesson.url,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)


class NotAuthorisedLessonTestCase(APITestCase):
    """
    Тесты с неавторизованным пользователем.
    """

    def setUp(self):
        self.user = User.objects.create(email="test_user@example.com")
        self.course = Course.objects.create(
            name="DevOps", description="Курс для обучения профессии DevOps", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Обучающее видео 1",
            course=self.course,
            owner=self.user,
            url="https://www.youtube.com/watch?v=8sv-6AN0_cg",
        )

    def test_lesson_retrieve(self):
        """
        Тест на получение данных урока.
        """
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create(self):
        """
        Тест на создание урока.
        """
        url = reverse("materials:lesson_create")
        data = {"name": "Обучающее видео 2", "course": self.course.pk, "url": "https://www.youtube.com/1"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update(self):
        """
        Тест на редактирование урока.
        """
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Урок 3", "course": self.course.pk, "url": "https://www.youtube.com/3"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete(self):
        """
        Тест на удаление урока.
        """
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        """
        Тест на получение списка уроков.
        """
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NotOwnerLessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test_user@example.com")
        self.course = Course.objects.create(
            name="DevOps", description="Курс для обучения профессии DevOps", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Обучающее видео 1",
            course=self.course,
            owner=self.user,
            url="https://www.youtube.com/watch?v=8sv-6AN0_cg",
        )
        self.any_user = User.objects.create(email="not_owner@example.com")
        self.client.force_authenticate(user=self.any_user)

    def test_lesson_delete(self):
        """
        Тест на удаление урока.
        """
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        """
        Тест на получение списка уроков.
        """
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {"count": 0, "next": None, "previous": None, "results": []}
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    """
    Проверка работы функционала подписки на курсы.
    """

    def setUp(self):
        self.user = User.objects.create(email="test_user@example.com")
        self.course = Course.objects.create(
            name="DevOps", description="Курс для обучения профессии DevOps", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Обучающее видео 1",
            course=self.course,
            owner=self.user,
            url="https://www.youtube.com/watch?v=8sv-6AN0_cg",
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_activate(self):
        """
        Проверка добавления и удаления подписки на курсы.
        """
        url = reverse("materials:course_subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {"message": "Подписка добавлена"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 1)

        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        message = {"message": "Подписка удалена"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, message)
        self.assertEqual(Subscription.objects.all().count(), 0)
