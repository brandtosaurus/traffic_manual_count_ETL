from fpdf import FPDF

import plotly.express as px
import plotly
import kaleido

import pandas as pd
import os
from config import ENGINE

READ_MANUAL_TABLE = """
select * from trafc.manual_count_data where h_station_date = '190B_2006-11-16' 
"""

# df = pd.read_sql(sql=READ_MANUAL_TABLE, con=ENGINE)
# print(df)

# plt = px.line(df, x='count_hour', y=['light', 'heavy','veryheavy','bus','taxi','total'])

# plotly.io.write_image(plt, file=r'C:\Users\MB2705851\Desktop\Temp\pltx.png',format='png',width=700, height=450)
# plt=(r"C:\Users\MB2705851\Desktop\Temp\pltx.png")

smec_logo = r"C:\Users\MB2705851\Pictures\1. LOGOS\SMEC%20South%20Africa%20LOGO%20Navy.jpg"
class PDF(FPDF):

    def page(self):
        self.set_fill_color(255, 255, 255)
        self.rect(5.0, 5.0, 200.0,287.0)

    def header(self):
        self.image(smec_logo, x = 10, y = 8, w = 100, h = 20, type = '', link = '')
        self.cell(80)
        self.set_xy(25.0, 6.0)
        self.ln(20)

    # def graph(self):
    #     self.set_xy(40.0,25.0)
    #     self.image(plt,  link='', type='', w=700, h=450)

# if __name__ == '__main__':
pdf = PDF()
pdf.add_page()
pdf.alias_nb_pages()
pdf.set_font('Verdana', '', 12)
pdf.output(r'C:\Users\MB2705851\Desktop\Temp\test.pdf', 'F')