# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/18 16:56
# @author  : Mo
# @function:



from collections import OrderedDict, Counter, defaultdict
from difflib import SequenceMatcher
import logging as logger
import traceback
import random
import math
import copy
import json
import re
import os
import gc

from pypinyin import pinyin, lazy_pinyin, Style
from tqdm import tqdm
import pandas as pd
import pypinyin


def is_chinese_char(uchar):
    """判断一个unicode是否是汉字"""
    return '\u4e00' <= uchar <= '\u9fa5'


def is_chinese_string(string):
    """判断是否全为汉字"""
    return all(is_chinese_char(c) for c in string)


def is_number(uchar):
    """判断一个unicode是否是数字"""
    return '\u0030' <= uchar <= '\u0039'


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    return '\u0041' <= uchar <= '\u005a' or '\u0061' <= uchar <= '\u007a'


def is_alphabet_string(string):
    """判断是否全部为英文字母"""
    return all(is_alphabet(c) for c in string)


def is_alphabet_number_string(string):
    """判断全是数字和英文字符"""
    return all((is_alphabet(c) or is_number(c)) for c in string)


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    return not (is_chinese_char(uchar) or is_number(uchar) or is_alphabet(uchar))


def B2Q(uchar):
    """半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()


def get_homophones_by_char(input_char):
    """
    根据汉字取同音字
    :param input_char:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.NORMAL)[0][0] == pinyin(input_char, style=pypinyin.NORMAL)[0][0]:
            result.append(chr(i))
    return result
