import requests as r

def get_html_from_syosetsu(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    data = r.get(url, headers=headers)
    print(data)
    return data.text