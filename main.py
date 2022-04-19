# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:04 2022

@author: pooruss
"""
import sys
import json
import argparse
import numpy as np
from recall_module import RecallModule
from rerank_module import RerankModule
from google_translate import translated_content
from evaluation import EvaluateClass

parser = argparse.ArgumentParser()
parser.add_argument("--config", default='./config/en_recall_q_config.ini.txt', type=str, required=True, help="init")
parser.add_argument("--task", default='demo', type=str, required=True, help="demo or evaluation")
parser.add_argument("--rerank", default=False, type=bool, required=True, help="To do rerank or not")
args = parser.parse_args()

if __name__ == "__main__":
    # evaluation
    if args.task == "evaluation":
        rm = RecallModule(args.config, 'utf-8')
        rm.construct_postings_lists()
        db_dict = json.load(open(rm.db_file, 'r', encoding='utf-8'))
        rm.set_db_dict(db_dict)
        matrics_map = ["P@1", "P@5", "MAP", "MRR", "nDCG"]
        evaluate_dict = np.load(rm.evaluate_set, allow_pickle=True).item()
        if args.rerank:
            rm2 = RerankModule(rm.config)
            log_file = rm2.return_log_file()
        else:
            rm2 = None
            log_file = rm.return_log_file()

        evaluate = EvaluateClass(evaluate_dict, log_file, matrics_map)

        cost_time = evaluate.evaluation(rm, rm2, rerank)
        config = rm.config
        for key in config['DEFAULT']:
            if key == "avg_l":
                log_file.write(key + ":" + str(rm.AVG_L) + '\n')
                continue
            log_file.write(key + ":" + config['DEFAULT'][key] + '\n')

        log_file.write("Total time:" + str(cost_time) + '\n')

    # demo, return top5 answer's question from faq bank
    elif args.task == "demo":
        print('************* welcome to COVID-19 FAQ system **************')
        language = input('choose language( en, es, zh, fr ):')
        rm = RecallModule(args.config, 'utf-8')
        rm.construct_postings_lists()
        db_dict = json.load(open(rm.db_file, 'r', encoding='utf-8'))
        rm.set_db_dict(db_dict)
        query = ''
        while query != '0':
            from googletrans import Translator

            translator = Translator(service_urls=[
                'translate.google.cn'
            ])
            query = input('please input your query about COVID-19( input 0 to exit ):')
            query_response = translator.translate(query, dest='en')
            print('Input query:' + query_response.text)
            flag, BM25_scores = rm.result_by_BM25(query)
            if flag == 1:
                cnt = 0
                for qs in BM25_scores:
                    cnt += 1
                    if cnt > 5:
                        break
                    index, question, answer = qs[0].split('\t')
                    # print (question + '\t' + answer)
                    # text: str, dest='en', src='auto')
                    question_response = translator.translate(question, dest='en')
                    print("Retrieved question:" + question_response.text)
                print(len(BM25_scores))
            else:
                print("sorry, can not find appropriate answer from current database!")
