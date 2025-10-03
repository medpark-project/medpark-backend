FROM python:3.11-slim
# aplicar atualizacoes de seguranca pois a imagem python contem 2 vulnerabilidades
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

ENV PYTHONPATH=/code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]