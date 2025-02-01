from django.contrib import admin

from materials.models import Lesson, Course, Payment


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = ("course",)
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_filter = ("course", "lesson", "method", "date")
