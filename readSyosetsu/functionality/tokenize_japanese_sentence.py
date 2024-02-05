from janome.tokenizer import Tokenizer

def tokenize_japanese_sentence(sentence):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(sentence)
    words = [token.surface for token in tokens]
    
    return words

print(tokenize_japanese_sentence( 'それからは与えられた新事業の仕事をこなし旦那様を待ち続ける日々。そうして三年が経ち十七歳で結婚した私は現在二十歳になっていた。'))