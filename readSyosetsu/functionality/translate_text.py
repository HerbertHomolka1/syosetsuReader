from deep_translator import GoogleTranslator

def translate_text(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)

