""" модуль генерирующий поисковые запросы из данных по таблице"""

import pandas as pd

goods_file = '/Volumes/big4photo/Downloads/products_no_barcode.xlsx'

def create_search(goods_file):
    df = pd.read_excel(goods_file)
    for i in range(40):
        if df.loc[i, 'description'] == 0:
            search_text = ''
            one_row = df.loc[i, ['product_title', 'trademark', 'value', 'unit']]
            one_row = one_row.values.astype(str)
            for i in one_row:
                words = " ".join(i.split())
                word = word.replace(',','')
                if words != '0':
                    search_text += words + ' '
        else:
            search_text = df.loc[i, 'description']
            search_text = search_text.replace(',','')
        # search_text = search_text.strip().replace(" ",'+')
        # return search_text
        print(search_text)


create_search(goods_file)
