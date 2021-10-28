from sqlalchemy import create_engine

OUTPATH = r"~\Desktop\Temp\manual_traffic_counts"
HEADEROUT = r"~\Desktop\Temp\manual_traffic_counts\header_import.csv"
DATAOUT = r"~\Desktop\Temp\manual_traffic_counts\header_import.csv"
PROBLEM_FILES = r"~\Desktop\Temp\manual_traffic_counts\PROBLEM_FILES.csv"

ENGINE = create_engine(
    "postgresql://postgres:Lin3@r1in3!431@linearline.dedicated.co.za:5432/gauteng"
)

HEADER = [
        "header_id",
        "counted_by",
        "tc_station_name",
        "count_type_id",
        "count_date_start",
        "count_weather",
        "h_station_date",
        "growth_rate_use",
        "count_interval",
    ]
                
DATA = [
        "count_hour",
        "light",
        "heavy",
        "bus",
        "taxi",
        "total",
        "header_time",
        "header_date",
        "count_time",
        "header_id",
    ]
