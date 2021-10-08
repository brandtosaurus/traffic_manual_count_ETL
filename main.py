import pandas as pd
import openpyxl
import os
import uuid
from datetime import datetime
from tkinter import filedialog
from tkinter import *
from typing import List

DROP_IF = ["DO NOT FILL IN", "DO NOT F"]


class Count(object):
    def __init__(self) -> None:
        self.path = self.gui()
        self.src = self.getfiles(self.path)
        self.etl(self.src)

    def gui(self):
        root = Tk()
        f = filedialog.askdirectory()
        root.destroy()
        return str(f)

    def getfiles(self, path: str) -> List[str]:
        print("COLLECTING FILES......")
        src = []
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.endswith(".xlsx"):
                    p = os.path.join(root, name)
                    src.append(p)
        src = list(set(src))
        return src

    def etl(self, src: List[str]):
        try:
            for file in self.src:

                xls = pd.ExcelFile(file)

                header_out_df = pd.DataFrame(
                    columns=[
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
                )
                data_out_df = pd.DataFrame(
                    columns=[
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
                )

                for sheet in xls.sheet_names:
                    df = pd.read_excel(file, sheet_name=sheet, header=None)

                    header = {
                        "header_id": [str(uuid.uuid4())],
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
                    header_out_df = header_out_df.append(header_temp)

                    data = df.loc[6:24, 0:5]
                    data.dropna
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

                    data_out_df = data_out_df.append(data)

                header_out_df.to_csv(
                    r"P:\C1570_RRAMS Central Karoo Dist Mun\3_Working\3-5_DivW\1 - RRAMS 2020\TIS\data recieved\header_db_import.csv",
                    mode="a",
                )
                data_out_df.to_csv(
                    r"P:\C1570_RRAMS Central Karoo Dist Mun\3_Working\3-5_DivW\1 - RRAMS 2020\TIS\data recieved\data_db_import.csv",
                    mode="a",
                )
        except Exception:
            print(file)


if __name__ == "__main__":
    Count()
    print("COMPLETED")
