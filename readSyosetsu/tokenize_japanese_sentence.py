from janome.tokenizer import Tokenizer

def tokenize_japanese_sentence(sentence):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(sentence)
    words = [token.surface for token in tokens]
    
    return words