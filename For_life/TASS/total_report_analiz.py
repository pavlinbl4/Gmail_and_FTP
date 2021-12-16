"""
скрипт для слияния данных из многостраничнах   elsx файлов в единный датафрэйм
"""


import pandas as pd

report_file = '/Volumes/big4photo/Documents/TASS/Tass_total_report_from_2015.xlsx'

data = pd.read_excel(report_file, None)  # в данном случае на выходе словарь {sheet_name:dataframe}

df = pd.DataFrame()  # получаю датафрэйм из всех старниц в файле
for sheet in data:
    if sheet != 'Sheet':
        df_month = data[sheet] #.set_index('photo_id')
        df = df.append(df_month, sort=True)
print(f"количество уникальных значений photo_id {df['photo_id'].nunique()}")


df.groupby("photo_id",as_index=False)\
    .aggregate({"income" : sum,'sold times': sum})\
    .sort_values("income")\
    .to_excel('/Volumes/big4photo/Documents/TASS/agg_income_from_2015.xlsx')

