# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 26 9:54 2022

@author: pooruss
"""

import csv
import numpy as np

def build_faq_bank(target_language):
    csv_reader = csv.reader(open('../data/source/FAQ_Bank.csv',mode='r',encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    bank_file = open('../data/faq_bank/'+target_language+'_qa_bank.txt', 'w', encoding='utf-8')
    # en_bank = open('./es_qa_bank.txt', 'w', encoding='utf-8')
    # zh_bank_q = open('./fr_qa_bank_q.txt', 'w', encoding='utf-8')
    for row in csv_reader:
        index, url, Q, answer, ori_language, type = row[0], row[1].replace('\n',''), row[2], row[4], row[7], row[8]
        if target_language == ori_language:
            if ori_language == 'en':
                if type == 'Forum':
                    continue
                Q = ' '.join(Q.split())
                answer = ' '.join(answer.split())
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'zh':
                Q = Q.replace('\n','')
                answer = answer.replace('\n','')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'es':
                Q = Q.replace('\n','')
                answer = answer.replace('\n','')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')
            elif ori_language == 'fr':
                Q = Q.replace('\n','')
                answer = answer.replace('\n','')
                res = [index, Q, answer]
                bank_file.write('\t'.join(res) + '\n')

if __name__ == "__main__":
    build_faq_bank('es')