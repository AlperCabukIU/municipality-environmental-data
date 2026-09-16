# Municipality Environmental Sensor Data

This project was created as a prototype for storing and analyzing environmental IoT sensor data. The use case represents a simplified environmental monitoring system for a municipality.

The sensor devices in the dataset are treated as three different municipal sensor stations. The stored measurements can be used to compare short-term environmental conditions between the stations during the pilot period.

## Use Case

The current dataset is treated as an eight-day pilot deployment of three environmental sensor stations in a fictional municipality.

An environmental planner would use a future dashboard to compare short-term environmental measurements between the stations and select different measurement types and time periods. The dashboard and API are part of the system design but are not implemented in the current prototype.

The current implementation focuses on data validation, batch processing, MongoDB storage, provenance and reliable import of the sensor measurements.

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

## Data Quality

Before the measurements are imported, the Python importer performs several basic data quality checks.

The importer:

- checks whether all required columns are available
- reports missing values
- removes measurements without a device ID or timestamp
- detects and removes complete duplicate measurements
- reports the measurement period and detected sensor devices

During testing with the complete dataset, 13 complete duplicate measurements were detected and removed. This reduced the dataset from 405,184 to 405,171 measurements.

The complete dataset covers approximately eight days, from July 12 to July 20, 2020. Therefore, the current prototype is intended for short-term comparisons between sensor stations rather than long-term or seasonal environmental analysis.

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

## Reliability and Provenance

Docker uses a health check to verify that MongoDB is available before the importer starts.

After the batch import, the Python importer compares the number of validated measurements with the number of documents stored in MongoDB. If the numbers do not match, the import fails with an error.

The prototype also stores information about the origin of the dataset in a separate `dataset_metadata` collection. This includes:

- dataset name
- creator
- source and source URL
- import date
- first and last measurement
- number of detected sensor devices
- number of records after validation

This information makes the origin and coverage of the imported dataset easier to trace.

## Data Analysis

The stored data can be queried by device and timestamp. MongoDB aggregation queries can also be used to compare measurements between the three sensor stations, for example average temperature or humidity.

The device IDs and timestamps can additionally be used to investigate measurement intervals and possible gaps in the sensor data. Since the three devices use different measurement frequencies, differences in the number of measurements do not automatically indicate missing data.

## Extending the Prototype

### Adding Another Sensor Station

The existing three device IDs are not hardcoded in the importer. An additional station can therefore be added by:

1. Adding measurements with a new unique `device` ID to the input dataset.
2. Using the same timestamp and measurement structure.
3. Running the existing Docker import workflow.
4. The importer will automatically include the new device in the detected sensor devices.
5. The new measurements can then be queried through the existing `sensor_measurements` collection.

### Adding Location Information

The current Kaggle dataset does not contain geographic coordinates. For a real municipal deployment, location information could be added through a separate `sensor_stations` collection.

Each station could contain its `device` ID, station name, latitude, longitude and a description of the location. The existing device ID would connect this information with the measurements stored in `sensor_measurements`.

A future API and dashboard could use this information to display meaningful station names and locations.

### Adding a New Measurement Type

Additional environmental measurements such as CO2, noise or particulate matter could be added to the system.

For example, adding CO2 would require:

1. Adding a `co2` field to measurements from compatible sensors.
2. Extending the validation logic if CO2 is required for the dataset.
3. Importing the measurements through the existing batch workflow.
4. Extending a future API to provide CO2 measurements.
5. Adding CO2 as a selectable measurement in the planned dashboard.

MongoDB allows documents with additional fields, so existing measurements do not need to contain the new measurement type.

### Extending to Multiple Municipalities

If the system were extended to multiple municipalities, each station would need additional metadata identifying its municipality and location. Comparisons between municipalities would also require common measurement units, comparable time periods and information about sensor quality and measurement frequency.

Provenance would be especially important if results were used in public discussions because users should be able to identify where the measurements originated and what period they represent. The current prototype provides basic dataset provenance, but additional information such as sensor calibration, exact locations and responsible organizations would be required for reliable real-world comparisons.