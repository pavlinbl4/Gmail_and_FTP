from deep_translator import GoogleTranslator

def trans_undescore(text):
    return GoogleTranslator(source='ru', target='en').translate(text).lower().replace(' ', '_')



text = " Я пытаюсь вставить целое число из списка чисел внутри команды в отдельный список команд"
print(trans_undescore(text))