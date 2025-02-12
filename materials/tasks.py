from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription
from users.models import User


@shared_task
def block_inactive_user():
    """
    Блокирует юзеров, которые не заходили более 30 дней.
    """
    User.objects.filter(
        is_active=True,
        is_staff=False,
        is_superuser=False,
        last_login__isnull=False,
        last_login__lt=timezone.now() - timezone.timedelta(days=30)
    ).update(is_active=False)


@shared_task
def sendmail_course_update(course):
    """
    Отправка сообщения об обновлении курса по подписке.
    """
    subscription_course = Subscription.objects.filter(course=course)
    print(f"Найдено {len(subscription_course)} подписок на курс {course}")
    for subscription in subscription_course:
        print(f"Отправка уведомления на {subscription.user.email}")
        send_mail(
            subject="Обновление материалов курса",
            message=f"Курс {subscription.course.name} был обновлен.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
