FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY . .

EXPOSE 7777

CMD ["uv", "run", "app.py"]