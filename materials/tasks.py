import datetime

import pytz
from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, TIME_ZONE
from materials.models import Subscription
from users.models import User


@shared_task
def block_inactive_user():
    """
    Блокирует юзеров, которые не заходили более 30 дней.
    """
    users = User.objects.filter(is_active=True).exclude(is_superuser=True)
    tz = pytz.timezone(TIME_ZONE)
    date_now_tz = datetime.datetime.now(tz)
    for user in users:
        if user.last_login:
            date = user.last_login
        else:
            date = user.date_joined
        time_delta = date_now_tz - date
        if time_delta > datetime.timedelta(days=30):
            user.is_active = False
            print(f"Юзер {user.email} заблокирован. Последний вход: {date}")


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
            fail_silently=False
        )
