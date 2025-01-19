from django.db import models


class Course(models.Model):
    """
    Модель курса обучения.
    """

    name = models.CharField(max_length=250, verbose_name="Название курса", help_text="Введите название курса")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Введите описание курса"
    )

    preview = models.ImageField(
        upload_to="materials/preview/",
        verbose_name="Превью",
        help_text="Загрузите превью курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """
    Модель урока.
    """

    name = models.CharField(max_length=250, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание урока", help_text="Введите описание урока"
    )

    preview = models.ImageField(
        upload_to="materials/preview/",
        verbose_name="Превью",
        help_text="Загрузите превью урока",
        blank=True,
        null=True,
    )
    url = models.URLField(
        blank=True, null=True, verbose_name="Ссылка на видео урока", help_text="Введите ссылку на видео урока"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lesson")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
