import pandas as pd
import os
import uuid

import csv
from io import StringIO

from datetime import datetime

# from psycopg2 import Error

# from tkinter import filedialog
# from tkinter import *

from typing import List

# from scipy.stats import kstest

import config

DROP_IF = ["DO NOT FILL IN", "DO NOT F"]


class Count(object):
    def __init__(self, type, path, csv_export, sql_export) -> None:
        self.header_out_df = pd.DataFrame(columns=config.HEADER)
        self.data_out_df = pd.DataFrame(columns=config.DATA)
        self.type = type
        self.path = path
        self.csv_export = csv_export
        self.sql_export = sql_export

    def choose(self, df, file):
        if self.type == "Basic Format":
            self.cumulative_etl(df, file)
        elif (self.type == "Manual Traffic Counting Sheet") and (
            df.loc[3, 5] == "Total"
        ):
            self.etl_no_veryheavy(df, file)
        elif (self.type == "Manual Traffic Counting Sheet") and (
            df.loc[3, 6] == "Total"
        ):
            self.etl_template_form(df, file)
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
    def hourly_count_calc(self, df):
        df2 = df
        df["light"] = df["light"].diff().fillna(df["light"])
        df["heavy"] = df["heavy"].diff().fillna(df["heavy"])
        df["bus"] = df["bus"].diff().fillna(df["bus"])
        df["taxi"] = df["taxi"].diff().fillna(df["taxi"])
        df["total"] = df["total"].diff().fillna(df["total"])
        if (df.values < 0).any():
            return df2
        else:
            return df

    def check_if_calculated(self, data):
        a = pd.Series(data["total"])
        normalized_df = (a - a.min()) / (a.max() - a.min())
        l = []
        cnt = a.count()
        for i in range(cnt):
            if i == 0:
                l.append(True)
            elif (a.iloc[i] >= a.iloc[i-1]):
                l.append(True)
            else:
                l.append(False)
        if ((normalized_df.iloc[0] == 0) & (normalized_df.iloc[-1] == 1)) and all(element == True for element in l):
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

    def etl_no_veryheavy(self, df, file) -> pd.DataFrame:

        ## UNCOMMENT THIS WHEN WORKING WITH FILES
        # xls = pd.ExcelFile(file)
        # df = pd.read_excel(file, sheet_name=xls.sheet_names, header=None)
        # for key, df in df.items():

        if df.loc[0, 0] == "MANUAL TRAFFIC COUNTING SHEET":

            if pd.isnull(df.loc[23, 8]):
                weather = "sunny"
            else:
                weather = df.loc[23, 8]

            gid = str(uuid.uuid4())

            header = {
                "header_id": [gid],
                "document_url": file,
                "counted_by": [df.loc[16, 8]],
                "tc_station_name": [str(df.loc[4, 8]) + str(df.loc[5, 8])],
                "count_type_id": 3,
                "count_date_start": [df.loc[2, 1]],
                "count_weather": [weather],
                "h_station_date": [gid],
                # [
                #     str(df.loc[4, 8]) + str(df.loc[5, 8]) + "_" + str(df.loc[2, 1])
                # ],
                "growth_rate_use": [str("Y")],
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
            data["count_hour"] = data["count_hour"].str[:2]
            data["h_station_date"] = header_temp.loc[0, "h_station_date"]
            data["tcname"] = header_temp.loc[0, "tc_station_name"]

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
            if header_temp["count_duration_hours"].any() == 18:
                data["count_type_id"] = 4
            else:
                pass

            self.header_out_df = self.header_out_df.merge(header_temp, how="outer")
            self.data_out_df = self.data_out_df.merge(data, how="outer")
            with open(
                os.path.expanduser(config.FILES_COMPLETE),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])

        else:
            print("something wrong with the NO VERY HEAVY PROCESS")
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def etl_template_form(self, df, file) -> pd.DataFrame:

        ## UNCOMMENT THIS WHEN WORKING WITH FILES
        # xls = pd.ExcelFile(file)
        # df = pd.read_excel(file, sheet_name=xls.sheet_names, header=None)
        # for key, df in df.items():

        if (
            df.loc[0, 0] == "MANUAL TRAFFIC COUNTING SHEET"
            or df.loc[0, 0] == "TRAFFIC COUNTING SHEET"
        ):

            if pd.isnull(df.loc[23, 9]):
                weather = "sunny"
            else:
                weather = df.loc[23, 9]

            gid = str(uuid.uuid4())

            header = {
                "header_id": [gid],
                "document_url": file,
                "counted_by": [df.loc[16, 9]],
                "tc_station_name": [str(df.loc[4, 9]) + str(df.loc[5, 9])],
                "count_type_id": 3,
                "count_date_start": [df.loc[2, 1]],
                "count_weather": [weather],
                "h_station_date": [gid],
                # [
                #     str(df.loc[4, 8]) + str(df.loc[5, 8]) + "_" + str(df.loc[2, 1])
                # ],
                "growth_rate_use": [str("Y")],
                "count_interval": [60],
                "latitude": [df.loc[14, 9]],
                "longitude": [df.loc[15, 9]],
                "kilometer_dist": [df.loc[8, 9]],
                "road_link": [df.loc[6, 9]],
                "type_of_count": [df.loc[13, 9]],
                "description": [
                    "Between " + str(df.loc[9, 9]) + " and " + str(df.loc[10, 9])
                ],
                "count_duration_hours": [df.loc[24, 9]],
                "no_days": [df.loc[25, 9]],
            }
            header_temp = pd.DataFrame(header)

            data = df.loc[4:29, 0:6]
            data = data[(data[0] != "Subtotal A") & (data[0] != "Subtotal B")]
            data = data.dropna(thresh=5)
            data.rename(
                columns={
                    0: "count_hour",
                    1: "light",
                    2: "heavy",
                    3: "veryheavy",
                    4: "bus",
                    5: "taxi",
                    6: "total",
                },
                inplace=True,
            )
            data["count_hour"] = data["count_hour"].str[:2]
            data["h_station_date"] = header_temp.loc[0, "h_station_date"]
            data["tcname"] = header_temp.loc[0, "tc_station_name"]

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
            if header_temp["count_duration_hours"].any() == 18:
                data["count_type_id"] = 4
            else:
                pass

            self.header_out_df = self.header_out_df.merge(header_temp, how="outer")
            self.data_out_df = self.data_out_df.merge(data, how="outer")
            with open(
                os.path.expanduser(config.FILES_COMPLETE),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])

        else:
            print("something wrong with the TEMPLATE FORM method")
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def execute(self, file):

        # TODO: add sheet name to problem files output

        try:
            df = pd.read_excel(file, sheet_name=None, header=None)
            for key, df in df.items():
                self.choose(df, file)
        except Exception:
            print("something wrong with the EXECUTE method")
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def psql_insert_copy(self, table, conn, keys, data_iter):
        """
        Execute SQL statement inserting data

        Parameters
        ----------
        table : pandas.io.sql.SQLTable
        conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
        keys : list of str
            Column names
        data_iter : Iterable that iterates the values to be inserted
        """
        # gets a DBAPI connection that can provide a cursor
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ", ".join('"{}"'.format(k) for k in keys)
            if table.schema:
                table_name = "{}.{}".format(table.schema, table.name)
            else:
                table_name = table.name

            sql = "COPY {} ({}) FROM STDIN WITH CSV".format(table_name, columns)
            cur.copy_expert(sql=sql, file=s_buf)

    def export(self):
        self.header_out_df = self.header_out_df.drop_duplicates()
        self.data_out_df = self.data_out_df.drop_duplicates()

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
        if self.csv_export == True:
            try:
                # EXPORT AS CSV
                self.header_out_df.to_csv(config.HEADEROUT, mode="a", index=False)
                print("CSV HEADER DONE")
            except Exception:
                print("""something went wrong with the HEADER CSV EXPORT""")
                pass

            try:
                self.data_out_df.to_csv(config.DATAOUT, mode="a", index=False)
                print("CSV DATA DONE")
            except Exception:
                print("""something went wrong with the DATA CSV EXPORT""")
                pass
        else:
            pass

        if self.sql_export == True:
            try:
                ## EXPORT INTO MAIN TABLE FASTER METHOD
                self.header_out_df.to_sql(
                    "manual_count_header",
                    config.ENGINE,
                    schema="trafc",
                    if_exists="append",
                    index=False,
                    method=self.psql_insert_copy,
                )

                print("HEADER DONE")
            except Exception:
                print(
                    """something went wrong with the HEADER: please check if the data is in the database 
                    or something on the database side. check the triggers on the manual_count_data table"""
                )
                pass

            try:
                ## EXPORT INTO MAIN TABLE FASTER METHOD
                self.data_out_df.to_sql(
                    "manual_count_data",
                    config.ENGINE,
                    schema="trafc",
                    if_exists="append",
                    index=False,
                    method=self.psql_insert_copy,
                )

                print("DATA DONE")
            except Exception:
                print(
                    """something went wrongwith the DATA: please check if the data is in the database 
                    or something on the database side. check the triggers on the manual_count_data table"""
                )
                pass
        else:
            pass


# if __name__ == "__main__":
#     execute()
