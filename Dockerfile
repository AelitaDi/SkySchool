# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Копируем исходный код приложения в контейнер
COPY . /app/

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media && chmod -R 755 /app/media
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
# CMD ["poetry", "run", "python", "manage.py", "runserver"]
