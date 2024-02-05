from get_html_from_syosetsu import get_html_from_syosetsu
from get_paragraph_text_list_from_html import get_paragraph_text_list_from_html
from clean_paragraph_text_list import clean_paragraph_text_list

def get_syosetsu_paragraph_list_from_url(url):
    html_code = get_html_from_syosetsu(url)
    paragraph_text_list = get_paragraph_text_list_from_html(html_code)
    cleaned_paragraph_text_list = clean_paragraph_text_list(paragraph_text_list)
    return cleaned_paragraph_text_list