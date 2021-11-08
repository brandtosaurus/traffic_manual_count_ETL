import main
import config
import pytest
import pandas as pd

type = 'TCS Trust'
path = r'C:\Users\MB2705851\OneDrive - Surbana Jurong Private Limited\Manuals & Guidelines\Traffic\Manual count import templates\TCS Trust'

p= main.Count(type,path)

# print(p.src)
# p = main.Count(str("TCS Trust"), str(path))
# TOTAL = len(p.src)
# print(TOTAL)
# count = 0
# while count <= TOTAL:
#     for file in p.src:
#         p.run(file)
#         count += 1

# header_out_df = p.header_out_df.drop_duplicates()
# data_out_df = p.data_out_df.drop_duplicates()
# print(p.header_out_df)
# print(p.data_out_df)
# data_out_df.to_csv(
#     config.DATAOUT,
#     mode="a",index=False
# )

# print("COMPLETED")

# c = main.Count(type, path)
# pth = c.getfiles(c.path)
# # df_list = c.df_list(c.getfiles(c.path))
# p.execute(pth)
# print(p.header_out_df)
# p.export()

def run():
    p = main.Count(str(type), str(path))
    src = p.getfiles(path)
    TOTAL = len(src)
    count = 0
    # while count <= TOTAL:
        # for file in src:
        #     count += 1
    p.execute(src)
        # self.countChanged.emit(int(count / TOTAL * 100))
    p.export()

run()


# df_list = list()
# path = p.src
# for file in path:
#     xls = pd.ExcelFile(file)
#     df = pd.read_excel(file, sheet_name=xls.sheet_names, header=None)
#     for key, df in df.items():
#         df_list.append(df)

# print(df_list)
    # sheet[path].append(xls.sheet_names)
# print(sheet)
    # df = pd.read_excel(file, sheet_name=None)
    # for key, df in df.items():
    #     print(key)
    # for sheet in xls.sheet_names[0]:
    #     print(sheet)
    #     # df = pd.read_excel(file, sheet_name=sheet, header=None)
    #     df = xls.parse(sheet)
    #     print(df)
    #     break

        