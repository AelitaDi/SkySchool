from django.db import models

from users.models import User


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
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="courses", null=True, blank=True
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", related_name="lessons", null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Payment(models.Model):
    """
    Модель платежа.
    """

    METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Пользователь",
                             related_name="payments")
    date = models.DateField(auto_now_add=True, verbose_name="Дата платежа")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="payments", blank=True, null=True
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Урок", related_name="payments", blank=True, null=True
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма платежа")
    method = models.CharField(max_length=9, choices=METHOD_CHOICES, default="cash", verbose_name="Способ оплаты")
    session_id = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name="id сессии",
                                  help_text="Введите id сессии")
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату",
                           help_text="Введите ссылку на оплату")

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return f"Оплата {self.course if self.course else self.lesson} на сумму {self.amount}р."


class Subscription(models.Model):
    """
    Модель подписки на обновления курса для пользователя.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="subscriptions")
    is_active = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self):
        if self.is_active:
            is_active = "активна"
        else:
            is_active = "не активна"
        return f"{self.user}: подписка на ({self.course} {is_active})"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
