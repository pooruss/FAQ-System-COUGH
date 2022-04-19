## FAQ System based on COUGH

#### Background

- 数据集来源： ["COUGH: A Challenge Dataset and Models for COVID-19 FAQ Retrieval"](https://arxiv.org/abs/2010.12800).

|                        | [FAQIR](http://takelab.fer.hr/data/faqir/) | [StackFAQ](http://takelab.fer.hr/data/StackFAQ/) | [LocalGov](http://nlp.ist.i.kyoto-u.ac.jp/EN/index.php?BERT-Based_FAQ_Retrieval) | [Sun and Sedoc](https://openreview.net/pdf?id=dGOeF3y_Weh) | [Poliak et al.](https://openreview.net/pdf?id=0X9O6VcYe_) | **COUGH** (ours) |
| :--------------------: | :----------------------------------------: | :----------------------------------------------: | :----------------------------------------------------------: | :--------------------------------------------------------: | :-------------------------------------------------------: | :--------------: |
|         Domain         |                   Yahoo!                   |                  StackExachange                  |                          Government                          |                          COVID-19                          |                         COVID-19                          |     COVID-19     |
|       # of FAQs        |                    4313                    |                       719                        |                             1786                             |                            690                             |                           2115                            |      15919       |
|    # of Queries (Q)    |                    1233                    |                       1249                       |                             784                              |                           6495*                            |                          24240*                           |       1201       |
| # of annotations per Q |                    8.22                    |                  Not Applicable                  |                             <10                              |                             5                              |                             5                             |      32.17       |
|      Query Length      |                    7.30                    |                      13.84                       |                              **                              |                             **                             |                            **                             |      12.97       |
|    FAQ-query Length    |                   12.30                    |                      10.39                       |                              **                              |                             **                             |                            **                             |      13.00       |
|   FAQ-answer Length    |                   33.00                    |                      76.54                       |                              **                              |                             **                             |                            **                             |      113.58      |
|        Language        |                  English                   |                     English                      |                           Japanese                           |                          English                           |                       Multi-lingual                       |  Multi-lingual   |
|      # of sources      |                     1                      |                        1                         |                              1                               |                             12                             |                            34                             |        55        |



------

#### Requirements:

python 3.7

- nltk==3.7
- numpy==1.19.3
- paddlepaddle-gpu==2.2.2.post111
- rocketqa==1.0.0

#### Recall and Rerank

- 召回模块支持：BM25、BM25L、BM25+

- 精排模块支持：Rocketqa-v1-marco-de、Rocketqa-v1-marco-ce ...



------

#### Data preprocess

- 根据不同scheme(A or C)，抽取评估集；共1200+条query

  ```shell
  cd preprocess
  python extract_evaluate_set.py A
  # 结果保存为npy文件，位于../data/evaluate_set/evaluate_set_scheme_A_test.npy
  ```

- 抽取不同语种的问答库，英文部分共9000+条（question，answer）items

  ```shell
  cd preprocess
  python extract_from_bank.py en en_bank
  # 结果保存为txt文件，位于../data/faq_bank/en_bank.txt
  ```



------

#### Demo

```shell
python main.py \
--config ./config/en_q_config.ini \
--task demo \
--rerank False
```

#### Evaluation

```shell
python main.py \
--config ./config/en_q_config.ini \
--task evaluation \
--rerank False
```



------

#### Todo

1. 更好地结合召回模块和精排模块的能力
2. 多语言功能完善
3. 前端页面