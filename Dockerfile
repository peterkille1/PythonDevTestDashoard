FROM continuumio/miniconda3

WORKDIR /app

COPY . /app/

RUN conda install -c conda-forge cartopy \
    && conda install -c conda-forge numpy pandas netCDF4 \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

ENV DATA_PATH=BERYL_test_data.nc

CMD ["python", "app.py"]