# pip install deep-translator
from deep_translator import GoogleTranslator

def translate_english(keywords):  # принимает список с ключевыми словами
    return GoogleTranslator(source='en', target='ru').translate_batch(keywords)