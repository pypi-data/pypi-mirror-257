# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/18 16:56
# @author  : Mo
# @function: char similarity


from tqdm import tqdm
import traceback
import json
import os

from text_char_similar.const_dict import dict_char_component, dict_char_fourangle
from text_char_similar.const_dict import dict_char_frequency, dict_char_number
from text_char_similar.const_dict import dict_char_pinyin, dict_char_stroke
from text_char_similar.const_dict import dict_char_struct, dict_char_order


def sim_fourangle(char1, char2, code=4):
    """ 计算两汉字相似度, 通过四角码(只计算前4位)
    calculate similarity of two chars, by judge wether is the same fourangle
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.5
    """
    char1_f4 = dict_char_fourangle.get(char1, "")
    char2_f4 = dict_char_fourangle.get(char2, "")
    result = 0
    if char1_f4 and char2_f4:
        same_count = sum(1 for cf1, cf2 in zip(char1_f4[:code],
                           char2_f4[:code]) if cf1 == cf2)
        result = same_count / code
    return result

def sim_pinyin(char1, char2, code=4):
    """ 计算两汉字相似度, 通过两个字拼音(拼音/声母/韵母/声调)
    calculate similarity of two chars, by char pinyin
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_pi = dict_char_pinyin.get(char1, [])
    char2_pi = dict_char_pinyin.get(char2, [])
    result = 0
    if char1_pi and char2_pi:
        same_count = sum(1 for cp1, cp2 in zip(char1_pi, char2_pi) if cp1 == cp2)
        result = same_count / code
    return result

def sim_component(char1, char2):
    """ 计算两汉字相似度, 通过偏旁部首
    calculate similarity of two chars, by judge wether is the same component
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: int, eg. 1 or 0
    """
    char1_component = dict_char_component.get(char1, "")
    char2_component = dict_char_component.get(char2, "")
    result = 0
    if char1_component and char1_component == char2_component:
        result = 1
    return result

def sim_frequency(char1, char2):
    """ 计算两汉字相似度, 通过两个字频log10的(1- 绝对值差/最大值)
    calculate similarity of two chars, by char frequency
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_fr = dict_char_frequency.get(char1, 0)
    char2_fr = dict_char_frequency.get(char2, 0)
    result = 0
    if char1_fr and char2_fr:
        result = 1 - abs((char1_fr - char2_fr) / max(char1_fr, char2_fr))
    return result

def sim_number(char1, char2):
    """ 计算两汉字相似度, 通过两个字笔画数的(1- 绝对值差/最大值)
    calculate similarity of two chars, by char number of stroke
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_nu = dict_char_number.get(char1, 0)
    char2_nu = dict_char_number.get(char2, 0)
    result = 0
    if char1_nu and char2_nu:
        result = 1 - abs((char1_nu - char2_nu) / max(char1_nu, char2_nu))
    return result

def sim_stroke(char1, char2):
    """ 计算两汉字相似度, 通过两个字拆字的(相同元素/所有元素)
    calculate similarity of two chars, by char count of stroke
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_st = dict_char_stroke.get(char1, [])
    char2_st = dict_char_stroke.get(char2, [])
    result = 0
    if char1_st and char2_st:
        count_and = len(set(char1_st) & set(char2_st))
        count_union = len(set(char1_st) | set(char2_st))
        result = count_and / count_union
    return result

def sim_struct(char1, char2):
    """ 计算两汉字相似度, 通过两个字构造结构
    calculate similarity of two chars, by char struct
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: int, 0 or 1, eg. 1
    """
    char1_st = dict_char_struct.get(char1, "")
    char2_st = dict_char_struct.get(char2, "")
    result = 0
    if char1_st and char2_st and char1_st == char2_st:
        result = 1
    return result

def sim_order(char1, char2):
    """ 计算两汉字相似度, 通过两个字笔顺(相同元素/所有元素)
    calculate similarity of two chars, by char struct
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    char1_or = dict_char_order.get(char1, "")
    char2_or = dict_char_order.get(char2, "")
    result = 0
    if char1_or and char2_or:
        count_and = len(set(list(char1_or)) & set(list(char2_or)))
        count_union = len(set(list(char1_or)) | set(list(char2_or)))
        result = count_and / count_union
    return result


def cal_sim_by_shape_v1(char1, char2, rounded=4, code=4,
    rate = (0.2, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2)):
    """ 计算两汉字相似度
    calculate similarity of two chars, by char shape
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 总得分*权重
    scores = [score_fourangle, score_component, score_frequency,
              score_number, score_stroke, score_struct, score_order]
    result = 0
    for idx, score in enumerate(scores):
        result += score * rate[idx]
    result = round(result, rounded)
    return result


def cal_sim_by_shape(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6,
    rate_stroke=4, rate_struct=8, rate_order=3):
    """ 计算两汉字相似度(字形)
    calculate similarity of two chars, by char shape
    rate(text-char-similar): 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 得分*权重
    result = score_fourangle * rate_fourangle + score_component * rate_component \
             + score_frequency * rate_frequency + score_number * rate_number \
             + score_stroke * rate_stroke + score_struct * rate_struct \
             + score_order * rate_order
    rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
               + rate_stroke + rate_struct + rate_order
    result = round(result/rate_all, rounded)
    return result




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

def calculate_char_similarity(rate=0.5):
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
            model_json_new[k] = v_score_sorted[:20]
            # if len(v_score_sorted) <= 5:
            #     v_score_sorted = [v[0] for v in v_score_sorted]
            # else:
            #     v_score_sorted = [v[0] for v in v_score_sorted if v[-1] > rate]
            # # model_json_new[k] = v_score_sorted[:5]
            #
            # if v_score_sorted:
            #     model_json_new[k] = v_score_sorted[:20]
            #     count += len(v_score_sorted[:20])
        save_json(model_json_new, "confusion_merge_all_fix_dict.sort_v2.json")
        print(len(model_json_new))
        print(count)
        """
        5520, 143005

        5520  80770
        
        5554  74339
        """


if __name__ == '__main__':
    calculate_char_similarity()
