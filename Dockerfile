FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]

EXPOSE 8501
