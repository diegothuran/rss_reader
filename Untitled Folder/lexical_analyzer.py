#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import string
import numpy as np

# ESTADOS = ['acre ', 'alagoas', 'amapá', 'amazonas', 'bahia', 'ceará', 'distrito federal',  'espírito santo',  'goiás',
#            'maranhão', 'mato grosso',  'mato grosso do sul',  'minas gerais',  'pará',  'paraíba',  'paraná',  'pernambuco',
#            'piauí',  'rio de janeiro', 'rio grande do norte', 'rio grande do sul', 'rondônia', 'roraima', 'santa catarina',
#            'são paulo', 'sergipe', 'tocantins']

ESTADOS = ['alagoas', 'amapá', 'amazonas', 'bahia', 'ceará', 'distrito federal', 'espírito santo', 'goiás',
           'maranhão', 'mato grosso', 'mato grosso do sul', 'minas gerais', 'paraíba', 'paraná', 'pernambuco',
           'piauí', 'rio de janeiro', 'rio grande do norte', 'rio grande do sul', 'rondônia', 'roraima',
           'santa catarina',
           'são paulo', 'sergipe', 'tocantins']

ESTADO_PARA = 'Pará'

ESTADO_ACRE = 'Acre'

# CAPITAIS = ['rio branco', 'maceió', 'macapá', 'manaus', 'salvador', 'fortaleza', 'brasília', 'vitória', 'goiânia', 'são luís',
#             'cuiabá', 'campo grande', 'belo horizonte', 'belém', 'joão pessoa', 'curitiba', 'recife', 'teresina', 'rio de janeiro',
#             'natal', 'porto alegre', 'porto velho', 'boa vista', 'florianópolis', 'são paulo', 'aracaju', 'palmas']

CAPITAIS = ['rio branco', 'maceió', 'macapá', 'manaus', 'brasília', 'goiânia', 'são luís',
            'cuiabá', 'campo grande', 'belo horizonte', 'belém', 'joão pessoa', 'curitiba', 'recife', 'teresina',
            'rio de janeiro',
            'porto alegre', 'porto velho', 'boa vista', 'florianópolis', 'são paulo', 'aracaju']

# CAPITAIS = ['rio branco', 'maceió', 'macapá', 'manaus', 'salvador', 'fortaleza', 'brasília', 'vitória', 'goiânia', 'são luís',
#             'cuiabá', 'campo grande', 'belo horizonte', 'belém', 'joão pessoa', 'curitiba', 'recife', 'teresina', 'rio de janeiro',
#             'porto alegre', 'porto velho', 'boa vista', 'florianópolis', 'são paulo', 'aracaju', 'palmas']

# CAPITAL_NATAL = 'Natal'
# CAPITAL_SALVADOR = 'Salvador'
# CAPITAL_FORTALEZA = 'Fortaleza'
# CAPITAL_VITORIA = 'Vitória'
# CAPITAL_PALMAS =  'Palmas'

CAPITAIS_CASE_SENSITIVE = ['Natal', 'Salvador', 'Fortaleza', 'Vitória', 'Palmas']

SIGLAS_ESTADOS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR',
                  'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

