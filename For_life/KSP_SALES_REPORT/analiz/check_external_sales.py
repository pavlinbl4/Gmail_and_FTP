"""
провести анализ файла внешних продаж с определением
- самый скачиваемый снимок
- самая дорогая продажа
- снимок, который принес больше всего прибыли
"""

import pandas as pd

test_file = '/Volumes/big4photo/Documents/Kommersant/Reports_files/report_in_CSV/only_external_sales_report_2021_Ноябрь.csv'

df = pd.read_csv(test_file)
df = df[df['income'] != 0]  # удаляю строки, где продажа равно нулю

print(f'количество уникальных photo_id - {df.image_id.nunique()}')  # количество уникальных photo_id
print(f'количество уникальных клиентов - {df.client.nunique()}')  # количество уникальных клиентов
print(f'суммарный доход {df.income.sum().round(2)}')

itog = df.groupby(['image_id'], as_index='image_id') \
    .aggregate({'income': sum, 'image_id': 'count'}) \
    .sort_values('income') \
    .rename(columns={'image_id': 'sold_time'})

m_income = itog.income.idxmax()
m_sold = itog.sold_time.idxmax()

print(f'снимок {m_income} принес максимальный доход - {itog.loc[m_income].income}')
print(f'снимок {m_sold} проданн максимальное количество раз - {itog.loc[m_sold].sold_time}')
