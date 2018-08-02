#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import base64
import datetime
from time import gmtime, strftime
import string
import numpy as np
import copy

USER = 'admpolitica'
PASSWORD = 'xarx@2018'

URL = 'https://politica.xarx.rocks/wp-json/wp/v2'
# url_media = 'https://politica.xarx.rocks/wp-json/wp/v2/media'
# url_pernambuco = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'

token = base64.standard_b64encode(USER + ':' + PASSWORD)
headers = {'Authorization': 'Basic ' + token}

# categoria sem_categoria : 1
# categoria geral : 97
INDEX_CATEGORIES = {
    'ac': 271,
    'al': 261,
    'ap': 272,
    'am': 273,
    'ba': 262,
    'ce': 263,
    'df': 250,
    'es': 257,
    'go': 251,
    'ma': 264,
    'mt': 252,
    'ms': 253,
    'mg': 258,
    'pa': 274,
    'pb': 265,
    'pr': 254,
    'pe': 266,
    'pi': 267,
    'rj': 259,
    'rn': 268,
    'rs': 255,
    'ro': 275,
    'rr': 276,
    'sc': 256,
    'sp': 260,
    'se': 269,
    'to': 270,

    'avante': 214,
    'dc': 215,
    'dem': 216,
    'mdb': 217,
    'novo': 218,
    'psl': 239,
    'patri': 219,
    'pcb': 248,
    'pcdob': 220,
    'pco': 221,
    'pdt': 222,
    'phs': 223,
    'pmb': 224,
    'pmn': 225,
    'pode': 226,
    'pp': 227,
    'ppl': 228,
    'pps': 229,
    'prep': 230,
    'prb': 231,
    'pros': 232,
    'prp': 233,
    'prtb': 234,
    'psb': 235,
    'psc': 236,
    'psd': 237,
    'psdb': 238,
    'psol': 240,
    'pstu': 241,
    'pt': 242,
    'ptb': 243,
    'ptc': 244,
    'pv': 245,
    'rede': 246,
    'sd': 247
}


def remove_punctuation(input_text):
    """
    Removes the punctuation from the input_text string
    python 2 (string.maketrans) is different from python 3 (str.maketrans)

    Parameters
    ----------
    input_text: string in which the punctuation will be removed

    Return
    ------
        input_text without the puncutation
    """
    # Make translation table
    # if not isinstance(input_text, str):
    #    input_text = str(input_text)
    punct = string.punctuation
    # if python 2
    trantab = string.maketrans(punct, len(punct) * ' ')  # Every punctuation symbol will be replaced by a space
    #     # if python 3
    #     trantab = str.maketrans(punct, len(punct) * ' ')  # Every punctuation symbol will be replaced by a space
    return input_text.translate(trantab)


def join_strings(list_of_strings):
    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return ", ".join(list_of_strings)


def get_categories_idx(categories_names):
    """
    Get the wordpress categories index from the list of strings

    Parameters
    ----------
    categories_names: list of strings containing the name of the categories

    Return:
    ------
        categories_idx: list of integers containing the index of the categories
    """
    #     categories_noticias = df['categorias'].values.tolist()
    list_categories = list(categories_names)
    categories_idx = []
    for category in list_categories:
        category = remove_punctuation(category)
        if category in INDEX_CATEGORIES.keys():
            categories_idx.append(INDEX_CATEGORIES[category])
    return categories_idx


def get_categories_all_noticias(df):
    """
    Get the list of categories (list of categories (str)) for all 'noticias'

    Parameters
    ----------
    df : dataframe containing all the data

    Return:
    ------
        list_categorias: list of list of categories for all 'noticias'
    """
    categories_noticias = df['categorias']
    list_categories = []
    for categories_noticia in categories_noticias:
        list_categories.append(remove_punctuation(categories_noticia).split())
    return list_categories


def get_categorias_noticia(df, idx_noticia):
    """
    Get the categories (list of categories (str)) for 'noticia' at idx_noticia index

    Parameters
    ----------
    df : dataframe containing all the data

    Return:
    ------
        list_categorias: lista de categorias para a noticia no indice idx_noticia
    """
    categories_noticias = df['categorias']
    list_categories = remove_punctuation(categories_noticias[idx_noticia]).split()
    return list_categories


