from xls2xlsx import XLS2XLSX
import os, fnmatch

report_dir = '/Volumes/big4photo/Downloads'

list_of_files = os.listdir(report_dir)
pattern = '*.xls'
count = 0
for file_name in list_of_files:
    if fnmatch.fnmatch(file_name, pattern):
        count += 1
        x2x = XLS2XLSX(f"{report_dir}/{file_name}")
        x2x.to_xlsx(f"{report_dir}/{file_name.capitalize()}x")
        os.remove(f"{report_dir}/{file_name}")

print(f"Сконвертированно {count} файлов")
