# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 9:54 2022

@author: pooruss
"""

import json
import numpy as np
from tqdm import tqdm

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

zhidao_qa = open('../data/zhidao_qa_bank.txt', 'w', encoding='utf-8')

with open('../data/zhidao_qa.json', 'r', encoding='utf-8') as json_file:
    for idx,line in tqdm(enumerate(json_file)):
        body_str = json.loads(line.strip())
        q = body_str['question']
        answers = body_str['answers']
        for a in answers:
            zhidao_qa.write(str(idx) + q + '\t' + a + '\n')
            # print(q + '\t' + a)

# train_set, test_set = split_train_test(data, 0.2)