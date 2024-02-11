def clean_paragraph_text_list(paragraph_text_list):
    new_paragraph_text_list = []
    for paragraph_text in paragraph_text_list:
        paragraph_text = paragraph_text.replace('\u3000','')
        if paragraph_text:
            new_paragraph_text_list.append(paragraph_text)
    return new_paragraph_text_list