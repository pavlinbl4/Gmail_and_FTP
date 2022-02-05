import os

title = "Готово"
message = "Файл скачан"
command = f'''
osascript -e 'display notification "{message}" with title "{title}"'
'''
os.system(command)