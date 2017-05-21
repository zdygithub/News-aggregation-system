# # -*- coding: utf8 -*-
# import math
# import jieba.analyse
# article_a = '我喜欢中国，也喜欢美国和日本。'
# article_b = '我喜欢足球，不喜欢篮球和网球。'
#
#
# def cut_word(article):
#     # 分词。这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
#     res = jieba.analyse.extract_tags(sentence=article, topK=20, withWeight=True)
#     return res
#
#
# def tf_idf(res1=None, res2=None):
#     # 向量，可以使用list表示
#     vector_1 = []
#     vector_2 = []
#     # 词频，可以使用dict表示
#     tf_1 = {i[0]: i[1] for i in res1}
#     tf_2 = {i[0]: i[1] for i in res2}
#     res = set(list(tf_1.keys()) + list(tf_2.keys())) # 出现的所有的词语
#
#     # 填充词频向量
#     for word in res:
#         if word in tf_1:
#             vector_1.append(tf_1[word])
#         else:
#             vector_1.append(0)
#         if word in tf_2:
#             vector_2.append(tf_2[word])
#         else:
#             vector_2.append(0)
#
#     return vector_1, vector_2
#
#
# def numerator(vector1, vector2):
#     #分子
#     return sum(a * b for a, b in zip(vector1, vector2))
#
#
# def denominator(vector):
#     #分母
#     return math.sqrt(sum(a * b for a,b in zip(vector, vector)))
#
#
# def run(vector1, vector2):
#     return numerator(vector1,vector2) / (denominator(vector1) * denominator(vector2))
#
#
# #计算出词频向量
# vectors =  tf_idf(res1=cut_word(article=article_a), res2=cut_word(article=article_b))
# # 相似度
# similarity = run(vector1=vectors[0], vector2=vectors[1])
# # 使用arccos计算弧度
# rad = math.acos(similarity)
# print(similarity, rad)
#
# # 0.2157074518785444 1.353380046633586


import sys,time
if __name__ == '__main__':
  for i in range(1,5):
    sys.stdout.write('█'+'->'+"\b\b")
    sys.stdout.flush()
    time.sleep(0.5)
