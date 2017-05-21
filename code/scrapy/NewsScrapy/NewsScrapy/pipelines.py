# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import math,sys
import jieba.analyse


class NewsscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


# TF-IDF算法和余弦相似性
class NewsSimilarPipeline(object):
    def process_item(self, item, spider):
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="1234", db="news_db", charset="utf8")
        cursor = conn.cursor()
        # sql = "select content,title from news_data order by id desc limit 10 "  # 逆序查询10个
        sql = "select content_html,title from news_data "
        cursor.execute(sql)
        contents = cursor.fetchall()
        conn.commit()
        conn.close()
        sys.stdout.write('文本相似度匹配中：' + '->' + "\b\b")
        for content in contents:
            article_a = content[0]
            article_b = item['content_html']
            # 分词
            res1 = self.cut_word(article=article_a)
            res2 = self.cut_word(article=article_b)

            # 计算出词频向量
            vectors = self.tf_idf(res1, res2)
            # 相似度
            similarity = self.run(vector1=vectors[0], vector2=vectors[1])
            sys.stdout.write('█' + '->' + "\b\b") # 进度条
            sys.stdout.flush()

            # 为item 添加关键字
            if item['keyword'] == '0':
                for i in range(3):
                    keyword = res1[i][0]
                    item['keyword'] = item['keyword'] + keyword + ','

            # 相似度
            if similarity < 0.9:
                if similarity > 0.75: # 相似新闻
                    item['similar'] = 1
                    print('\n匹配到相似新闻-->'+item['title']+'\n相似新闻-->'+content[1])
                    item['title'] = content[1]
            else:
                item['similar'] = 2 # 重复标志

        return item

    def cut_word(self, article):
        # 分词
        # 这里使用了TF-IDF算法。
        # 返回：[(),(),()]
        res = jieba.analyse.extract_tags(sentence=article, topK=20, withWeight=True)
        return res

    def tf_idf(self, res1=None, res2=None):
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

    def numerator(self, vector1, vector2):
        # 分子
        return sum(a * b for a, b in zip(vector1, vector2))

    def denominator(self, vector):
        # 分母
        return math.sqrt(sum(a * b for a, b in zip(vector, vector)))

    def run(self, vector1, vector2):
        # 余弦相似度
        return self.numerator(vector1, vector2) / (self.denominator(vector1) * self.denominator(vector2))


# 使用异步机制写入mysql
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        if item['similar'] != 2:
            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
                    insert ignore into news_data(title, title_original, site_original, url_original,
                                                newstime, content, content_html,front_image_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql,(item["title"], item["title_original"],
                                   item["site_original"], item["url_original"],
                                   item["newstime"], item["content"], item["content_html"],
                                   item['front_image_url'],))