from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson, Payment, Subscription
from materials.validators import UrlValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="url")]


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lesson = LessonSerializer(read_only=True, many=True)
    subscription = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = kwargs.get("context").get("request")

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription(self, course):
        user = self.request.user
        sub = Subscription.objects.filter(user=user, course=course)
        if sub:
            return sub[0].is_active
        return False

    class Meta:
        model = Course
        fields = ("name", "description", "lessons_count", "lesson", "subscription")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
