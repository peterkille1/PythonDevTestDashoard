# PythonDevTestDashboard
A Python-based web dashboard application that visualizes wind speed data from a NetCDF file using Dash. The dashboard allows users to interactively explore the wind speed across different geographic areas and times.

## Features
- Interactive wind speed visualizations
- Customizable map with selectable time frames
- Dockerized for easy deployment

## Project Setup

### Steps to Run

1. **Clone the Repository**

   ```bash
   git clone https://github.com/peterkille1/PythonDevTestDashoard.git
   cd PythonDevTestDashboard
   ```

2. **Build Docker Image**

   ```bash
   docker build -t windspeed-app .
   ```

3. **Run Docker Container**

   ```docker run -p 8050:8050 windspeed-app
   ```

    or build and run
    ```docker-compose up
    ```


4. **Access the App**

   Open your browser and navigate to: [http://localhost:8050](http://localhost:8050)

## Using Docker Compose

If you prefer to use `docker-compose`, here’s a sample `docker-compose.yml`:

```yaml
version: '3.8'
services:
  windspeed-app:
    build: .
    ports:
      - "8050:8050"
    environment:
      - DATA_PATH=BERYL_test_data.nc
```

To run the app using `docker-compose`:

```bash
docker-compose up
```
