from config import (
    MIN_GREEN_TIME,
    MAX_GREEN_TIME
)


def optimize_signal(
    vehicle_count,
    congestion
):

    if congestion == "Low":

        green_time = 20


    elif congestion == "Medium":

        green_time = 35


    elif congestion == "High":

        green_time = 50


    else:

        green_time = 70


    # Additional adjustment
    if vehicle_count > 40:

        green_time += 10


    green_time = max(
        MIN_GREEN_TIME,
        green_time
    )


    green_time = min(
        MAX_GREEN_TIME,
        green_time
    )


    return green_time