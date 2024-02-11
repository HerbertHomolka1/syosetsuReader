from bs4 import BeautifulSoup

def get_paragraph_text_list_from_html(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    # relevant text on syosetsu is inside <p id='L1' or L2 etc> tags
    paragraph_text_list = []
    l_tags_exist = True
    i = 1

    while l_tags_exist:
        tag_id = f"L{i}"
        p_tag = soup.find('p', id=tag_id)
        if p_tag:
            text = p_tag.get_text()
            paragraph_text_list.append(text)
            i+=1
        else:
            l_tags_exist = False
    return paragraph_text_list