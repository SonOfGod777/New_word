# -*- coding: utf-8 -*-
import pickle, os, json, jieba, collections
import pandas as pd
import numpy as np
from collections import defaultdict
# from sqlalchemy import create_engine
pd.set_option('display.max_columns', None)


def save_model(model, filename):
    """保存模型"""
    with open(filename, 'wb') as fw:
        pickle.dump(model, fw)


def load_model(filename):
    """加载模型"""
    with open(filename, 'rb') as fr:
        model = pickle.load(fr)
    return model


def get_stopwords():
    """读取停用词"""
    with open('data/stopword.txt', 'r' , encoding='utf-8') as f:
        return set([line.strip() for line in f])


def generate_ngram(input_list, n):
    '''生成n_gram模型'''
    result = []
    for i in range(1, n+1):
        result.extend(zip(*[input_list[j:] for j in range(i)]))
    return result


def load_dictionary(filename):
    """
    加载外部词频记录
    """
    word_freq = {}
    with open(filename, 'r' , encoding='utf-8') as f:
        for line in f:
            try:
                line_list = line.strip().split(' ')
                # 规定最少词频
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = line_list[1]
            except IndexError as e:
                continue
    return word_freq


def load_data(line_lis, stopwords, seg=True):
    """
    粗略分词，过滤掉停用词
    """
    # jieba.load_userdict(userdict)
    data = []
    for line in line_lis:
        try:
            if seg:
                word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords and not x.isdigit() and not x.encode().isalpha()]
            else:
                word_list = [x for x in line.strip if x not in stopwords and not x.isdigit() and not x.encode().isalpha()]
        except:
            print(line)
        data.append(word_list)
    return data


def load_data_2_root(root , data):
    '''
    生成n_gram模型，添加到根目录
    '''
    for word_list in data:
        ngrams = generate_ngram(word_list, 5)
        for d in ngrams:
            root.add(d)
            root.add_reverse(d)
    return len(ngrams)
