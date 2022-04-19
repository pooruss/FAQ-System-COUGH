# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 9:54 2022

@author: pooruss
"""

import csv
import numpy as np

def build_index_query_dict(ars_file_path):
    index_query_dict = {}
    csv_reader = csv.reader(open(ars_file_path,mode='r',encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    Q_set = set()
    for row in csv_reader:
        Q_index, Q = row[0], row[1].replace('\n','')
        if Q not in Q_set:
            index_query_dict[Q_index] = Q
            Q_set.add(Q)
        else:
            index_query_dict[Q_index] = Q
    return index_query_dict

def build_Qq_dict(ars_file_path):
    ars_dict = {}
    csv_reader = csv.reader(open(ars_file_path,mode='r',encoding='utf-8'))
    csv.field_size_limit(1024 * 1024 * 1024)
    Q_set = set()
    for idx,row in enumerate(csv_reader):
        if idx == 0:
            continue
        Q_index, Q, faq_index, raw_score, score, label = row[0], row[1].replace('\n',''), row[2], row[3], float(row[4]), '1' if row[-1] == 'positive' else '0'
        # scheme A
        # label = ('1' if score >= 0.3 else '0' )
        # scheme C
        label = ('1' if '4' in raw_score or '3' in raw_score else '0' )
        if Q not in Q_set:
            ars_dict[Q_index] = {}
            ars_dict[Q_index][faq_index] = {}
            ars_dict[Q_index][faq_index]['query'] = Q
            ars_dict[Q_index][faq_index]['label'] = label
        else:
            ars_dict[Q_index][faq_index] = {}
            ars_dict[Q_index][faq_index]['query'] = Q
            ars_dict[Q_index][faq_index]['label'] = label
        Q_set.add(Q)
    return ars_dict


if __name__ == "__main__":
    cnt = 0
    index_query_dict = build_index_query_dict('../data/source/Annotated_Relevance_Set.csv')
    Qq_dict = build_Qq_dict('../data/source/Annotated_Relevance_Set.csv')
    evaluate_dict = {}
    for Q_index in index_query_dict:
        if Q_index in Qq_dict:
            for faq_index in Qq_dict[Q_index]:
                label = Qq_dict[Q_index][faq_index]['label']
                query = Qq_dict[Q_index][faq_index]['query']
                if label == '1':
                    if Q_index not in evaluate_dict:
                        evaluate_dict[Q_index] = {}
                        evaluate_dict[Q_index]['query'] = ''
                        evaluate_dict[Q_index]['faq_index'] = []
                    evaluate_dict[Q_index]['faq_index'].append(faq_index)
                    cnt += 1
                    evaluate_dict[Q_index]['query'] = query
    # np.save('../data/evaluate_set/evaluate_set_scheme_A_test.npy', evaluate_dict)
    print (cnt)
    # test
    # for faq_index in evaluate_dict['0']['faq_index']:
        # print (faq_index)

