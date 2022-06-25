import os
import csv

import pandas as pd

import calcs
import config


if __name__ == "__main__":
    if not os.path.exists(os.path.expanduser(config.OUTPATH)):
        os.makedirs(os.path.expanduser(config.OUTPATH))

    if not os.path.exists(os.path.expanduser(config.FILES_COMPLETE)):
        with open(
                os.path.expanduser(config.FILES_COMPLETE),
                "w",
            ) as f:
                pass

    fileComplete = os.path.expanduser(config.FILES_COMPLETE)
    try:
        fileComplete = pd.read_csv(fileComplete, header=None, sep="\n")
        fileComplete = fileComplete[0].tolist()
    except Exception:
        fileComplete = []

    p = calcs.Count("Manual Traffic Counting Sheet", r"C:\FTP\Trafftrans", True, True)
    src = p.getfiles(r"C:\FTP\Trafftrans")

    files = [i for i in src if i not in fileComplete]

    for file in files:
        p.execute(file)
        with open(
                os.path.expanduser(config.FILES_COMPLETE),
                "a",
                newline="",
        ) as f:
            write = csv.writer(f)
            write.writerows([[file]])
            
    p.export()
