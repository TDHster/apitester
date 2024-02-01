FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]

#docker build -t apitester .
#docker run -p 8501:8501 apitester