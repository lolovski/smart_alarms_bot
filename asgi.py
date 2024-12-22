from fastapi import FastAPI

# Импортируем приложение из основного файла (например, main.py)
from main import app

# ASGI-приложение для сервера
# Убедитесь, что файл WSGI на сервере ссылается на этот файл
