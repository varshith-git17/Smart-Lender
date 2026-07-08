import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from imblearn.over_sampling import SMOTE

# ----------------------------
# Load dataset
# ----------------------------
import os

file_path = os.path.abspath("loan_data.csv")
print("Reading file:", file_path)

df = pd.read_csv(file_path)

print("Columns:", df.columns.tolist())
# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

print("Columns in dataset:")
print(df.columns.tolist())

# ----------------------------
# Check required column
# ----------------------------
# ----------------------------
# Drop Loan_ID
# ----------------------------
if "Loan_ID" in df.columns:
    df.drop(columns=["Loan_ID"], inplace=True)

# ----------------------------
# Fill missing values
# ----------------------------
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

# Remove duplicates
df.drop_duplicates(inplace=True)

# ----------------------------
# Encode categorical columns
# ----------------------------
label_encoders = {}

for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

# ----------------------------
# Split X and y
# ----------------------------
target_col = "Loan_Status"

X = df.drop(columns=[target_col])
y = df[target_col]