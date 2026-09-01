import joblib

from config import (
    MODEL_PATH,
    LOW_LIMIT,
    MEDIUM_LIMIT,
    HIGH_LIMIT
)


def calculate_density(vehicle_count):

    if vehicle_count <= LOW_LIMIT:

        return "Low"


    if vehicle_count <= MEDIUM_LIMIT:

        return "Medium"


    if vehicle_count <= HIGH_LIMIT:

        return "High"


    return "Very High"


def load_model():

    return joblib.load(
        MODEL_PATH
    )


def predict_congestion(
    model,
    vehicle_count,
    average_speed
):

    prediction = model.predict([[
        vehicle_count,
        average_speed
    ]])

    return prediction[0]