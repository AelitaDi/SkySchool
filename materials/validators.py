from rest_framework import serializers
import re


class UrlValidator:
    """
    Валидатор для проверки ссылок только на ресурс youtube.com
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('^(https|http)(://www.youtube.com/)(.*?)$')
        url = dict(value).get(self.field)
        print(url)
        match = reg.match(url)
        if match is None:
            raise serializers.ValidationError("Допустимы ссылки только на ресурс youtube.com")
