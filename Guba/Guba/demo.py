import re
from tqdm import tqdm
import pymysql
import settings
import redis
import math

#
page = 'http://guba.eastmoney.com/news,gs600518,838966979.html'
#
#
print(re.findall(r',(\S+),', page)[0])


print('来源：东方财富网 作者：数据中心'.split('：')[-1])
# print(re.findall(r',(\d+)\.', page)[0])

# print(ls)

# print(re.findall(r'\|(\d+)\|', page))

# print(math.ceil(int(ls[0])/int(ls[1])))

# r = redis.Redis(host='localhost', port=6379, db=0)
#
# r.set('foo', 'bar')
#
# print(r.get('foo'))

#
# connect = pymysql.connect(
#     host=settings.MYSQL_HOST,
#     db=settings.MYSQL_DBNAME,
#     user=settings.MYSQL_USER,
#     passwd=settings.MYSQL_PASSWD,
#     charset='utf8',
#     use_unicode=True)
#
# cursor = connect.cursor()
#
# sql = "SELECT code FROM Companys where Companys.`type` = '沪市' ORDER BY  code ASC"
#
# cursor.execute(sql)

# results = cursor.fetchall()

# for row in results:
#     url = "http://guba.eastmoney.com/list,{code},1,f_1.html".format(code=row[0])
#     # 打印结果
#     redis_connect.rpush('Guba:start_urls', url)
#     print("url=%s" % url)

# connect.close()
#
#
#
# http://guba.eastmoney.com/topic,900942.html
#
# http://guba.eastmoney.com/list,600518,1,f_1.html

# redis_connect = redis.Redis(host='localhost', port=6379, db=0)

# pool = redis.ConnectionPool(host='120.***.***.***', port=6379, db=0, password='*******', decode_responses=True)
# redis_connect = redis.Redis(connection_pool=pool)
#
# redis_connect_local = redis.Redis(host='localhost', port=6379, db=0)
#
# temp = redis_connect_local.lrange("NewsContent:start_urls", 0, -1)
#
# for linkurl in tqdm(temp):
#     redis_connect.rpush('NewsContent_bkp:start_urls', linkurl)
#
# print(len(temp), len(set(temp)))

# test_date = '发表于 2019-06-06 16:33:46'
#
# res = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", test_date)
#
# print(res)
#
# str = '\r\n                                                康美是不是要收广告费呀？ \r\n                                            '
#
# print(str.replace('\r', '').replace('\n', '').strip())

# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# redis_connect = redis.Redis(connection_pool=pool)