def get_heterotony_by_char(input_char):
    """
    根据汉字取同音字
    :param input_char:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == pinyin(input_char, style=pypinyin.TONE2)[0][0]:
            result.append(chr(i))
    return result
def get_homophones_by_pinyin(input_pinyin):
    """
    根据拼音取同音字
    :param input_pinyin:
    :return:
    """
    result = []
    # CJK统一汉字区的范围是0x4E00-0x9FA5,也就是我们经常提到的20902个汉字
    for i in range(0x4e00, 0x9fa6):
        if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == input_pinyin:
            # TONE2: 中zho1ng
            result.append(chr(i))
    return result


def txt_write(lines, path, mode="w", encode_type="utf-8"):
    """
        txt【list】写入文件
    Args:
        lines[List]: input data to write, eg. ["桂林山水甲天下\\n"]
        path[String]: path of file of read, eg. "corpus/xuexiqiangguo.txt"
        mode[String]: write mode of file, eg. "w", "a+", "wb"
        encode_type[String]: data encode type of file, eg. "utf-8", "gbk"
    Returns:
        lines[List]: output lines
    """
    try:
        file = open(path, mode, encoding=encode_type)
        file.writelines(lines)
        file.close()
    except Exception as e:
        logger.info(str(e))
def txt_read(path, encode_type="utf-8", errors=None):
    """
        读取txt文件，默认utf8格式, 不能有空行
    Args:
        path[String]: path of file of read, eg. "corpus/xuexiqiangguo.txt"
        encode_type[String]: data encode type of file, eg. "utf-8", "gbk"
        errors[String]: specifies how encoding errors handled, eg. "ignore", strict
    Returns:
        lines[List]: output lines
    """
    lines = []
    try:
        file = open(path, "r", encoding=encode_type, errors=errors)
        lines = file.readlines()
        file.close()
    except Exception as e:
        logger.info(str(e))
    finally:
        return lines
def save_xlsx(path_json, path_xlsx="nkpmath.xlsx"):
    """   json转化为xlsx的excel文件   """
    kg_list = load_json(path_json)
    res_xlsx = {}
    for kg_i in kg_list:
        for jdx, kg_i_j in enumerate(kg_i):
            jdx_str = str(jdx)
            if jdx_str in res_xlsx:
                res_xlsx[jdx_str].append(kg_i_j)
            else:
                res_xlsx[jdx_str] = [kg_i_j]
    pdr = pd.DataFrame(res_xlsx)
    with pd.ExcelWriter(path_xlsx, engine="xlsxwriter",
            options={"strings_to_urls": False}) as writer:
        pdr.to_excel(writer)
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
def get_all_dirs_files(path_dir):
    """
        递归获取某个目录下的所有文件(所有层, 包括子目录)
    Args:
        path_dir[String]:, path of dir, eg. "/home/data"
    Returns:
        data[List]: data of input, eg. ["2020_01_08.txt"]
    """
    path_files = []
    for root, dirs, files in os.walk(path_dir):  # 分别代表根目录、文件夹、文件
        for file in files:  # 遍历文件
            file_path = os.path.join(root, file)  # 获取文件绝对路径
            path_files.append(file_path)  # 将文件路径添加进列表
    files = list(set(path_files))
    files.sort()
    return files
def find_diff_pos(sent1, sent2):
    """
    判断两个病句的不同之处, 返回insert/delete/replace, difflib-SequenceMatcher
    args:
        sent1: str, sentence of org, eg. "春天来了，越来越来暖和了。"
        sent2: str, sentence of fix, eg. "春天来了，天气越来越暖和了。"
    return:
        diff_pos_s: List<Tuple>, tag and position, eg. ""
    """
    matcher = SequenceMatcher(None, sent1, sent2)
    diff_pos_s = []
    for tag, idx_1, idx_2, jdx_1, jdx_2 in matcher.get_opcodes():
        if tag != "equal":
            line_tuple = [tag, sent1[idx_1:idx_2],
                          sent2[jdx_1: jdx_2], [idx_1, idx_2]]
            diff_pos_s.append(line_tuple)
    return diff_pos_s
def cut_sentence(text):
    """  分句(文本摘要)  """
    # re_sen = re.compile('[:;!?。：；？！\n\r]') #.不加是因为不确定.是小数还是英文句号(中文省略号......)
    # re_sen = re.compile('[!?。？！\n\r]')
    # re_sen = re.compile('[,，"“”、<>《》{}【】:;!?。：；？！\n\r]') #.不加是因为不确定.是小数还是英文句号(中文省略号......)
    re_sen = re.compile('[!?。？！\n\r…]')
    sentences = re_sen.split(text)
    return sentences


pun_1 = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟 〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'
pun_2 = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
puns = pun_1 + pun_2
def delete_last_punctuation(text):
    """   -删除句末的标点符号-   """
    while len(text) > 0 and text[-1] in puns:
        text = text[:-1]
    return text


def tet_char_fourangle():
    """   获取四角编码   """
    data_pianpangbushou_2w = txt_read("data/sijiaobianma_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char_components_dict[char1] = char2
            ee = 0
        else:
            print(d)
    save_json(char_components_dict, "char_fourangle.dict")


def tet_char_component():
    """   获取偏旁部首   """
    data_pianpangbushou_2w = txt_read("data/pianpangbushou_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char_components_dict[char1] = char2
            ee = 0
        else:
            print(d)
    save_json(char_components_dict, "char_component.dict")


def tet_char_struct():
    """   获取偏旁部首   """
    data_pianpangbushou_2w = txt_read("data/hanzijiegou_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char_components_dict[char1] = char2
            ee = 0
        else:
            print(d)
    save_json(char_components_dict, "char_struct.dict")


def tet_char_pinyin():
    """   获取偏旁部首   """
    # for i in range(0x4e00, 0x9fa6):
    #     if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == pinyin(input_char, style=pypinyin.TONE2)[0][0]:
    #         result.append(chr(i))

    data_pianpangbushou_2w = txt_read("data/pianpangbushou_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char1_pinyin = lazy_pinyin(char1)
            char_components_dict[char1] = char1_pinyin[0]
            ee = 0
        else:
            print(d)
    save_json(char_components_dict, "char_pinyin.dict")
def tet_char_pinyin_v2():
    """   获取拼音, 声母, 韵母, 声调   """
    # for i in range(0x4e00, 0x9fa6):
    #     if pinyin([chr(i)], style=pypinyin.TONE2)[0][0] == pinyin(input_char, style=pypinyin.TONE2)[0][0]:
    #         result.append(chr(i))

    data_pianpangbushou_2w = txt_read("data/pianpangbushou_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char1_pinyin = lazy_pinyin(char1)
            char1_first_letter = pinyin(char1, style=Style.FIRST_LETTER)
            char1_tone = pinyin(char1, style=Style.TONE3)
            v1 = char1_pinyin[0]
            v2 = char1_first_letter[0][0]
            if "zh" in v1 or "ch" in v1 or "sh" in v1:
                v2 = v1[:2]
            v3 = v1[len(v2):]
            v4 = char1_tone[0][0][-1]
            char_components_dict[char1] = [v1, v2, v3, v4]
            ee = 0
        else:
            print(d)
    save_json(char_components_dict, "char_pinyin_v2.dict")



def tet_char_stroke():
    """   获取偏旁部首   """
    """   获取偏旁部首   """
    chaizi_jt = txt_read("data/chaizi-jt.txt")
    chaizi_jt_add = txt_read("data/chaizi-jt_add.txt")
    data_chaizi = chaizi_jt + chaizi_jt_add
    char_components_dict = {}
    for d in data_chaizi:
        d_sp = d.strip().split("\t")
        if len(d_sp) >= 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char2_sp = char2.split(" ")
            if char1 == "□":
                continue
            char_components_dict[char1] = char2_sp
            ee = 0
        else:
            print(d)
    print(len(char_components_dict))
    save_json(char_components_dict, "char_stroke.dict")


def tet_char_freq():
    """   获取字频, log10   """
    data_pianpangbushou_2w = txt_read("data/sijiaobianma_2w.txt")
    char_components_dict = {}
    for d in data_pianpangbushou_2w:
        d_sp = d.strip().split(" ")
        if len(d_sp) == 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char_components_dict[char1] = char2
            ee = 0
        else:
            print(d)
    macropodus_list = load_json("data/macropodus.dict")[0]
    macropodus_dict = {}
    for k, v in macropodus_list.items():
        if len(k) == 1:
            macropodus_dict[k] = v
    char_freq = {}
    count = 0
    for k, v in char_components_dict.items():
        if k in macropodus_dict:
            # char_freq[k] = macropodus_dict.get(k)
            kk = macropodus_dict.get(k)
            kk_log = math.log2(kk)
            char_freq[k] = round(kk_log, 2)
        else:
            count += 1
            char_freq[k] = 1
    save_json(char_freq, "char_freq.dict")
    print(count)
    """ 14669   """


def tet_char_count():
    """   获取笔画数,   """
    chaizi_jt = txt_read("data/bihuashu_2w.txt")
    char_components_dict = {}
    for d in chaizi_jt:
        d_sp = d.strip().split(" ")
        if len(d_sp) >= 2:
            char1 = d_sp[0]
            char2 = d_sp[1]
            char_components_dict[char1] = int(char2)
            ee = 0
        else:
            print(d)
    print(len(char_components_dict))
    save_json(char_components_dict, "char_number.dict")

def tet_char_order():
    """   获取笔顺   """
    chaizi_jt = txt_read("data/CJK.txt")
    char_components_dict = {}
    for d in chaizi_jt[1:]:
        d_sp = d.strip().split(",")
        if len(d_sp) == 7:
            char1 = d_sp[1].replace("鿶", "")
            char2 = d_sp[-2]
            if "鿱" != char1 and char2 and char1:
                char_components_dict[char1] = char2
                ee = 0
        else:
            print(d)
    print(len(char_components_dict))
    save_json(char_components_dict, "char_order.dict")


if __name__ == '__main__':
    ee = 0
    # tet_char_fourangle()
    # tet_char_component()
    # tet_char_struct()
    # tet_char_pinyin()
    # tet_char_stroke()
    # tet_char_freq()
    # tet_char_count()
    # tet_char_pinyin_v2()
    tet_char_order()

