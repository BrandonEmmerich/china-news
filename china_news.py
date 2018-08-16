# -*- coding: utf-8 -*-

import requests
import pandas as pd

empty_list = []

for i in range(1,10):
    print i
    url = 'https://www.yicai.com/api/ajax/getjuhelist?action=news&page={}&pagesize=100'.format(i)
    res = requests.get(url)
    df = pd.DataFrame(res.json())
    df_clean = df[['CreateDate','url','NewsTitle','NewsNotes']]

    empty_list.append(df_clean)

df = pd.concat(empty_list)

def _find_keyword(input_string):
    """A helper function to find occurances of keywords"""
    input_string = input_string.encode('utf-8')

    keyword = '违约'

    if keyword in input_string:
        status = True

    else:
        status = False

    return status

df_match = df[df['NewsNotes'].map(_find_keyword) |df['NewsTitle'].map(_find_keyword) ]

import ipdb; ipdb.set_trace()
