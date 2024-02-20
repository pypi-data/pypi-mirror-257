# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/2/20 11:55
# @author  : Mo
# @function:


# You can define addi in the global scope before executing calc function:


import multiprocessing as mp
import os


def addi(num1, num2):
    print(num1 + num2)

def calc(num1, num2):

    m = mp.Process(target=addi, args=(num1, num2))
    m.start()
    print("here is main", os.getpid())
    m.join()


if __name__ == "__main__":
    # creating processes
    calc(5, 6)




import multiprocess as mp  # Note that we are importing "multiprocess", no "ing"!
import os

def calc(num1, num2):

    def addi(num1, num2):
        print(num1 + num2)

    m = mp.Process(target=addi, args=(num1, num2))
    m.start()

    print("here is main", os.getpid())
    m.join()


if __name__ == "__main__":
    # creating processes
    calc(5, 6)
