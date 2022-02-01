import pandas as pd

names = ['product_id', 'action']
all_data = pd.DataFrame(columns=names) # создаю аустой датафрэйм с именами колонок

# пол

df = pd.read_csv('/Users/evgeniy/PycharmProjects/Gmail_and_FTP/Freelance test 1/befor_400_line/log.csv',
                 names=['product_id', 'action']
                )
df2 = pd.read_csv('/Users/evgeniy/PycharmProjects/Gmail_and_FTP/Freelance test 1/befor_400_line/log copy.csv',
                  names=['product_id', 'action'])

print(len(df))
print(len(df2))
new = pd.concat([all_data,df2])
print(new)