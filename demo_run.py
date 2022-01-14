# -*- coding: utf-8 -*-
import os
from config import basedir
import model
import utils
import time


def read_txt(path):
    with open(path,'r',encoding='utf-8') as file:
        data = [str(w).split()[1].strip() for w in file ]
        return list(set(data))


"""初始化模型，flask接口形式，不必反复初始化"""
stopwords = utils.get_stopwords()  # 加载停用词
root_name = basedir + "/data/root.pkl"  # 创建root目录
if os.path.exists(root_name):
    root = utils.load_model(root_name)
else:
    dict_name = basedir + '/data/dict.txt'
    word_freq = utils.load_dictionary(dict_name)
    root = model.TrieNode(word_freq)
    utils.save_model(root, root_name)


if __name__ == '__main__':
    row_data = read_txt('data/row_data.txt')
    t0 = time.time()
    data = utils.load_data(row_data, stopwords)  # 提取分词文本
    total = utils.load_data_2_root(root, data)   # 将新的文本插入到Root中
    result = root.find_word()
    t1 = time.time()
    print(t1-t0, result)







