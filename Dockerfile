FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

ENV DATA_PATH BERYL_test_data.nc

CMD ["python", "app.py"]