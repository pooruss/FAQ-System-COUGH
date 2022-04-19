# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:04 2022

@author: pooruss
"""
import math
from time import *


class EvaluateClass:

    def __init__(self, evaluate_dict, log_file, matrics_map):
        self.evaluate_dict = evaluate_dict
        self.matrics_map = matrics_map
        self.total_p1 = 0.0
        self.total_p5 = 0.0
        self.total_map = 0.0
        self.total_mrr = 0.0
        self.total_ndcg = 0.0
        self.P1 = 0.0
        self.P5 = 0.0
        self.map = 0.0
        self.map_cnt = 0.0
        self.mrr = 0.0
        self.dcg = 0.0
        self.idcg = 0.0
        self.MAP = 0.0
        self.MRR =0.0
        self.nDCG = 0.0

        self.log_file = log_file

    def zero(self):
        self.P1, self.P5, self.map, self.map_cnt, self.mrr, self.dcg = \
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    def evaluation(self, recall_module, rerank_module, rerank):

        def IDCG(n):
            idcg = 0
            for i in range(n):
                idcg += 1 / math.log(i + 2, 2)
            return idcg

        start_time = time()
        for Q_cnt, Q_index in enumerate(self.evaluate_dict):
            Q_cnt += 1
            gt_length = len(self.evaluate_dict[Q_index]['faq_index'])
            query = self.evaluate_dict[Q_index]['query']

            if rerank:
                index_list, rerank_list = [], []
                recall_score_dict = dict()
                index_to_qa = dict()

            flag, BM25_scores = recall_module.result_by_BM25(query)

            if flag == 1:
                recall_res_cnt = 0.0
                self.zero()
                self.idcg = IDCG(gt_length)

                total_score = 0.0
                for idx, qs in enumerate(BM25_scores):
                    total_score += float(qs[1])

                for idx, qs in enumerate(BM25_scores):
                    if idx >= 50: # fetch top 50 only
                        break
                    faq_index, question, answer = qs[0].split('\t')

                    if not rerank:
                        faq_index = qs[0].split('\t')[0]
                        recall_res_cnt += 1
                        self.compute_indicators(faq_index, recall_res_cnt, Q_index, idx)
                        continue
                    else: # prepare for rerank
                        index_to_qa[faq_index] = question + '\t' + answer
                        index_list.append(faq_index)
                        rerank_list.append(question + '.' + answer)
                        score = (float(qs[1])/float(total_score))*(100-idx)
                        # score = float(qs[1])
                        recall_score_dict[faq_index] = score

                if rerank: # rerank

                    RANK_DICT = rerank_module.reranking(index_list, recall_score_dict, query, rerank_list)

                    for idx, index_score in enumerate(RANK_DICT):
                        faq_index, rank_score = index_score[0], index_score[1]
                        recall_res_cnt += 1
                        self.compute_indicators(faq_index, recall_res_cnt, Q_index, idx)

                self.total_indicators(Q_cnt, gt_length)
                self.logger(Q_cnt)
        cost_time = time() - start_time
        return cost_time

    def compute_indicators(self, faq_index, recall_res_cnt, Q_index, idx):
        if faq_index in self.evaluate_dict[Q_index]['faq_index']:
            # P@1
            if idx == 0 and "P@1" in self.matrics_map:
                self.P1 += (1 if faq_index in self.evaluate_dict[Q_index]['faq_index'] else 0)
            # P@5
            if "P@5" in self.matrics_map:
                if recall_res_cnt <= 5:
                    self.P5 += 1
            # MAP
            if "MAP" in self.matrics_map:
                self.map_cnt += 1
                self.map += (self.map_cnt / recall_res_cnt)
            # MRR
            if "MRR" in self.matrics_map and self.mrr == 0.0:
                rank = float(idx + 1)
                self.mrr += (1 / rank)
            # nDCG
            if "nDCG" in self.matrics_map:
                rank = float(idx + 1)
                self.dcg += 1 / math.log(rank + 1, 2)

    def total_indicators(self, Q_cnt, gt_length):
        # P@1
        self.total_p1 += self.P1
        self.P1 = self.total_p1 / Q_cnt
        # P@5
        self.total_p5 += self.P5
        self.P5 = self.total_p5 / (5 * Q_cnt)
        # MAP
        self.total_map += (self.map / gt_length)
        self.MAP = self.total_map / Q_cnt
        # MRR
        self.total_mrr += self.mrr
        self.MRR = self.total_mrr / Q_cnt
        # nDCG
        self.total_ndcg += (self.dcg / self.idcg if self.idcg != 0 else 0)
        self.nDCG = self.total_ndcg / Q_cnt

    def logger(self, Q_cnt):
        self.log_file.write('########### evaluate {} ##########'.format(Q_cnt) + '\n')
        self.log_file.write('当前P@1：' + str(self.P1) + '\n')
        self.log_file.write(
            '当前P@5：' + str(self.P5) + '\n')
        self.log_file.write('当前MAP：' + str(self.MAP) + '\n')
        self.log_file.write('当前MRR：' + str(self.MRR) + '\n')
        self.log_file.write('当前nDCG：' + str(self.nDCG) + '\n')
        print('########### evaluate {} ##########'.format(str(Q_cnt)))
        print('当前P@1：' + str(self.P1))
        print('当前P@5：' + str(self.P5))
        print('当前MAP：' + str(self.MAP))
        print('当前MRR：' + str(self.MRR))
        print('当前nDCG：' + str(self.nDCG))
