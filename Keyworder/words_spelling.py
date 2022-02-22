"""
модуль для проверки орфографии в списке ключевых слов - 20220222
"""


from spellchecker import SpellChecker

spell = SpellChecker(language='ru')
CRED = '\033[91m'
GREEN = '\33[32m'
CEND = '\033[0m'


def correct_bad_words(keywords):  # функция принимает список с ключевыми словами и возвращает исправленный список  слов
    spell.word_frequency.load_dictionary('my_custom_dictionary.gz')
    unknown_words = list(spell.unknown(keywords))  # слова которых нет в словаре или которые с ошибками
    known_words = list(spell.known(keywords))  # слова, которые есть в словаре
    check_bad_words(unknown_words)
    return unknown_words + known_words


def check_bad_words(unknown_words):
    for word in unknown_words:  # модуль для замены неправильного слова
        if word not in spell:
            cor = spell.candidates(word)
            choise_voc = {cor[0]: cor[1] for cor in enumerate(cor)}  # создаю словарь индекс - вариант правописания
            print(f"Выберите цифру правильного варианта написания {CRED}'{word}'{CEND} \n"
                  f"нажмите '/'  введите правильное слово вместо  {CRED}'{word}'{CEND} \n"
                  f"нажмите 'пробел' , если слово написано  правильно и хотите добавить слово {GREEN}'{word}'{CEND} в словарь \n ")

            correct_key = input()  # ключ правильного варианта написания

            if correct_key.isdigit():
                bad_word_index = unknown_words.index(word)  # индекс неправильного слова в списке ключевых слов
                unknown_words[bad_word_index] = choise_voc[
                    int(correct_key)]  # на это место вставляю правильное слово из словаря
            elif correct_key == ' ':
                spell.word_frequency.add(word)  # добавляю новое слово
                spell.export('my_custom_dictionary.gz', gzipped=True)  # сохраняю дополнительный словарь с новым словом
            elif correct_key == '/':
                spell.word_frequency.add(input())  # добавляю новое слово
                spell.export('my_custom_dictionary.gz', gzipped=True)  # сохраняю дополнительный словарь с новым словом
            else:
                print("please input digit")


keywords = ['высокотехнологичное', 'уутка', 'завод', 'слон', 'фотоархив']

print(correct_bad_words(keywords))
