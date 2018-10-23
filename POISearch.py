from __future__ import print_function

import requests
import pymysql

print('Loading function')

# pool = redis.ConnectionPool(host='13.211.204.107', port=6379, decode_responses=True)
# r = redis.Redis(connection_pool=pool)
db = pymysql.connect("13.211.204.107","saicmotor","Saic1234","saicdb")

# 璋锋瓕鍦板浘浣跨敤鏂规硶锛屼絾鏄洜涓洪渶瑕佷竴涓粯璐硅处鍙凤紝鎵�浠ユ殏鏃跺厛涓嶅惎鐢�
"""{'error_message': 'You have exceeded your daily request quota for this API. If you did not set a custom daily request quota,
 verify your project has an active billing account: http://g.co/dev/maps-no-account', 'results': [], 'status': 'OVER_QUERY_LIMIT'}"""
# def query_location():
#     url="https://maps.googleapis.com/maps/api/geocode/json"
#     key = "AIzaSyCfN7bhbUQFG1H4gMZ0nQdAbesWqlmxAww"
#     address="liubu"
#     params={"address":address,"key":key}
#     result=requests.get(url,params).json()
#     print(result)
#
#
# def test():
#     url="https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCfN7bhbUQFG1H4gMZ0nQdAbesWqlmxAww"
#     result=requests.get(url).json()
#     print(result)
#     return result

def  record_rds(city,poidata):
    cursor=db.cursor()
    sql = 'insert into cptest2(user_id,poi_data,city) VALUES (%s,"%s","%s")' %(111,poidata,city)
    print(sql)
    try:
        print("db insert success")
        cursor.execute(sql.encode('utf8'))
        db.commit()
    except:
        print("db insert error")
        db.rollback()
    # db.close()


def baidu_poi(event,context):
    url="http://api.map.baidu.com/place/v2/suggestion"
    query=event["query"]
    region=event["region"]
    print(type(region))
    city_limit=event["city_limit"]
    ak = "858IXX0VryP710Oco4xMPA18AagF2As9"
    output = "json"
    params={"query":query,"region":region,"city_limit":city_limit,"ak":ak,"output":output}
    result=requests.get(url,params).json()
    record_rds(region, result)
    print(result)
    return result

print("Function End !!")

if __name__ == '__main__':
    event={"query":'tiananmen',"region":"鍖椾含","city_limit":"true"}
    baidu_poi(event,2)
    