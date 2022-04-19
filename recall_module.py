# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:04 2022

@author: pooruss
"""

import math
# import jieba
import configparser
import json
import datetime
import time

import numpy as np
from time import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# nltk.download('stopwords')
now_time = datetime.datetime.now()


class Question:
    faq_index = ''
    question = ''
    answer = ''
    tf = 0
    ld = 0

    def __init__(self, faq_index, question, answer, tf, ld):
        self.faq_index = faq_index
        self.question = question
        self.answer = answer
        self.tf = tf
        self.ld = ld

    def __repr__(self):
        return (self.faq_index + u'\t' + self.question + u'\t' +
                self.answer + u'\t' + str(self.tf) + u'\t' + str(self.ld))

    def __str__(self):
        return (self.faq_index + u'\t' + self.question + u'\t' +
                self.answer + u'\t' + str(self.tf) + u'\t' + str(self.ld))


class RecallModule:
    stop_words = set()
    postings_lists = {}
    config_path = ''
    config_encoding = ''

    def __init__(self, config_path, config_encoding):
        super(RecallModule, self).__init__()
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        self.config = config
        self.language = config['DEFAULT']['language']

        self.K1 = float(config['DEFAULT']['k1'])
        self.B = float(config['DEFAULT']['b'])
        self.AVG_L = float(config['DEFAULT']['avg_l'])

        self.data_path = config['DEFAULT']['data_dir_path']
        self.db_path = config['DEFAULT']['db_path']
        self.scheme = config['DEFAULT']['scheme']

        self.stop_words = set(stopwords.words(self.language))
        self.stop_words_method = config['DEFAULT']['stop_words_method']
        self.stop_words_path = config['DEFAULT']['stop_words_path']

        self.syn_dict_path = config['DEFAULT']['syn_dict_path']
        self.use_syn = config['DEFAULT']['use_syn']

        self.evaluate_set_path = config['DEFAULT']['evaluate_set_path']
        self.es_method = config['DEFAULT']['es_method']
        self.recall_method = config['DEFAULT']['recall_method']

        if self.scheme == 'A':
            self.evaluate_set = self.evaluate_set_path + 'evaluate_set_scheme_A.npy'
        elif self.scheme == 'B':
            self.evaluate_set = self.evaluate_set_path + 'evaluate_set_scheme_B.npy'
        else:
            self.evaluate_set = self.evaluate_set_path + 'evaluate_set_scheme_C.npy'

        if self.stop_words_method != 'nltk':
            self.stop_words = set()
            for line in open(self.stop_words_path + "en_{}.txt".format(self.stop_words_method), 'r', encoding='utf-8'):
                self.stop_words.add(line.strip())

        if self.use_syn == 'True':
            self.syn_dict = np.load(self.syn_dict_path + 'syn_dict.npy', allow_pickle=True).item()
        else:
            self.syn_dict = dict()
        self.total_syn_cost_time = 0.0

        self.db_file = self.db_path + '_' + self.stop_words_method + '_' + self.es_method + '.json'
        self.db_dict = None

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict

    def write_postings_to_db(self):
        db_dict = {}
        for key, value in self.postings_lists.items():
            db_dict[key] = {}
            db_dict[key]['df'] = str(value[0])
            db_dict[key]['q_list'] = '|||'.join(map(str, value[1]))
        json_str = json.dumps(db_dict)  # ensure_ascii=False)
        db_file = open(self.db_file, 'w', encoding='utf-8')
        # print json_str
        db_file.write(json_str)

    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)
        data_file = open(self.data_path, 'r', encoding='utf-8')
        AVG_L, qid, qnum = 0, 0, 0
        last_qid = '-1'
        for idx, line in enumerate(data_file):
            # if idx > 100:
            #     break
            u = line.strip().split('\t')
            try:
                faq_index, question, reply = u[0], u[1], u[2]
                if faq_index != last_qid:
                    qnum += 1
                last_qid = faq_index
            except:
                print('data bank error!' + '\t' + line.strip())
                continue
            if self.es_method == 'q':
                doc = question
            elif self.es_method == 'qa':
                doc = question + '. ' + reply
            else:
                doc = reply
            seg_list = word_tokenize(doc.lower(), language=self.language)
            ld, cleaned_dict = self.clean_list(seg_list)
            AVG_L = AVG_L + ld
            for key, value in cleaned_dict.items():
                q = Question(faq_index, question, reply, value, ld)
                if key in self.postings_lists:
                    self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                    self.postings_lists[key][1].append(q)
                else:
                    self.postings_lists[key] = [1, [q]]  # [df, [question]]
        AVG_L = float(AVG_L) / float(qnum)
        config.set('DEFAULT', 'N', str(qnum))
        config.set('DEFAULT', 'avg_l', str(AVG_L))
        self.N = qnum
        self.AVG_L = AVG_L
        with open(self.config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        self.write_postings_to_db()

    def read_from_db(self, key_word):
        if key_word in self.db_dict:
            return float(self.db_dict[key_word]['df']), self.db_dict[key_word]['q_list'].split('|||')
        elif self.use_syn == 'True':  # 同义词典
            start_time = time()
            syn_word_list = []
            if key_word in self.syn_dict:
                for syn_word in self.syn_dict[key_word]:
                    syn_word_list.append(syn_word)
            for syn_key_word in syn_word_list:
                if syn_key_word in self.db_dict:
                    cost_time = time() - start_time
                    self.total_syn_cost_time += float(cost_time)
                    self.log_file.write("syn solved! But cost more time:" + str(float(self.total_syn_cost_time)) + '\n')
                    print("syn solved! But cost more time:" + str(float(self.total_syn_cost_time)))
                    return float(self.db_dict[syn_key_word]['df']), self.db_dict[syn_key_word]['q_list'].split('|||')
            return None, None
        else:
            return None, None

    def result_by_BM25(self, sentence):
        seg_list = word_tokenize(sentence.lower(), language=self.language)
        n, cleaned_dict = self.clean_list(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            df, q_list = self.read_from_db(term)
            # print df, q_list
            if df is None:
                # print ("Query word not in db!")
                continue
            try:
                if self.recall_method == 'BM25':
                    w = math.log((self.N - df + 0.5) / (df + 0.5), 2)
                    g = 0.0
                elif self.recall_method == 'BM25L' or self.recall_method == 'BM25+':
                    w = math.log((self.N + 1) / (df + 0.5), 2)
                    g = 0.5
            except:
                continue
            for q in q_list:
                # print q
                try:
                    faq_index, question, answer, tf, ld = q.split(u'\t')
                except:
                    continue
                tf = float(tf)
                ld = float(ld)
                BBLDL = (1 - self.B + self.B * ld / self.AVG_L)
                if self.recall_method != 'BM25+':
                    s = ((self.K1 + 1) * (tf + g * BBLDL) * w) / (tf + self.K1 * BBLDL + g * BBLDL)
                else:
                    s = w * (((self.K1 + 1) * tf / (self.K1 * BBLDL + tf)) + g)
                if (faq_index + '\t' + question + '\t' + answer) in BM25_scores:
                    BM25_scores[faq_index + '\t' + question + '\t' + answer] = BM25_scores[
                                                                                   faq_index + '\t' + question + '\t' + answer] + s
                else:
                    BM25_scores[faq_index + '\t' + question + '\t' + answer] = s
        BM25_scores = sorted(BM25_scores.items(), key=lambda item: item[1])
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, {}
        else:
            return 1, BM25_scores

    def set_db_dict(self, db_dict):
        self.db_dict = db_dict

    def return_log_file(self):
        log_file = open('./run_log/{}_Q-{}_scheme{}_{}_syn{}_{}.log'.format(
            self.recall_method, self.es_method, self.scheme,
            self.stop_words_method, self.use_syn, str(now_time)[:10]),
            'w', encoding='utf-8')
        return log_file
