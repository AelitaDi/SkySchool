from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    PaymentListAPIView,
    PaymentCreateAPIView,
    SubscriptionManagerAPIView,
)

from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename='course')

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path('course_subscription/', SubscriptionManagerAPIView.as_view(), name='course_subscription'),
]
urlpatterns += router.urls
