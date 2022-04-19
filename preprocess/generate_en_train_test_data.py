# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 26 9:54 2022

@author: pooruss
"""

import csv
import numpy as np

def build_Qil_dict(ars_file_path):
    Qil_dict = {}
    csv_reader = csv.reader(open(ars_file_path,mode='r',encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    Q_set = set()
    for row in csv_reader:
        Q_index, Q, faq_index, label = row[0], row[1].replace('\n',''), row[2], '1' if row[-1] == 'positive' else '0'
        average = row[4]
        if average < 3:

        if Q not in Q_set:
            Qil_dict[Q] = {}
            Qil_dict[Q][faq_index] = label
            Q_set.add(Q)
        else:
            Qil_dict[Q][faq_index] = label
    return Qil_dict

def build_faq_dict(faq_file_path):
    faq_dict = {}
    csv_reader = csv.reader(open(faq_file_path,mode='r',encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    for row in csv_reader:
        faq_index, q = row[0], row[2].replace('\n','')
        faq_dict[faq_index] = q
    return faq_dict

def split_train_test(data, test_ratio):
    train_data, test_data = [], []
    # 设置随机数种子，保证每次生成的结果都是一样的
    np.random.seed(42)
    # permutation随机生成0-len(data)随机序列
    shuffled_indices = np.random.permutation(len(data))
    # test_ratio为测试集所占的半分比
    test_set_size = int(len(data)) * test_ratio
    test_indices = shuffled_indices[:int(test_set_size)]
    train_indices = shuffled_indices[int(test_set_size):]
    for train_indice in train_indices:
        train_data.append(data[train_indice])
    for test_indice in test_indices:
        test_data.append(data[test_indice])
    return train_data, test_data


if __name__ == "__main__":
    Qil_dict = build_Qil_dict('../data/source/Annotated_Relevance_Set.csv')
    faq_dict = build_faq_dict('../data/source/FAQ_Bank.csv')
    # es_train_data = open('es_all_labeled_data.txt','w', encoding='utf-8')
    data = []
    for Q in Qil_dict:
        for faq_index in faq_dict:
            if faq_index in Qil_dict[Q]:
                for label in Qil_dict[Q][faq_index]:
                    res = [Q, faq_dict[faq_index], label]
                    data.append(res)
                # es_train_data.write('\t'.join(res)+'\n')

    # 测试
    train_set, test_set = split_train_test(data, 0.2)
    print(len(train_set), "train +", len(test_set), "test")

    es_train_data = open('../data/finetune/en_ernie_Qq_train_data.txt','w', encoding='utf-8')
    for item in train_set:
        print (item)
        es_train_data.write('\t'.join(item)+'\n')
        print (item)
    es_test_data = open('../data/finetune/en_ernie_Qq_test_data.txt','w', encoding='utf-8')
    for item in test_set:
        es_test_data.write('\t'.join(item)+'\n')
