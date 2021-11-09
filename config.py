from sqlalchemy import create_engine

OUTPATH = r"~\Desktop\Temp\manual_traffic_counts"
HEADEROUT = r"~\Desktop\Temp\manual_traffic_counts\header_import.csv"
DATAOUT = r"~\Desktop\Temp\manual_traffic_counts\data_import.csv"
PROBLEM_FILES = r"~\Desktop\Temp\manual_traffic_counts\PROBLEM_FILES.csv"
DROP_IF = ["DO NOT FILL IN", "DO NOT F"]

ENGINE = create_engine(
    r"postgresql://postgres:Lin3@r1in3!431@linearline.dedicated.co.za:5432/gauteng"
)

SITE = [
    "node_id",
    "leg_id",
    "tcname",
    "description",
    "count_station_type_id",
    "count_cycle_id",
    "axle_group_id",
    "congestion_group_id",
    "growth_group_id",
    "traffic_type_id",
    "publictrans_group_id",
    "geom",
    "max_speed",
    "location",
    "owner",
    "latitude",
    "longitude",
]

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
    "count_duration_hours",
    "no_days",
]

DATA = [
    "count_hour",
    "light",
    "heavy",
    "bus",
    "taxi",
    "total",
    # "header_time",
    "header_date",
    "count_time",
    "header_id",
    "h_station_date",
    "tcname"
]

KS_SAMPLE = [56, 247, 357, 481, 606, 738, 865, 1009, 1225, 1402, 1602, 1762]

KS_SAMPLE2 = [100, 500, 1000, 2000, 5000, 7000, 9000, 10000, 15000, 20000, 30000, 45000]

# TEST_DATA ={
#     "count_hour": ['06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00'],
#     "light":[223,188,106,113,117,91,85,126,140,143,208,172],
#     "heavy":[6,13,14,21,25,28,19,25,24,34,39,36],
#     "bus":,
#     "taxi":,
#     "total":,
#     "header_time":,
#     "header_date":,
#     "count_time":,
#     "header_id":,
# }


# TEST_HEADER = {
#     "header_id":,
#     "document_url":,
#     "counted_by":,
#     "tc_station_name":,
#     "count_type_id":,
#     "count_date_start":,
#     "count_weather":,
#     "h_station_date":,
#     "growth_rate_use":,
#     "count_interval":,
#     "latitude":,
#     "longitude":,
#     "kilometer_dist":,
#     "road_link":,
#     "type_of_count":,
#     "description":,
#     "no_of_hours":,
#     "no_days":
# }