def get_reduced_news(news_text):
    """
    Get the reduced text (content) of the news in the in the POST format

    Parameters
    ----------
    news_text : initial text of the news (in the current format is the abstract text)

    Return:
    ------
        reduced_news: reduced text (content) of the news in the in the POST format
    """
    # get paragraph_tag
    paragraph_tag = '\n'
    tag_idxs = []
    for i, _ in enumerate(news_text):
        if news_text[i:i + len(paragraph_tag)] == paragraph_tag:
            tag_idxs.append(i)

    img_tag = 'img'
    foto_tag = 'foto'
    globo_tag = 'globo'
    # No caso das noticias do globo
    try:
        # No caso de as noticias nao virem com imagens
        if (img_tag not in news_text[:tag_idxs[0]]):
            reduced_size = len(news_text) / 5
            reduced_news = news_text[:reduced_size]
        else:
            verification_text = news_text[:tag_idxs[5]]
            if ((globo_tag in verification_text.lower()) or (foto_tag in verification_text.lower())):
                for i in xrange(5, 0, -1):
                    temp = news_text[tag_idxs[i - 1]:tag_idxs[i]]
                    if ((globo_tag in temp.lower()) or (foto_tag in temp.lower())):
                        paragraph_idx = i
                        break

                # paragrafo vazio
                if (abs(tag_idxs[paragraph_idx + 1] - tag_idxs[paragraph_idx]) < 10):
                    paragraph_idx += 1
                main_content = news_text[tag_idxs[paragraph_idx]:]
                reduced_size = len(main_content) / 5
                reduced_news = main_content[:reduced_size]
    # No caso das noticias do jornal do comercio, que tem um abstract diferente do texto em si
    except:
        reduced_news = news_text

    # Remover '\n' duplicado
    # ver isso no linux: se no lugar do \r\n vai ser so \n (https://stackoverflow.com/questions/14606799/what-does-r-do-in-the-following-script)
    # reduced_news = reduced_news.replace('\n\n\t \n\n', '<p>')
    # reduced_news = reduced_news.replace('\n', '<p>')

    return reduced_news


def post_news(df):
    # columns = image, links, noticia, titulos, categorias, estacoes
    #     df = pd.read_csv('../Data/news/resultados-categorias-tag.csv')
    use_image = True

    for idx in range(len(df)):
        #     for idx in range(0, 5):
        row = df.iloc[idx]

        #         print(row['titulos'])
        #         print(row['categorias'])
        #         print(row['abstract'])
        #         print(row['image'])

        #         # date now
        #         date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # title for the post
        title = row['titulos'].encode('utf-8')
        # the wordpress categories index for the 'noticia' at idx_noticia index
        categories_names = row['categorias']
        categories = get_categories_idx(categories_names)
        cats = join_strings(np.array(categories).astype(str).tolist())
        #             # the text of the 'noticia' and the link of the 'noticia'
        #             content = df['noticia'][idx] + '\n\nFonte: ' + '<a href=' + df['links'][idx] +'> ' + df['links'][idx] + '</a>'

        #             news = df['noticia']
        news = row['abstract'].encode('utf-8')
        reduced_news = get_reduced_news(news)
        temp = '... ' + '<a href=' + row['links'] + '> ' + 'Leia a reportagem completa' + '</a>'
        complemento = temp.encode('utf-8', 'ignore')
        content = reduced_news + complemento

        # if the 'noticia' does not have category
        if (categories == []):
            cats = '97'  # category Geral

        # url for the choosen station
        url = URL
        #             url_pernambuco = 'https://politica.xarx.rocks/pe/wp-json/wp/v2'

        #             payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; \
        #             name=\"title\"\r\n\r\n{0}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        #             form-data; name=\"categories\"\r\n\r\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        #             form-data; name=\"content\"\r\n\r\n{2}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        #             form-data; name=\"status\"\r\n\r\npublish\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(title,
        #                                                                                                           cats,
        #                                                                                                           content).encode("utf-8")

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; \
        name=\"title\"\r\n\r\n{0}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        form-data; name=\"categories\"\r\n\r\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        form-data; name=\"content\"\r\n\r\n{2}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: \
        form-data; name=\"status\"\r\n\r\npublish\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(title,
                                                                                                       cats,
                                                                                                       content)

        headers_postman = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'authorization': "Basic YWRtcG9saXRpY2E6eGFyeEAyMDE4",
            'cache-control': "no-cache",
            'postman-token': "660515d7-2398-f142-2660-69ff2d5ef344"
        }

        #         response = requests.request("POST", url, data=payload, headers=headers)
        #         print(response.text)

        r = requests.post(url + '/posts', headers=headers_postman, data=payload)
        print('POST = ' + str(r))

        if (use_image):
            try:
                image_path = 'Images/' + row['image'].encode('utf-8')
                media = {'file': open(image_path, 'rb'), 'caption': 'picture'}
                image = requests.post(url + '/media', headers=headers, files=media)
                print('IMAGE_POST = ' + str(image))

                img_id = requests.get(url + '/media').json()[0]['id']
                post_id = requests.get(url + '/posts').json()[0]['id']
                print(img_id)
                print(post_id)

                imgid = (json.loads(image.content))['id']
                postid = (json.loads(r.content))['id']
                print(imgid)
                print(postid)
                updated_post = {'featured_media': img_id}

                update = requests.post(url + '/posts/' + str(post_id), headers=headers, json=updated_post)
                print('UPDATE_POST = ' + str(update))
            except:
                print('Image not found.')