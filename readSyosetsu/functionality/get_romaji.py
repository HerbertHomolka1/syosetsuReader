import pykakasi

def get_romaji(text):
    kks = pykakasi.kakasi()
    romaji_text = kks.convert(text)
    romaji_text = [word['hira'] for word in romaji_text]
    romaji_text = ''.join(romaji_text)
    return romaji_text