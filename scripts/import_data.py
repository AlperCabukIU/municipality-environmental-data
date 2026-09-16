import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timezone

# Load dataset
data_file = os.getenv("DATA_FILE", "data/iot_telemetry_sample.csv")
df = pd.read_csv(data_file)

print("Rows loaded:", len(df))

# Check if important columns are available
required_columns = [
    "ts",
    "device",
    "co",
    "humidity",
    "light",
    "lpg",
    "motion",
    "smoke",
    "temp"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError("Missing column: " + column)

# Show missing values
print("\nMissing values:")
print(df.isnull().sum())

# Remove rows without device or timestamp
missing_critical = df[["device", "ts"]].isnull().any(axis=1).sum()
print("Rows with missing device ID or timestamp:", missing_critical)

df = df.dropna(subset=["device", "ts"])

# Check duplicate measurements
duplicate_count = df.duplicated().sum()
print("\nDuplicate measurements:", duplicate_count)

# Remove duplicate measurements
df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["ts"], unit="s", utc=True)

# Show dataset coverage
print("\nDataset coverage:")
print("First measurement:", df["timestamp"].min())
print("Last measurement:", df["timestamp"].max())
print("Sensor devices:", df["device"].nunique())
print("Device IDs:", df["device"].unique())

# Dataset provenance information
dataset_metadata = {
    "dataset_name": "Environmental Sensor Telemetry Data",
    "creator": "Gary Stafford",
    "source": "Kaggle",
    "source_url": "https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k",
    "import_date": datetime.now(timezone.utc),
    "first_measurement": df["timestamp"].min(),
    "last_measurement": df["timestamp"].max(),
    "sensor_devices": df["device"].nunique(),
    "records_after_validation": len(df)
}

# Rename temperature column
df = df.rename(columns={"temp": "temperature"})

# Remove old timestamp column
df = df.drop(columns=["ts"])

# Connect to MongoDB
mongo_host = os.getenv("MONGO_HOST", "localhost")
client = MongoClient("mongodb://" + mongo_host + ":27017/")

db = client["municipality_environment"]
collection = db["sensor_measurements"]
metadata_collection = db["dataset_metadata"]

print("\nConnected to MongoDB")

# Remove old data before a new import
collection.delete_many({})
metadata_collection.delete_many({})
metadata_collection.insert_one(dataset_metadata)

# Import data in batches
batch_size = 5000

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i + batch_size]

    records = batch.to_dict("records")

    collection.insert_many(records)

    print("Imported", min(i + batch_size, len(df)), "of", len(df))

# Verify import
expected_documents = len(df)
imported_documents = collection.count_documents({})

print("\nImport finished")
print("Expected documents:", expected_documents)
print("Imported documents:", imported_documents)

if imported_documents != expected_documents:
   raise ValueError("Import verification failed")

print("Import verification: PASSED")

client.close()