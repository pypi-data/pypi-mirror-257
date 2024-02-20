# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/18 16:56
# @author  : Mo
# @function:


from tqdm import tqdm
import traceback
import json
import os

from text_char_similar.const_dict import dict_char_component, dict_char_fourangle
from text_char_similar.const_dict import dict_char_frequency, dict_char_number
from text_char_similar.const_dict import dict_char_pinyin, dict_char_stroke
from text_char_similar.const_dict import dict_char_struct


def cal_sim_by_shape_v1(char1, char2, rounded=4):
    """   计算字形相似度   """
    # 获取四码和汉字笔画数
    structure1 = dict_char_struct.get(char1, None)
    structure2 = dict_char_struct.get(char2, None)
    stroke1 = dict_char_number.get(char1, None)
    stroke2 = dict_char_number.get(char2, None)
    code1 = dict_char_fourangle.get(char1, None)
    code2 = dict_char_fourangle.get(char2, None)

    # 定义结构相似度
    if structure1 and structure2 and structure1 == structure2:
        score_structure = 1
    else:
        score_structure = 0

    # 定义四码相似度
    score_code = 0
    if code1 and code2:
        # 四码分为四位计算，若相同则指数+1，不同为0,总权数除以4再加权
        for idx in range(4):
            if code1[idx] == code2[idx]:
                score_code += 1
        score_code /= 4

    # 笔画数利用相对偏差的方式进行计算
    score_stroke = 0
    if stroke1 and stroke2:
        stroke1 = int(stroke1)
        stroke2 = int(stroke2)
        score_stroke = 1 - abs((stroke1 - stroke2) / max(stroke1, stroke2))
    # 四码权重、笔画权重和结构权重分别为为 0.4 0.3 0.3
    score_shape = score_code * 0.4 + score_stroke * 0.3 + score_structure * 0.3
    score_shape = round(score_shape, rounded)
    return score_shape

def cal_sim_by_shape_v1(char1, char2, rounded=4):
    """   计算字形相似度   """
    # 获取四码和汉字笔画数
    structure1 = dict_char_struct.get(char1, None)
    structure2 = dict_char_struct.get(char2, None)
    stroke1 = dict_char_number.get(char1, None)
    stroke2 = dict_char_number.get(char2, None)
    code1 = dict_char_fourangle.get(char1, None)
    code2 = dict_char_fourangle.get(char2, None)

    # 定义结构相似度
    if structure1 and structure2 and structure1 == structure2:
        score_structure = 1
    else:
        score_structure = 0

    # 定义四码相似度
    score_code = 0
    if code1 and code2:
        # 四码分为四位计算，若相同则指数+1，不同为0,总权数除以4再加权
        for idx in range(4):
            if code1[idx] == code2[idx]:
                score_code += 1
        score_code /= 4

    # 笔画数利用相对偏差的方式进行计算
    score_stroke = 0
    if stroke1 and stroke2:
        stroke1 = int(stroke1)
        stroke2 = int(stroke2)
        score_stroke = 1 - abs((stroke1 - stroke2) / max(stroke1, stroke2))
    # 四码权重、笔画权重和结构权重分别为为 0.4 0.3 0.3
    score_shape = score_code * 0.4 + score_stroke * 0.3 + score_structure * 0.3
    score_shape = round(score_shape, rounded)
    return score_shape





def save_json(jsons, json_path, indent=4):
    """
        保存json
    Args:
        path[String]:, path of file of save, eg. "corpus/xuexiqiangguo.lib"
        jsons[Json]: json of input data, eg. [{"桂林": 132}]
        indent[int]: pretty-printed with that indent level, eg. 4
    Returns:
        None
    """
    with open(json_path, "w", encoding="utf-8") as fj:
        fj.write(json.dumps(jsons, ensure_ascii=False, indent=indent))
    fj.close()
def load_json(path, parse_int=None):
    """
        加载json
    Args:
        path_file[String]:, path of file of save, eg. "corpus/xuexiqiangguo.lib"
        parse_int[Boolean]: equivalent to int(num_str), eg. True or False
    Returns:
        data[Any]
    """
    with open(path, mode="r", encoding="utf-8") as fj:
        model_json = json.load(fj, parse_int=parse_int)
    return model_json

def calculate_char_similarity():
    """   计算 单字 相似度   """
    path_confusion = "D:/workspace/code_yxp/code_own/text-composition/sample_v2_2023/confusion_merge_all_fix_dict.json"
    with open(path_confusion, mode="r", encoding="utf-8") as fj:
        model_json = json.load(fj)
        model_json_new = {}
        count = 0
        for k, v in tqdm(model_json.items(), desc="data"):
            v_score = []
            for vi in v:
                try:
                    score_sim = cal_sim_by_shape(k, vi)
                except Exception as e:
                    print(traceback.print_exc())
                    print(k, vi)
                    score_sim = 0
                if k != vi:
                    v_score.append((vi, score_sim))
            v_score_sorted = sorted(iter(v_score), key=lambda x: x[-1], reverse=True)
            # model_json_new[k] = v_score_sorted[:5]
            if len(v_score_sorted) <= 5:
                v_score_sorted = [v[0] for v in v_score_sorted]
            else:
                v_score_sorted = [v[0] for v in v_score_sorted if v[-1] > 0.6]
            # model_json_new[k] = v_score_sorted[:5]

            if v_score_sorted:
                model_json_new[k] = v_score_sorted[:20]
                count += len(v_score_sorted[:20])
        save_json(model_json_new, "confusion_merge_all_fix_dict.sort_v2.json")
        print(len(model_json_new))
        print(count)
        """
        5520, 143005

        5520  80770
        """


if __name__ == '__main__':
    calculate_char_similarity()
