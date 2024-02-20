# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/20 14:48
# @author  : Mo
# @function:


# import sys
# sys.path.append("D:/workspace/code_yxp/code_own/char-similar")

# ## 2.1 快速使用
# from char_similar import std_cal_sim
# char1 = "我"
# char2 = "他"
# res = std_cal_sim(char1, char2)
# print(res)
# # output:
# # 0.5821


# ## 2.2 详细使用
# from char_similar import std_cal_sim
# # "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
# kind = "all"
# rounded = 4  # 保留x位小数
# char1 = "我"
# char2 = "他"
# res = std_cal_sim(char1, char2, rounded=rounded, kind=kind)
# print(res)
# # output:
# # 0.5821


# ## 2.3 多线程使用
# from char_similar import pool_cal_sim
# # "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
# kind = "shape"
# rounded = 4  # 保留x位小数
# char1 = "我"
# char2 = "他"
# res = pool_cal_sim(char1, char2, rounded=rounded, kind=kind)
# print(res)
# # output:
# # 0.5821



# ## 2.4 多进程使用
# if __name__ == '__main__':
#     from char_similar import multi_cal_sim
#     # "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
#     kind = "shape"
#     rounded = 4  # 保留x位小数
#     char1 = "我"
#     char2 = "他"
#     res = multi_cal_sim(char1, char2, rounded=rounded, kind=kind)
#     print(res)
#     # output:
#     # 0.5821


