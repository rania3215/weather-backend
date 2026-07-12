import pandas as pd


def export_to_csv(records):

    data = []

    for record in records:

        data.append({
            "id": record.id,
            "location": record.location,
            "temperature": record.temperature,
            "humidity": record.humidity,
            "description": record.description,
            "created_at": record.created_at
        })


    df = pd.DataFrame(data)

    file_path = "weather_export.csv"

    df.to_csv(
        file_path,
        index=False
    )

    return file_path