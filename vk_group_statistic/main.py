# -*- encoding: utf-8 -*-
__author__ = 'pahaz'

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

import requests as req
import random as rand
from collections import Counter
from bs4 import BeautifulSoup as Parser
import pymorphy as pm

morph_ru = pm.get_morph("ru.sqlite-json")
morph_en = pm.get_morph("en.sqlite-json")
word_counter = Counter()
people_count_list = []


def return_nf(word):
    """ Word normal form """
    try:
        word = word.upper()

        info = morph_ru.get_graminfo(word)
        if info:
            word = info[0]['norm']
        else:
            info = morph_en.get_graminfo(word)
            if info:
                word = info[0]['norm']

        return word
    except:
        return word


# def seporate_by(lst, by):
#     """ [1, 2, 3, 4] by 2 -> [[1, 2], [3, 4]]
#     """
#     if len(lst) % by != 0:
#         raise TypeError("Invalid list length")
#     len_sublist = len(lst) / by
#     return [lst[x:x + len_sublist] for x in range(0, len(lst), len_sublist)]


def parse_vk_club(id):
    """
    Return None if group access error
    """
    rez = req.get("http://vk.com/club{0}".format(id),
                  headers={'Accept-Language': 'en-us,en;q=0.5'})
    parser = Parser(rez.content)

    # get count users
    try:
        selector = parser.select('#group_followers .module_header .p_header_bottom')
        count_str = selector[0].stripped_strings.next().split(" ", 1)[0]
        count = int(count_str)
    except:
        count = 0

    # get words
    try:
        selector = parser.select('#group_wide .page_top')
        page_top = ' '.join(list(selector[0].stripped_strings))
        words = re.split(u'[^a-zA-ZА-Яа-яЁё]+', page_top)
        words = filter(lambda x: len(x) > 3, words)
        words = map(lambda x: x.upper(), words)
        words = map(return_nf, words)
    except:
        return None

    return (words, count)


if __name__ == "__main__":
    COUNT = int(sys.argv[1]) if len(sys.argv) == 2 else 10000
    print("COUNT GROUPS : " + str(COUNT))

    i = 0
    while i < COUNT:
        print('==' + str(i))
        x = rand.randrange(1000, 50000000)
        print("https://vk.com/club{0}".format(x))
        rez = parse_vk_club(x)
        if rez:
            i += 1
            words, count_user_in_group = rez
            word_counter.update(words)
            people_count_list.append(count_user_in_group)
            lst = word_counter.most_common()#sorted([(v, k) for k, v in word_counter.iteritems()], lambda x, y: y[0] - x[0])
            print(u', '.join([u"{0:d} - {1:s}".format(x[0], x[1]) for x in lst]))
        else:
            print('Invalid Group')

    print("\n === FINALL === \n")
    people_count_list.sort()

    #data1 = map(max, seporate_by(people_count_list, 10))
    interval = len(people_count_list) / 10
    data1 = [lst[x+interval-1] for x in range(0, len(lst), interval)]

    for z in range(len(data1)):
        print("In {0}% -- count of people < {1}".format(10 * (z+1), x[x]))

    print("Words stats top-100 : ")
    lst = sorted([(v, k) for k, v in word_counter.iteritems()], lambda x, y: y[0] - x[0])
    print(u'\n'.join([u"{1:s} -- {0:d} times ".format(x[0], x[1]) for x in lst][:100]))

    locs = np.arange(10)
    width = 0.88
    plt.bar(locs, data1, width=width)
    labels = [str(10) + "%" for x in range(10)]
    plt.xticks(locs + width / 2., labels)
    plt.show()
