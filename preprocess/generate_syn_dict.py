# -*- coding: utf-8 -*-
"""
Created on Wednesday Mar 28 18:04 2022

@author: pooruss
"""

import numpy as np

def build_syn_dict(syn_file_path):
    syn_dict = {}
    cnt = 0
    for line in open(syn_file_path, 'r', encoding='utf-8'):
        if '有问题' in line.strip():
            continue
        try:
            v = line.strip().split('\t')
            word, word_list= v[0], v[1].replace("\"", "").split(', ')
        except:
            cnt += 1
            continue

        syn_dict[word] = set()
        for syn_word in word_list:
            syn_dict[word].add(syn_word)

        for syn_word1 in word_list:
            syn_dict[syn_word1] = set()
            for syn_word2 in word_list:
                syn_dict[syn_word1].add(syn_word2)
    print (len(syn_dict))
    print (cnt)
    return syn_dict


if __name__ == "__main__":
    syn_dict = build_syn_dict('../data/syn/english_synonyms_and_antonyms.txt')
    np.save('../data/syn/syn_dict.npy', syn_dict)
