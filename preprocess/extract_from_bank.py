# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 26 9:54 2022

@author: pooruss
"""

import csv
import numpy as np


def build_faq_bank(target_language, bank_file):
    csv_reader = csv.reader(open('../data/source/FAQ_Bank.csv', mode='r', encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    bank_file = open('../data/faq_bank/' + bank_file, 'w', encoding='utf-8')
    for row in csv_reader:
        index, url, Q, answer, ori_language, type = row[0], row[1].replace('\n', ''), row[2], row[4], row[7], row[8]
        if target_language == ori_language:
            if ori_language == 'en':
                if type == 'Forum':
                    continue
                Q = ' '.join(Q.split())
                answer = ' '.join(answer.split())
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'zh':
                Q = Q.replace('\n', '')
                answer = answer.replace('\n', '')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'es':
                Q = Q.replace('\n', '')
                answer = answer.replace('\n', '')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'fr':
                Q = Q.replace('\n', '')
                answer = answer.replace('\n', '')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')


if __name__ == "__main__":
    language = sys.argv[1]
    bank_file = syys.argv[2]
    build_faq_bank(language, bank_file)
