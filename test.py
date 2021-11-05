import main
import config
import pytest
import pandas as pd

type = 'TCS Trust'
path = r'C:\Users\MB2705851\OneDrive - Surbana Jurong Private Limited\Manuals & Guidelines\Traffic\Manual count import templates\TCS Trust'

p= main.Count(type,path)

print(p.src)
p = main.Count(str("TCS Trust"), str(path))
TOTAL = len(p.src)
print(TOTAL)
count = 0
while count <= TOTAL:
    for file in p.src:
        p.run(file)
        count += 1

header_out_df = p.header_out_df.drop_duplicates()
data_out_df = p.data_out_df.drop_duplicates()
print(p.header_out_df)
print(p.data_out_df)
header_out_df.to_csv(
        config.HEADEROUT,
        mode="a",index=False
    )
data_out_df.to_csv(
    config.DATAOUT,
    mode="a",index=False
)

print("COMPLETED")


# file = p.src
# print(file)
# for f in file:
#     xls = pd.ExcelFile(f)
#     print(xls.sheet_names)
#     for sheet in xls.sheet_names:
#         print(sheet)
#         df = pd.read_excel(f, sheet_name=sheet, header=None)
#         print(df)