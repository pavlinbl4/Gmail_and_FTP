import os
import pandas as pd

# names = ['product_id', 'action']
names = ['product_id', 'prodct_name', 'barcode_8','barcode_13']
all_data = pd.DataFrame(columns=names) # создаю аустой датафрэйм с именами колонок
print(all_data.columns)
# print(len(all_data))

dir_name = '/Users/evgeniy/PycharmProjects/Gmail_and_FTP/Freelance test 1/befor_400_line'

files = os.listdir(dir_name)

for file in files:
    if file.endswith(".csv"):
        df = pd.read_csv(f'{dir_name}/{file}',
                         names=names)
        all_data = pd.concat([all_data,df])
all_data.to_csv("/Users/evgeniy/PycharmProjects/Gmail_and_FTP/Freelance test 1/concat_separate_file.csv")