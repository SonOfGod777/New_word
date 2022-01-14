# -*- coding: utf-8 -*-
import math
from collections import defaultdict


class Node(object):
    def __init__(self):
        self.word = None
        self.word_finish = False
        self.count = 0
        self.index = None
        self.child = defaultdict(Node)


class TrieNode(object):
    """
    建立前缀树，并且包含统计词频，计算左右熵，计算互信息的方法
    """
    def __init__(self, data=None, PMI_limit=20):
        self.root = Node()
        self.root_reverse = Node()
        self.PMI_limit = PMI_limit
        self.dic = {}
        self.total = 0

        if not data:
            return
        curr_node = self.root
        for key, values in data.items():
            curr_node.child[key]
            curr_node.count = int(values)

    def add(self, words):
        curr_node = self.root
        for char in words:
            curr_node = curr_node.child[char]
        curr_node.word_finish = True
        curr_node.word = words
        curr_node.count += 1

    def add_reverse(self, words):
        cur_node = self.root_reverse
        words = tuple(reversed(words))
        for word in words:
            cur_node = cur_node.child[word]
        cur_node.word = words
        cur_node.word_finish = True
        cur_node.count += 1

    def search_one(self):
        one_dic = {}
        one_total = 0
        node = self.root
        for word, child in node.child.items():
            if child.word_finish == True:
                one_total += child.count
                one_dic[word] = child.count
        return one_total, one_dic

    def search_bi(self):
        bi_dic = {}
        bi_total = 0
        node = self.root
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                if child1.word_finish == True:
                    bi_total += child1.count
                    bi_dic[word + '_' + word1] = child1.count
        return bi_total, bi_dic

    def search_th(self):
        th_dic, th_rigth_dic = {}, {}
        th_total, p = 0, 0
        node = self.root
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    if child2.word_finish == True:
                        th_total += child2.count
                        th_dic[word + '_' + word1 + '_' + word2] = child2.count
                for word2, child2 in child1.child.items():
                    if child2.word_finish == True:
                        p += child2.count / th_total * math.log(child2.count / th_total, 2)
                th_rigth_dic[word + '_' + word1] = -p
        return th_total, th_dic, th_rigth_dic

    def search_fo(self):
        fo_dic, fo_rigth_dic = {}, {}
        fo_total, p = 0, 0
        node = self.root
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    for word3, child3 in child2.child.items():
                        if child3.word_finish == True:
                            fo_total += child3.count
                            fo_dic[word + '_' + word1 + '_' + word2 + '_' + word3] = child3.count
                    for word3, child3 in child2.child.items():
                        if child3.word_finish == True:
                            p += child3.count / fo_total * math.log(child3.count / fo_total, 2)
                    fo_rigth_dic[word + '_' + word1 + '_' + word2] = -p
        return fo_total, fo_dic, fo_rigth_dic

    def rigth_fi(self):
        fi_rigth_dic = {}
        fi_total, p = 0, 0
        node = self.root
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    for word3, child3 in child2.child.items():
                        for word4, child4 in child3.child.items():
                            if child4.word_finish == True:
                                fi_total += child4.count
                        for word4, child4 in child3.child.items():
                            if child4.word_finish == True:
                                p += child4.count / fi_total * math.log(child4.count / fi_total, 2)
                        fi_rigth_dic[word + '_' + word1 + '_' + word2 + '_' + word3] = -p
        return fi_rigth_dic

    def left_fi(self):
        fi_left_dic = {}
        fi_total, p = 0, 0
        node = self.root_reverse
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    for word3, child3 in child2.child.items():
                        for word4, child4 in child3.child.items():
                            if child4.word_finish == True:
                                fi_total += child4.count
                        for word4, child4 in child3.child.items():
                            if child4.word_finish == True:
                                p += child4.count / fi_total * math.log(child4.count / fi_total, 2)
                        fi_left_dic[word3 + '_' + word2 + '_' + word1 + '_' + word] = -p
        return fi_left_dic

    def left_th(self):
        th_left_dic = {}
        p, total = 0, 0
        node = self.root_reverse
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    if child2.word_finish == True:
                        total += child2.count
                for word2, child2 in child1.child.items():
                    if child2.word_finish == True:
                        p += child2.count / total * math.log(child2.count / total, 2)
                th_left_dic[word1 + '_' + word] = -p
        return th_left_dic

    def left_fo(self):
        fo_left_dic = {}
        p, total = 0, 0
        node = self.root_reverse
        for word, child in node.child.items():
            for word1, child1 in child.child.items():
                for word2, child2 in child1.child.items():
                    for word3, child3 in child2.child.items():
                        if child3.word_finish == True:
                            total += child3.count
                    for word3, child3 in child2.child.items():
                        if child3.word_finish == True:
                            p += child3.count / total * math.log(child3.count / total, 2)
                    fo_left_dic[word2 + '_' + word1 + '_' + word] = -p
        return fo_left_dic

    def search(self, start_node=None, word=None):
        if start_node:
            node = start_node
        else:
            node = self.root
        for child in node.child.values():
            if child.word_finish == True:
                self.total += child.count
                if word:
                    word = word + '_' + child.word
                    self.dic[word] = child.count
                else:
                    self.dic[child.word] = child.count
                    word = child.word

            self.search(child, word)

    def find_word(self, pmi_thre=70, freq_thre=3, free_thre=7):
        one_total, one_dic = self.search_one()
        bi_total, bi_dic = self.search_bi()
        th_total, th_dic, th_rigth_dic = self.search_th()
        fo_total, fo_dic, fo_rigth_dic = self.search_fo()
        fi_rigth_dic = self.rigth_fi()

        th_left_dic = self.left_th()
        fo_left_dic = self.left_fo()
        fi_left_dic = self.left_fi()

        total = one_total + bi_total + th_total + fo_total
        fre_dic = {**one_dic, **bi_dic, **th_dic, **fo_dic}
        left_dic = {**th_left_dic, **fo_left_dic, **fi_left_dic}
        rigth_dic = {**th_rigth_dic, **fo_rigth_dic, **fi_rigth_dic}

        freedom_dic = {k: rigth_dic[k] if v > rigth_dic[k] else v for k, v in left_dic.items()}
        pmi_dic = {}
        for words, count in fre_dic.items():
            words_lis = str(words).split('_')
            if len(words_lis) > 1:
                px_py = max([fre_dic.get('_'.join(words_lis[:j])) * fre_dic.get('_'.join(words_lis[j:])) for j in
                             range(1, len(words_lis))])
                pmi = fre_dic.get(words) * total / px_py
                pmi_dic[words] = pmi

        words_fre = {k: v for k, v in fre_dic.items() if v > freq_thre}
        freedom_dic = {k: v for k, v in freedom_dic.items() if v > free_thre}
        pmi_dic = {k: v for k, v in pmi_dic.items() if v > pmi_thre}

        return [w for w in pmi_dic if w in freedom_dic and w in words_fre]
