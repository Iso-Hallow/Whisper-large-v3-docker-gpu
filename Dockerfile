FROM python:3.10-slim

# Установка системных библиотек (ffmpeg нужен для аудио)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и ставим библиотеки Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем наш код
COPY app.py .

# Открываем порт 7860
EXPOSE 7860

# Запускаем
CMD ["python", "app.py"]
