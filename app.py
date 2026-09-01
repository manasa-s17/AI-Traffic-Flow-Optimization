from flask import (
    Flask,
    render_template,
    jsonify
)

import cv2

from config import VIDEO_PATH

from traffic_engine import TrafficEngine

from congestion_model import (
    load_model,
    predict_congestion
)

from signal_optimizer import (
    optimize_signal
)

from database import (
    create_database,
    save_record,
    get_recent_records
)


app = Flask(__name__)


# Initialize system
engine = TrafficEngine()

model = load_model()

create_database()


@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html"
    )


@app.route("/api/analyze")
def analyze():

    cap = cv2.VideoCapture(
        str(VIDEO_PATH)
    )


    total_count = 0

    total_speed = 0

    frame_count = 0


    vehicle_types = {

        "car": 0,

        "motorcycle": 0,

        "bus": 0,

        "truck": 0
    }


    # Process selected frames
    while frame_count < 100:

        success, frame = cap.read()


        if not success:

            break


        processed_frame, data = (
            engine.process_frame(frame)
        )


        total_count += data[
            "vehicle_count"
        ]


        total_speed += data[
            "average_speed"
        ]


        for vehicle in vehicle_types:

            vehicle_types[
                vehicle
            ] += data[
                "vehicle_types"
            ][vehicle]


        frame_count += 1


    cap.release()


    if frame_count == 0:

        return jsonify({
            "error":
            "Unable to read video."
        }), 500


    average_count = (
        total_count /
        frame_count
    )


    average_speed = (
        total_speed /
        frame_count
    )


    congestion = predict_congestion(

        model,

        average_count,

        average_speed
    )


    green_time = optimize_signal(

        average_count,

        congestion
    )


    save_record(

        round(average_count),

        vehicle_types,

        round(
            average_speed,
            2
        ),

        congestion,

        green_time
    )


    return jsonify({

        "vehicle_count":
            round(average_count),

        "vehicle_types":
            vehicle_types,

        "average_speed":
            round(
                average_speed,
                2
            ),

        "congestion":
            congestion,

        "green_time":
            green_time
    })


@app.route("/api/history")
def history():

    records = get_recent_records()

    return jsonify(records)


if __name__ == "__main__":

    app.run(
        debug=True
    )