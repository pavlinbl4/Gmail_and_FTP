"""
идея такая сравнива отчеты после добавления снимков и смотрю какие из них добавли
"""


import pandas as pd
import datacompy

pd.options.display.max_colwidth = 100

photo_base = '/Volumes/big4photo/Documents/TASS/Tass_data/all_TASS_images.xlsx'

last_df = pd.read_excel(photo_base,sheet_name='2022-03-24')
print(f'last_df = {last_df.shape}')

previos_df = pd.read_excel(photo_base,sheet_name='2022-03-22')
print(f'previos_df - {previos_df.shape}')

common = pd.merge(previos_df,last_df, on= ['image_id'],how='inner')
print(f'common - {common.shape}')


difference = datacompy.Compare(previos_df,last_df, join_columns=['image_id','image_date','image_caption']).df2_unq_rows



print(difference[['image_id','image_link']])



