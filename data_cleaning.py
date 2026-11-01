
"""
Data Cleaning and Basic Analysis
This script cleans the workout dataset and generates a basic statistical summary.
"""

import pandas as pd
from pathlib import Path

# Load the dataset
file_path = Path(__file__).parent / "data.csv"
df = pd.read_csv(file_path)

print("WORKOUT DATA ANALYSIS")
print("=" * 40)

# Check the original dataset
print("\nOriginal dataset shape:", df.shape)

print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Fill missing calorie values using the median
calorie_median = df["Calories"].median()
df["Calories"] = df["Calories"].fillna(calorie_median)

# Fill the missing date based on the dataset's daily date sequence
# Verify this date against the original source if available.
df.loc[df["Date"].isnull(), "Date"] = "2020/12/23"

# Remove duplicate records
duplicates = df.duplicated().sum()
print("\nDuplicate records found:", duplicates)

df = df.drop_duplicates()

# Standardize date values
df["Date"] = (
    df["Date"]
    .astype("string")
    .str.strip()
    .str.replace("'", "", regex=False)
)

# Convert dates into a consistent datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numerical columns into numeric data types
numeric_columns = ["Duration", "Pulse", "Maxpulse", "Calories"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Check for unusually high duration values instead of changing them automatically
print("\nRecords with unusually high duration:")
print(df[df["Duration"] > 300])

# Check the cleaned dataset
print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned dataset shape:", df.shape)

# Generate basic statistical analysis
print("\nSTATISTICAL SUMMARY")
print("=" * 40)
print(df.describe())

print("\nAverage calories burned:", round(df["Calories"].mean(), 2))
print("Maximum calories burned:", df["Calories"].max())
print("Minimum calories burned:", df["Calories"].min())
print("Average workout duration:", round(df["Duration"].mean(), 2))

# Save the cleaned dataset
output_path = Path(__file__).parent / "cleaned_data.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved as cleaned_data.csv")
print("\nFirst five records:")
print(df.head())

print("\nData cleaning and analysis completed successfully!")
