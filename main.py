import pandas as pd
import os
import csv
import uuid
from tkinter import filedialog
from tkinter import *
from typing import List

import config

DROP_IF = ["DO NOT FILL IN", "DO NOT F"]


class Count(object):
    def __init__(self) -> None:
        self.type, self.path = self.gui()
        self.src = self.getfiles(self.path)
        if self.type == "Cumulative Count":
            self.cumulative_etl(self.src)
        elif self.type == "TCS Trust":
            self.tcs_etl

    def gui(self):
        f = ""

        def select_folder():
            f = filedialog.askdirectory()
            root.destroy()

        root = Tk()
        root.geometry("400x150+100+100")
        root.title("Manual Count Data Import")

        menu = StringVar()
        menu.set("Select Count Type")
        drop = OptionMenu(root, menu, "Cumulative Count", "TCS Trust")
        drop.pack()

        button1 = Button(root, text="Select Folder", command=select_folder)
        button1.pack()

        root.mainloop()

        return drop, str(f)

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

    def cumulative_etl(self, src: List[str]) -> pd.DataFrame:
        self.src = self.getfiles(self.path)
        try:
            for file in self.src:

                xls = pd.ExcelFile(file)

                header_out_df = pd.DataFrame()
                data_out_df = pd.DataFrame()

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

                    # TODO: process data so that count is only for that hour (not cumulative)
                    # TODO: make sure the below works
                    data["light"] = data["light"].diff().fillna(data["light"])
                    data["heavy"] = data["heavy"].diff().fillna(data["heavy"])
                    data["bus"] = data["bus"].diff().fillna(data["bus"])
                    data["taxi"] = data["taxi"].diff().fillna(data["taxi"])
                    data["total"] = data["total"].diff().fillna(data["total"])

                    data_out_df = data_out_df.append(data)

                    header_out_df.to_csv(
                        config.HEADEROUT,
                        mode="a",
                    )
                    data_out_df.to_csv(
                        config.DATAOUT,
                        mode="a",
                    )

        except Exception:
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

    def tcs_etl(self, src: List[str]) -> pd.DataFrame:
        self.src = self.getfiles(self.path)
        try:
            for file in self.src:

                xls = pd.ExcelFile(file)

                header_out_df = pd.DataFrame()
                data_out_df = pd.DataFrame()

                for sheet in xls.sheet_names:
                    df = pd.read_excel(file, sheet_name=sheet, header=None)

                    header = {
                        "header_id": [str(uuid.uuid4())],
                        "counted_by": ["TCS Trust"],
                        "tc_station_name": [str(df.loc[4, 8]) + str(df.loc[5, 8])],
                        "count_type_id": 3,
                        "count_date_start": [df.loc[2, 1]],
                        "count_weather": [df.loc[1, 2]],
                        "h_station_date": [
                            str(df.loc[4, 8])
                            + str(df.loc[5, 8])
                            + "_"
                            + str(df.loc[2, 1])
                        ],
                        "growth_rate_use": [str("y")],
                        "count_interval": [60],
                        "latitude": [df.loc[14, 8]],
                        "longitude": [df.loc[15, 8]],
                        "kilometer_dist": [df.loc[8, 8]],
                        "road_link": [df.loc[6, 8]],
                        "type_of_count": [df.loc[13, 8]],
                        "description": [
                            "Between "
                            + str(df.loc[9, 8])
                            + " and "
                            + str(df.loc[10, 8])
                        ],
                        "no_of_hours": [df.loc[24, 8]],
                        "no_days": [df.loc[25, 8]],
                    }
                    header_temp = pd.DataFrame(header)
                    header_out_df = header_out_df.append(header_temp)
                    header_out_df = header_out_df.drop_duplicates()

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
                    data["header_id"] = header_temp.loc[0, "header_id"]

                    data["count_hour"] = pd.to_datetime(
                        data["count_hour"].str[:8], format="%H"
                    ).dt.time

                    hour = data["count_hour"].astype(str)
                    data["count_time"] = header_temp.loc[0, "count_date_start"]
                    data["count_time"] = pd.to_datetime(
                        data["count_time"], format="%y/%m/%d"
                    ) + pd.to_timedelta(hour)

                    data["header_date"] = header_temp.loc[0, "count_date_start"]
                    data_out_df = data_out_df.append(data)
                    data_out_df = data_out_df.drop_duplicates()

                    header_out_df.to_csv(
                        config.HEADEROUT,
                        mode="a",
                    )
                    data_out_df.to_csv(
                        config.DATAOUT,
                        mode="a",
                    )

        except Exception:
            with open(
                os.path.expanduser(config.PROBLEM_FILES),
                "a",
                newline="",
            ) as f:
                write = csv.writer(f)
                write.writerows([[file]])
            pass

        return header_out_df, data_out_df

    def __repr__(self) -> str:
        try:
            return repr(self.df)
        except Exception:
            return repr(self)


if __name__ == "__main__":

    if not os.path.exists(os.path.expanduser(config.OUTPATH)):
        os.makedirs(os.path.expanduser(config.OUTPATH))

    Count()

    # header.to_csv(
    #     config.HEADEROUT,
    #     mode="a",
    # )
    # data.to_csv(
    #     config.DATAOUT,
    #     mode="a",
    # )

    print("COMPLETED")
