import pandas as pd
import os
import uuid
import csv

from datetime import datetime

# from tkinter import filedialog
# from tkinter import *

from typing import List

# from scipy.stats import kstest

import config

DROP_IF = ["DO NOT FILL IN", "DO NOT F"]


class Count(object):
    def __init__(self, type, path) -> None:
        self.header_out_df = pd.DataFrame(columns=config.HEADER)
        self.data_out_df = pd.DataFrame(columns=config.DATA)
        self.type = type
        self.path = path

    def choose(self, df, file):
        if self.type == "Basic Format":
            self.cumulative_etl(df, file)
        elif self.type == "Detailed Manual Traffic Count Form":
            self.tcs_etl(df, file)
        else:
            pass

    def getfiles(self, path) -> List[str]:
        print("COLLECTING FILES......")
        src = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".xlsx") or name.endswith(".csv"):
                    p = os.path.join(root, name)
                    src.append(p)
        src = list(set(src))
        return src

    # ! process data so that count is only for that hour (not cumulative)
    def hourly_count_calc(self, data):
        data["light"] = data["light"].diff().fillna(data["light"])
        data["heavy"] = data["heavy"].diff().fillna(data["heavy"])
        data["bus"] = data["bus"].diff().fillna(data["bus"])
        data["taxi"] = data["taxi"].diff().fillna(data["taxi"])
        data["total"] = data["total"].diff().fillna(data["total"])
        return data

    def check_if_calculated(self, data):
        a = data["total"]
        normalized_df = (a - a.min()) / (a.max() - a.min())
        if (normalized_df.head(1).all() == 0.0) & (normalized_df.tail(1).all() == 1):
            return self.hourly_count_calc(data)
        else:
            return data

    def cumulative_etl(self, df, file) -> pd.DataFrame:

        ## UNCOMMENT THIS WHEN WORKING WITH FILES
        # xls = pd.ExcelFile(file)
        # df = pd.read_excel(file, sheet_name=xls.sheet_names, header=None)
        # for key, df in df.items():

        header = {
            "header_id": [str(uuid.uuid4())],
            "document_url": file,
            "counted_by": ["CKDM"],
            "tc_station_name": [df.loc[0, 1]],
            "count_type_id": 3,
            "count_date_start": [df.loc[1, 1]],
            "count_weather": [df.loc[2, 1]],
            "h_station_date": [df.loc[0, 1] + "_" + str(df.loc[1, 1])],
            "growth_rate_use": [str("y")],
            "count_interval": [60],
        }
        header_temp = pd.DataFrame(header)
        self.header_out_df = self.header_out_df.merge(header_temp, how="outer")
        # self.header_out_df = self.header_out_df.drop_duplicates()

        data = df.loc[6:24, 0:5]
        data.dropna(thresh=5)
        data.rename(
            columns={
                0: "count_hour",
                1: "light",
                2: "heavy",
                3: "bus",
                4: "taxi",
                5: "total",
            },
            inplace=True,
        )

        data = data[data.count_hour.isin(DROP_IF) == False]

        data["header_id"] = header_temp.loc[0, "header_id"]

        data["count_hour"] = pd.to_datetime(
            data["count_hour"].str[:8], format="%H:%M:%S"
        ).dt.time

        hour = data["count_hour"].astype(str)
        data["count_time"] = header_temp.loc[0, "count_date_start"]
        data["count_time"] = pd.to_datetime(
            data["count_time"], format="%y/%m/%d"
        ) + pd.to_timedelta(hour)

        data["header_date"] = header_temp.loc[0, "count_date_start"]

        data = self.check_if_calculated(data)
        self.data_out_df = self.data_out_df.merge(data, how="outer")
        self.data_out_df = self.data_out_df.drop_duplicates()

    def tcs_etl(self, df, file) -> pd.DataFrame:

        ## UNCOMMENT THIS WHEN WORKING WITH FILES
        # xls = pd.ExcelFile(file)
        # df = pd.read_excel(file, sheet_name=xls.sheet_names, header=None)
        # for key, df in df.items():

        if df.loc[0, 0] == "MANUAL TRAFFIC COUNTING SHEET":
            header = {
                "header_id": [str(uuid.uuid4())],
                "document_url": file,
                "counted_by": ["Detailed Manual Traffic Count Form"],
                "tc_station_name": [str(df.loc[4, 8]) + str(df.loc[5, 8])],
                "count_type_id": 3,
                "count_date_start": [df.loc[2, 1]],
                "count_weather": [df.loc[1, 2]],
                "h_station_date": [str(uuid.uuid4())],
                # [
                #     str(df.loc[4, 8]) + str(df.loc[5, 8]) + "_" + str(df.loc[2, 1])
                # ],
                "growth_rate_use": [str("y")],
                "count_interval": [60],
                "latitude": [df.loc[14, 8]],
                "longitude": [df.loc[15, 8]],
                "kilometer_dist": [df.loc[8, 8]],
                "road_link": [df.loc[6, 8]],
                "type_of_count": [df.loc[13, 8]],
                "description": [
                    "Between " + str(df.loc[9, 8]) + " and " + str(df.loc[10, 8])
                ],
                "count_duration_hours": [df.loc[24, 8]],
                "no_days": [df.loc[25, 8]],
            }
            header_temp = pd.DataFrame(header)

            data = df.loc[4:29, 0:5]
            data = data[(data[0] != "Subtotal A") & (data[0] != "Subtotal B")]
            data = data.dropna(thresh=5)
            data.rename(
                columns={
                    0: "count_hour",
                    1: "light",
                    2: "heavy",
                    3: "bus",
                    4: "taxi",
                    5: "total",
                },
                inplace=True,
            )
            # ! GET TIME TO DATETIME
            data["count_hour"] = data["count_hour"].str[:2]
            data["h_station_date"] = header_temp.loc[0, "h_station_date"]
            data["tcname"] = header_temp.loc[0, "tc_station_name"]

            # ! GET TIME TO DATETIME
            # data["count_hour"] = pd.to_datetime(
            #     data["count_hour"].str[:8], format="%H"
            # ).dt.time

            hour = data["count_hour"].astype(str)
            data["count_time"] = header_temp.loc[0, "count_date_start"]
            data["count_time"] = pd.to_datetime(
                data["count_time"], format="%y/%m/%d"
            ) + pd.to_timedelta(hour)

            data["header_date"] = header_temp.loc[0, "count_date_start"]

            new_datetime = (
                header_temp.loc[0, "count_date_start"].strftime("%Y-%m-%d") + " " + hour
            )
            data["count_hour"] = pd.to_datetime(new_datetime)

            data = self.check_if_calculated(data)

            header_temp["count_duration_hours"] = data["total"].notnull().sum()

            self.header_out_df = self.header_out_df.merge(header_temp, how="outer")
            self.data_out_df = self.data_out_df.merge(data, how="outer")
        else:
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def execute(self, file):
        if not os.path.exists(os.path.expanduser(config.OUTPATH)):
            os.makedirs(os.path.expanduser(config.OUTPATH))

        # for file in path:
        try:
            df = pd.read_excel(file, sheet_name=None, header=None)
            for key, df in df.items():
                self.choose(df, file)
        except Exception:
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def export(self):
        self.header_out_df = self.header_out_df.drop_duplicates()
        self.data_out_df = self.data_out_df.drop_duplicates()

        try:
            self.header_out_df = self.header_out_df.drop(
                columns=[
                    "header_id",
                    "latitude",
                    "longitude",
                    "kilometer_dist",
                    "road_link",
                    "type_of_count",
                    "description",
                    "no_days",
                ]
            )
            self.data_out_df = self.data_out_df.drop(
                columns=["header_date", "count_time", "header_id"]
            )

            # EXPORT AS CSV TO CHECK DATA
            # self.header_out_df.to_csv(config.HEADEROUT, mode="a", index=False)
            # self.data_out_df.to_csv(config.DATAOUT, mode="a", index=False)

            ## EXPORT INTO TEMP TABLE IF NEEDED BEFORE INSERTING TO MAIN TABLE
            self.header_out_df.to_sql(
                "temp_manual_count_header",
                config.ENGINE,
                schema="trafc",
                if_exists="replace",
                index=False,
            )
            self.data_out_df.to_sql(
                "temp_manual_count_data",
                config.ENGINE,
                schema="trafc",
                if_exists="replace",
                index=False,
            )

            ## EXPORT INTO MAIN TABLE
            # self.header_out_df.to_sql(
            #     "manual_count_header",
            #     config.ENGINE,
            #     schema="trafc",
            #     if_exists="append",
            #     index=False
            # )

            # self.data_out_df.to_sql(
            #     "manual_count_data",
            #     config.ENGINE,
            #     schema="trafc",
            #     if_exists="append",
            #     index=False
            # )
            print("DONE")
        except Exception:
            print("something went wrong")
            pass


# if __name__ == "__main__":
#     execute()
