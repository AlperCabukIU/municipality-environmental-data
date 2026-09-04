# Municipality Environmental Sensor Data

This project was created as a prototype for storing and analyzing environmental IoT sensor data. The use case represents a simplified environmental monitoring system for a municipality.

The sensor devices in the dataset are treated as three different municipal sensor stations. The stored measurements can be used to compare environmental conditions between the stations and analyze historical sensor data.

## Dataset

The project uses the "Environmental Sensor Telemetry Data" dataset by Gary Stafford from Kaggle.

The dataset contains measurements such as:

- Temperature
- Humidity
- Carbon monoxide (CO)
- LPG
- Smoke
- Light
- Motion

The complete dataset contains 405,184 measurements from three sensor devices.

For easier reproduction of the project, the repository contains a sample with 15,000 measurements. The prototype was also tested successfully with the complete dataset.

Dataset source:
[Environmental Sensor Telemetry Data](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k) by Gary Stafford on Kaggle.

## Technologies

- Python
- MongoDB
- Docker
- Pandas
- PyMongo

## Project Structure

municipality-environmental-data/
- data/
  - iot_telemetry_sample.csv
- scripts/
  - import_data.py
- .gitignore
- docker-compose.yml
- Dockerfile
- README.md
- requirements.txt

## Running the Project

Docker Desktop must be installed and running.

Clone the repository and open a terminal inside the project folder.

Start the application with:

docker compose up --build

Docker starts the MongoDB database and the Python importer. The importer validates the dataset and imports the measurements into MongoDB in batches.

The MongoDB database is called:

municipality_environment

The measurements are stored in the collection:

sensor_measurements

## Checking the Imported Data

Open the MongoDB shell:

docker exec -it municipality-mongodb mongosh

Select the database:

use municipality_environment

The number of imported measurements can be checked with:

db.sensor_measurements.countDocuments()

The included sample dataset should return 15000 documents.

## Data Analysis

The stored data can be queried by device and timestamp. MongoDB aggregation queries can also be used to compare measurements between the three sensor stations, for example average temperature or humidity.

The device IDs and timestamps can aditionally be used to investigate missing measurements or possible gaps in the sensor data.