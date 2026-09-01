import sys
from pathlib import Path


# Allow imports from project root
ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT))


import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split
)

from sklearn.metrics import (
    accuracy_score,
    classification_report
)


DATA_PATH = ROOT / "data" / "traffic_data.csv"

MODEL_PATH = (
    ROOT /
    "models" /
    "congestion_model.pkl"
)


# Load dataset
df = pd.read_csv(DATA_PATH)


# Features
X = df[
    [
        "vehicle_count",
        "average_speed"
    ]
]


# Target
y = df["congestion"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = RandomForestClassifier(

    n_estimators=150,

    random_state=42
)


# Train
model.fit(
    X_train,
    y_train
)


# Evaluate
predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    f"Model Accuracy: "
    f"{accuracy * 100:.2f}%"
)


print(
    "\nClassification Report:"
)


print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# Save model
joblib.dump(
    model,
    MODEL_PATH
)


print(
    "\nModel saved successfully."
)