SIGLAS_ESTADOS_SEM_PA_AC = ['AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PB', 'PR',
                            'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# SIGLAS_ESTADOS_SEM_RN = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA','PB', 'PR',
#                   'PE', 'PI', 'RJ', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE','TO']

SIGLAS_ESTADOS_SEM_CASE_SENSITIVE = ['AC', 'AL', 'AP', 'AM', 'DF', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR',
                                     'PE', 'PI', 'RJ', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE']

SIGLAS_ESTADOS_CASE_SENSITIVE = ['RN', 'BA', 'CE', 'ES', 'TO']

PARTIDOS = ['democracia cristã', 'democratas', 'movimento democrático brasileiro',
            'partido social liberal', 'partido comunista brasileiro', 'partido comunista do brasil',
            'partido da causa operária', 'partido democrático trabalhista', 'partido humanista da solidariedade',
            'partido da mulher brasileira', 'partido da mobilização nacional', 'partido progressista',
            'partido pátria livre', 'partido popular socialista', 'partido da república',
            'partido republicano brasileiro',
            'partido republicano da ordem social', 'partido republicano progressista',
            'partido renovador trabalhista brasileiro',
            'partido socialista brasileiro', 'partido social cristão', 'partido social democrático',
            'partido da social democracia brasileira', 'partido socialismo e liberdade',
            'partido socialista dos trabalhadores unificado', 'partido dos trabalhadores',
            'partido trabalhista brasileiro',
            'partido trabalhista cristão', 'partido verde', 'rede sustentabilidade', 'solidariedade']

# prep is the PARTIDO DA REPUBLICA (PR) -> conflict with PR from PARANA
SIGLAS_PARTIDOS = ['dc', 'dem', 'mdb', 'psl', 'pcb', 'pcdob', 'pco', 'pdt', 'phs', 'pmb',
                   'pmn', 'pp', 'ppl', 'pps', 'prep', 'prb', 'pros', 'prp', 'prtb', 'psb', 'psc', 'psd', 'psdb',
                   'psol', 'pstu', 'pt', 'ptb', 'ptc', 'pv', 'rede', 'sd']

PARTIDOS_CASE_SENSITIVE = ['Avante', 'Partido Novo', 'Podemos', 'Patriota']

SIGLAS_PARTIDOS_CASE_SENSITIVE = ['AVANTE', 'NOVO', 'PODE', 'PATRI']


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
    # if not isinstance(input_text, str):
    #    input_text = str(input_text)
    # Make translation table
    punct = string.punctuation
    # if python 2
    trantab = string.maketrans(punct, len(punct) * ' ')  # Every punctuation symbol will be replaced by a space
    #     # if python 3
    #     trantab = str.maketrans(punct, len(punct)*' ')  # Every punctuation symbol will be replaced by a space
    return input_text.translate(trantab)


def set_stations_and_categories(df):
    """
    Set the categories for the noticias.
    Adds the 'categorias' column to the dataframe

    Parameters
    ----------
    df : dataframe containing all the data

    Return
    ------
        Dataframe with the new 'categorias' column added
        set_cats: list of set of categories (now all is category)
    """
    noticias = df['noticia'].values.tolist()
    cats = []
    for idx_noticia in range(len(noticias)):
        states_by_text, cats_by_text = [], []
        # Removing punctuation
        try:
            text = remove_punctuation(noticias[idx_noticia])

            # CASE_SENSITIVE VERIFICATION
            # Seek for SIGLAS_ESTADOS sigla
            words = text.split()
            for word in words:
                if word in SIGLAS_ESTADOS:
                    states_by_text.append(word.lower())

            #             # Natal, caso a parte, para evitar o erro de 'indulto natalino'
            #             if CAPITAL_NATAL in text:
            #                 states_by_text.append('rn')
            #
            #             if CAPITAL_SALVADOR in text:
            #                 states_by_text.append('ba')
            #
            #             if CAPITAL_FORTALEZA in text:
            #                 states_by_text.append('ce')
            #
            #             if CAPITAL_VITORIA in text:
            #                 states_by_text.append('es')
            #
            #             if CAPITAL_PALMAS in text:
            #                 states_by_text.append('to')

            for idx_capitais in range(len(CAPITAIS_CASE_SENSITIVE)):
                if CAPITAIS_CASE_SENSITIVE[idx_capitais] in text:
                    cats_by_text.append(SIGLAS_ESTADOS_CASE_SENSITIVE[idx_capitais].lower())

            # Pará, caso a parte, para evitar o erro de verbo no futuro 'parará'
            if ESTADO_PARA in text:
                states_by_text.append('pa')

            # Acre, caso a parte, para evitar o erro de verbo acreditar
            if ESTADO_ACRE in text:
                states_by_text.append('ac')

            # Seek for PARTIDOS_CASE_SENSITIVE name
            for idx_partidos in range(len(PARTIDOS_CASE_SENSITIVE)):
                if PARTIDOS_CASE_SENSITIVE[idx_partidos] in text:
                    cats_by_text.append(SIGLAS_PARTIDOS_CASE_SENSITIVE[idx_partidos].lower())

            # Seek for SIGLAS_PARTIDOS_CASE_SENSITIVE sigla
            words = text.split()
            for word in words:
                if word in SIGLAS_PARTIDOS_CASE_SENSITIVE:
                    cats_by_text.append(word.lower())

            # LOWER_CASE VERIFICATION: text to lower case
            text = text.lower()

            # seek for ESTADOS name
            for idx_estado in range(len(ESTADOS)):
                if ESTADOS[idx_estado] in text:
                    states_by_text.append(SIGLAS_ESTADOS_SEM_PA_AC[idx_estado].lower())

            # seek for CAPITAIS name
            for idx_capitais in range(len(CAPITAIS)):
                if CAPITAIS[idx_capitais] in text:
                    states_by_text.append(SIGLAS_ESTADOS_SEM_CASE_SENSITIVE[idx_capitais].lower())

            # Seek for PARTIDOS name
            for idx_partidos in range(len(PARTIDOS)):
                if PARTIDOS[idx_partidos] in text:
                    cats_by_text.append(SIGLAS_PARTIDOS[idx_partidos])

            # Seek for PARTIDOS sigla
            words = text.split()
            for word in words:
                if word in SIGLAS_PARTIDOS:
                    cats_by_text.append(word)
            # correcting the acronym for party PR
            cats_by_text = ['pr' if x == 'prep' else x for x in cats_by_text]
            cats_concat = cats_by_text + states_by_text
            cats.append(cats_concat)
        except:
            cats.append([])
    # Removing replicated items
    set_cats = [set(cat) for cat in cats]

    df = df.assign(categorias=set_cats)
    return df, set_cats


def lexical(df):
    #     # columns = Unnamed: 0, Unnamed: 0.1, imagem, links, noticia, titulos, categorias
    #     df = pd.read_csv('../Data/news/resultados-uol2.csv', index_col=False)
    #     df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'imagem'], axis=1)
    #     df, set_cats = set_stations_and_categories(df)
    #     # columns = image, links, noticia, titulos, categorias
    #     df.to_csv('../Data/news/resultados-categorias-tag.csv', encoding='utf-8')

    # columns = ['Unnamed: 0', 'titulos', 'links', 'noticia', 'image', 'abstract'])
    #     df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'imagem'], axis=1)
    df, set_cats = set_stations_and_categories(df)
    # columns = image, links, noticia, titulos, categorias
    df.to_csv('results.csv', encoding='utf-8')

    name_file = 'categorias-tag.txt'
    print('Writing table file')
    f = open(name_file, 'w')
    for idx_cats in range(len(set_cats)):
        f.write('\n' + str(idx_cats) + ' - categorias: ' + str(set_cats[idx_cats]))
    f.close()
    print('End file')
    return df

#     # Testing
#     noticias = df['noticia']
#     print(noticias[27])

#     df = pd.read_csv('../Data/resultados-categorias-tag.csv', index_col=0)
#     news = df['noticia']
#     estacoes = df['estacoes']
#     categorias = df['categorias']
#     print(news[4])
#     print(estacoes[4])
#     print(categorias[4])