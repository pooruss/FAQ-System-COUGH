# -*- coding: utf-8 -*-
"""
Created on Wednesday Jan 19 18:04 2022

@author: pooruss
"""
import datetime
import rocketqa

from time import *

now_time = datetime.datetime.now()


class RerankModule:

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.rank_method = config['DEFAULT']['rerank_method']
        self.rank_method2 = config['DEFAULT']['rerank_method2']
        self.dual_encoder = rocketqa.load_model(model=self.rank_method,
                                                use_cuda=True, device_id=0, batch_size=25)
        # self.dual_encoder2 = rocketqa.load_model(model=self.rank_method2,
        #                                         use_cuda=True, device_id=0, batch_size=25)
        self.score_method = config['DEFAULT']['score_method']
        self.score_method2 = config['DEFAULT']['score_method2']
        self.scheme = config['DEFAULT']['scheme']
        self.stop_words_method = config['DEFAULT']['stop_words_method']
        self.use_syn = config['DEFAULT']['use_syn']
        self.es_method = config['DEFAULT']['es_method']
        self.recall_method = config['DEFAULT']['recall_method']
        self.rerank_method = config['DEFAULT']['rerank_method']

    def reranking(self, index_list, recall_score_dict, query, rerank_list):
        # reranking
        RANK_DICT = dict()

        start_time = time()
        dot_products = self.dual_encoder.matching(query=[query] * len(rerank_list), para=rerank_list)
        # dot_products2 = self.dual_encoder2.matching(query=[query] * len(rerank_list), para=rerank_list)
        total_score, total_score2 = 0.0, 0.0
        for idx, score in enumerate(dot_products):
            total_score += float(score)
        # for idx, score2 in enumerate(dot_products2):
        #     total_score2 += float(score2)
        # dot_products += dot_products2
        for (idx,qid), rank_score in zip(enumerate(index_list), dot_products):
            # 归一化
            rank_score = (rank_score / total_score) * (50 - idx)
            # rank_score2 = (rank_score2 / total_score2) * (50 - idx)
            if self.score_method == 'split_sum':
                if idx < 5:
                    rank_score *= recall_score_dict[qid]
                # elif idx < 10:
                #     rank_score *= recall_score_dict[qid]
                else:
                    rank_score *= ((float(idx) / float(idx + 1)) * recall_score_dict[qid])
                rank_score += recall_score_dict[qid]
            elif self.score_method == 'sum_10':
                rank_score *= 10
                rank_score += recall_score_dict[qid]
            # elif self.score_method == 'sum':
            #     rank_score += recall_score_dict[qid]
            # elif self.score_method == 'multi':
            #     rank_score *= recall_score_dict[qid]
            # elif self.score_method == 'recall':
            #     rank_score = recall_score_dict[qid]
            # elif self.score_method == 'rank':
            #     rank_score = rank_score
            # if self.score_method2 == 'split_sum':
            #     if idx < 5:
            #         rank_score2 *= recall_score_dict[qid]
            #     else:
            #         rank_score2 *= ((float(idx) / float(idx + 1)) * recall_score_dict[qid])
            # else:
            #     rank_score2 = rank_score2
            # rank_score = rank_score + rank_score2 + recall_score_dict[qid]
            RANK_DICT[qid] = float(rank_score)

        RANK_DICT = sorted(RANK_DICT.items(), key=lambda item: item[1])
        RANK_DICT.reverse()
        print("rerank time consume:" + str(time() - start_time))

        return RANK_DICT

    def return_config(self):
        return self.config

    def return_log_file(self):
        log_file = open('./run_log/{}_Q-{}_scheme{}_{}_{}_{}_{}.log'.format(
            self.recall_method, self.es_method, self.scheme,
            self.stop_words_method, self.rerank_method, self.score_method, str(now_time)[:10]),
            'w', encoding='utf-8')
        return log_file
