#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import urllib3
import tldextract
import os
import wget
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

def download_image(url, path_to_save_image):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)

    with open(path_to_save_image, 'wb') as out:
        while True:
            data = r.read(15)
            if not data:
                break
            out.write(data)

    r.release_conn()


def extract_domain(link):
    ext = tldextract.extract(link)
    return ext.domain

def downlaod_and_move_image(path_to_image):
    files_in_image_folder = os.listdir('Images')
    file_name = wget.download(path_to_image)
    if file_name in files_in_image_folder:
        temp = file_name.split('.')
        temp[0] = temp[0] + '2'
        temp = clean_join_strings(temp)
        os.rename(file_name, temp)
        file_name = temp
        del temp
        destination = os.path.join('/home/diego/Documentos/rss_reader/Untitled Folder/Images', file_name)
        os.rename(file_name, destination)
    else:
        destination = os.path.join('/home/diego/Documentos/rss_reader/Untitled Folder/Images', file_name)
        os.rename(file_name, destination)
    return file_name

def get_noticia_uol(link):
    req = requests.get(link)
    bs = BeautifulSoup(req.text).find('div', id='texto').find_all('p')
    images = BeautifulSoup(req.text).find('div', id='texto').find_all('img')
    link_image = ""
    noticia = []
    if bs == []:
        link_image = 0
        pass
    else:

        ext = tldextract.extract(link)
        domain = ext.domain
        subdomain = ext.subdomain
        if images == []:
            noticia = bs
            link_image = 0
        else:
            i = 0
            for p in bs:
                if i >= 2:
                    text = p.contents[0]
                    if isinstance(text, str):
                        noticia.append(p.contents[0])
                i += 1
            src = images[0].get('src')
            link_image = src

    return join_strings(noticia), link_image

def join_strings(list_of_strings):

    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return "<p>".join(list_of_strings)


def clean_join_strings(list_of_strings):

    """
        Método para transformar tokens em uma única sentença
    :param list_of_strings: Lista com os tokens
    :return: sentença formada pela união dos tokens
    """
    return "".join(list_of_strings)

def get_noticia_comercio(link):
    req = requests.get(link)
    bs = BeautifulSoup(req.text).find('div', class_='noticia espacamento claro').find_all('div')
    noticia = ""
    for div in bs:
        noticia += str(div.contents[0].encode('utf-8'))
    return noticia