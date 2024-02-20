# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/20 9:01
# @author  : Mo
# @function:


from tqdm import tqdm
import traceback
import time
import json
import sys
import os

path_sys = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path_sys)
# print(path_sys)

from text_char_similar.const_dict import load_json, save_json, txt_read, txt_write
from text_char_similar.char_similarity_multi import multi_cal_sim
from text_char_similar.char_similarity_pool import pool_cal_sim
from text_char_similar.char_similarity import cal_sim


def tet_v1():
    """   基础版   """
    ### 2w字一一对比
    dict_char_fourangle = load_json("data/char_fourangle.dict")
    list_chat_all_1 = list(dict_char_fourangle.keys())
    res_dict_128 = {}
    res_dict = {}
    kind = "all"  # "shape"  # "all"  # "shape" # "all"   "w2v"  "pinyin"
    list_chat_all_2 = list(dict_char_fourangle.keys())

    for k in tqdm(list_chat_all_1, desc="data"):
        v_score = []
        for v in list_chat_all_2:
            score = cal_sim(k, v, rounded=4, kind=kind)
            # score = cal_sim_by_shape(k, v)
            # score = cal_sim_by_pinyin(k, v)
            # score = cal_sim_by_w2v(k, v)
            # score = cal_sim_by_all(k, v)
            v_score.append((v, score))
        v_score_sorted = sorted(iter(v_score), key=lambda x:x[-1], reverse=True)
        # res_dict[k] = v_score_sorted[:128]
        res_dict_128[k] = "".join([v[0] for v in v_score_sorted][:128])
        res_dict[k] = v_score_sorted
    save_json(res_dict_128, f"c2c_{kind}_128.dict")
    save_json(res_dict, f"c2c_{kind}.dict")


def tet_v2():
    """   测试版, pool变慢-concurrent.futures.ThreadPoolExecutor   """
    ### 2w字一一对比
    dict_char_fourangle = load_json("data/char_fourangle.dict")
    list_chat_all_1 = list(dict_char_fourangle.keys())
    res_dict_128 = {}
    res_dict = {}
    kind = "shape"  # "shape"  # "all"  # "shape" # "all"   "w2v"  "pinyin"
    list_chat_all_2 = list(dict_char_fourangle.keys())
    time_start = time.time()
    number = 16
    for k in tqdm(list_chat_all_1[:number], desc="data"):
        v_score = []
        for v in list_chat_all_2:
            # score = cal_sim(k, v, rounded=4, kind=kind)
            score = pool_cal_sim(k, v, rounded=4, kind=kind)
            # score = multi_cal_sim(k, v, rounded=4, kind=kind)
            v_score.append((v, score))
    time_end = time.time()
    time_cost = time_end - time_start
    print(time_cost)
    """cal_sim
2.497999668121338
2.474030017852783
2.4980030059814453
2.499959945678711
"""


if __name__ == '__main__':
    myz = 0

    # tet_v1()

    tet_v2()


