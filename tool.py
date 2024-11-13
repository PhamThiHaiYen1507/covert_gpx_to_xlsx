import streamlit as st
import gpxpy
import pandas as pd
import io

st.title("Chuyển đổi GPX sang Excel")

# Tải lên file GPX
uploaded_file = st.file_uploader("Chọn file GPX", type=["gpx"])

if uploaded_file is not None:
    # Đọc và xử lý file GPX
    gpx = gpxpy.parse(uploaded_file)
    data = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                heart_rate = None
                if point.extensions:
                    for ext in point.extensions:
                        hr_element = ext.find('.//{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr')
                        if hr_element is not None:
                            heart_rate = hr_element.text
                            break
                time_no_timezone = point.time.replace(tzinfo=None) if point.time else None
                data.append({
                    'Latitude': point.latitude,
                    'Longitude': point.longitude,
                    'Elevation': point.elevation,
                    'Time': time_no_timezone,
                    'Heart Rate': heart_rate
                })

    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(data)

    # Xuất dữ liệu ra file Excel
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    # Tên file xuất ra
    output_filename = f"{uploaded_file.name.split('.')[0]}.xlsx"

    # Hiển thị nút tải xuống
    st.download_button(
        label="Tải xuống file Excel",
        data=output,
        file_name=output_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
