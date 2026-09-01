async function analyzeTraffic() {

    const button =
        document.getElementById(
            "analyzeButton"
        );

    const status =
        document.getElementById(
            "status"
        );


    button.disabled = true;

    button.innerText =
        "Analyzing...";


    status.innerText =
        "AI is analyzing traffic video...";


    try {

        const response =
            await fetch(
                "/api/analyze"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Analysis failed"
            );
        }


        document.getElementById(
            "vehicleCount"
        ).innerText =
            data.vehicle_count;


        document.getElementById(
            "averageSpeed"
        ).innerText =
            data.average_speed +
            " km/h";


        document.getElementById(
            "congestion"
        ).innerText =
            data.congestion;


        document.getElementById(
            "greenTime"
        ).innerText =
            data.green_time +
            " sec";


        const types =
            data.vehicle_types;


        document.getElementById(
            "vehicleTypes"
        ).innerHTML = `

            <p>🚗 Cars: ${types.car}</p>

            <p>🏍 Motorcycles:
                ${types.motorcycle}
            </p>

            <p>🚌 Buses:
                ${types.bus}
            </p>

            <p>🚚 Trucks:
                ${types.truck}
            </p>

        `;


        status.innerText =
            "Traffic analysis completed successfully.";


    } catch (error) {

        console.error(error);


        status.innerText =
            "Error: " +
            error.message;


    } finally {

        button.disabled = false;

        button.innerText =
            "Analyze Traffic";

    }

}