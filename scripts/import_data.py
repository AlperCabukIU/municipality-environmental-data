import os
import pandas as pd
from pymongo import MongoClient

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
df = df.dropna(subset=["device", "ts"])

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["ts"], unit="s", utc=True)

# Rename temperature column
df = df.rename(columns={"temp": "temperature"})

# Remove old timestamp column
df = df.drop(columns=["ts"])

# Connect to MongoDB
mongo_host = os.getenv("MONGO_HOST", "localhost")
client = MongoClient("mongodb://" + mongo_host + ":27017/")

db = client["municipality_environment"]
collection = db["sensor_measurements"]

print("\nConnected to MongoDB")

# Remove old data before a new import
collection.delete_many({})

# Import data in batches
batch_size = 5000

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i + batch_size]

    records = batch.to_dict("records")

    collection.insert_many(records)

    print("Imported", min(i + batch_size, len(df)), "of", len(df))

print("\nImport finished")
print("Documents:", collection.count_documents({}))

client.close()