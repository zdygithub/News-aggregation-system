# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from . import models
import jieba.analyse
import math


# 新闻列表（响应函数）
def NewsList(request):
    session = request.session.get('username',default=None)
    if session != None:
        user = models.UserInfo.objects.get(username=session)
        news1 = models.NewsData.objects.all().order_by('-id')[:10]  # 从数据库中取出所有数据，并按id降序排列

        rec_dict={}
        # 对前10个新闻进行推荐匹配
        for n in news1:
            # 分词
            res1 = cut_word(article=user.keyword)
            res2 = cut_word(article=n.keyword)
            # 计算出词频向量
            vectors = tf_idf(res1, res2)
            # 相似度
            similarity = run(vector1=vectors[0], vector2=vectors[1])

            # 相似度字典
            rec_dict[n.id] = similarity
        # 对字典 按value进行 倒序排序，返回列表[(),(),()]
        rec_list = sorted(rec_dict.items(), key=lambda items:items[1], reverse=True)
        print(rec_list)

        news = []
        for each in rec_list:
            each_news = models.NewsData.objects.get(id=each[0])
            news_dict = {'id':each_news.id, 'title':each_news.title, 'content':each_news.content,
                         'front_image_url':each_news.front_image_url}
            news.append(news_dict)

    else:
        news = models.NewsData.objects.all().order_by('-id')[:10]  # 从数据库中取出所有数据，并按id降序排列

    return render(request, 'news_list.html', {'news':news, 'session':session})  # 跳转到主页面，并将news对象传递到前端


# 新闻内容展示（响应函数）
def NewsContent(request, n_id=1):
    session = request.session.get('username', default=None)
    news = models.NewsData.objects.get(id=n_id)
    user = models.UserInfo.objects.get(username=session)
    user.keyword = news.keyword
    user.save()
    return render(request, 'news_content.html', {'news':news})


# 登录（响应函数）
def NserLogin(request):
    name = request.POST.get('name')  # 获取前端form表单提交的数据
    password = request.POST.get('password')

    if models.UserInfo.objects.filter(username=name, password=password):
        request.session['username'] = name
        # news = models.NewsData.objects.filter(site_original=u'网易')  # 从数据库中取出所有数据，并按id降序排列
        return NewsList(request)  # 跳转到主页面，并将news对象传递到前端
    else:
        # news = models.NewsData.objects.all().order_by('-id')[:10]  # 从数据库中取出所有数据，并按id降序排列
        return NewsList(request)  # 跳转到主页面，并将news对象传递到前端


# 登出（响应函数）
def NserLogout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return NewsList(request)


# 相似度 推荐算法

def cut_word(article):
    # 分词
    # 这里使用了TF-IDF算法。
    # 返回：[(),(),()]
    res = jieba.analyse.extract_tags(sentence=article, topK=20, withWeight=True)
    return res

def tf_idf(res1=None, res2=None):
    # 向量，可以使用list表示
    vector_1 = []
    vector_2 = []
    # 词频，可以使用dict表示
    tf_1 = {i[0]: i[1] for i in res1}
    tf_2 = {i[0]: i[1] for i in res2}
    res = set(list(tf_1.keys()) + list(tf_2.keys()))  # 出现的所有的词语

    # 填充词频向量
    for word in res:
        if word in tf_1:
            vector_1.append(tf_1[word])
        else:
            vector_1.append(0)
        if word in tf_2:
            vector_2.append(tf_2[word])
        else:
            vector_2.append(0)

    return vector_1, vector_2

def numerator(vector1, vector2):
    # 分子
    return sum(a * b for a, b in zip(vector1, vector2))

def denominator(vector):
    # 分母
    return math.sqrt(sum(a * b for a, b in zip(vector, vector)))

def run(vector1, vector2):
    # 余弦相似度
    return numerator(vector1, vector2) / (denominator(vector1) * denominator(vector2))