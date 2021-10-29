from sqlalchemy import create_engine

OUTPATH = r"~\Desktop\Temp\manual_traffic_counts"
HEADEROUT = r"~\Desktop\Temp\manual_traffic_counts\header_import.csv"
DATAOUT = r"~\Desktop\Temp\manual_traffic_counts\header_import.csv"
PROBLEM_FILES = r"~\Desktop\Temp\manual_traffic_counts\PROBLEM_FILES.csv"

ENGINE = create_engine(
    "postgresql,//postgres,Lin3@r1in3!431@linearline.dedicated.co.za,5432/gauteng"
)

HEADER = [
    "header_id",
    "document_url", 
    "counted_by", 
    "tc_station_name",
    "count_type_id", 
    "count_date_start", 
    "count_weather",
    "h_station_date",
    "growth_rate_use",
    "count_interval", 
    "latitude", 
    "longitude", 
    "kilometer_dist",
    "road_link",
    "type_of_count", 
    "description",
    "no_of_hours", 
    "no_days"
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

KS_SAMPLE = [56, 247, 357, 481, 606, 738, 865, 1009, 1225, 1402, 1602, 1762]

KS_SAMPLE2 = [100, 500, 1000, 2000, 5000, 7000, 9000, 10000, 15000, 20000, 30000, 45000]
