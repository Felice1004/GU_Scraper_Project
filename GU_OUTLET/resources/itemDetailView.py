from flask_restful import Resource 
from config import config
from flask import Flask, render_template, make_response
import psycopg2

class ItemDetailView(Resource):
    def get(self, category, id):
        categories = ['coat', 'jacket','parka','cardigan']
        if category not in categories:
            return make_response('page not found')
        else:
            
            sql_item = "SELECT * FROM ITEM WHERE itemid = " + "'" + id + "'"
            sql_price = "SELECT * FROM PRICE WHERE itemid = " + "'" + id + "'"
            sqls = [sql_item, sql_price]
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                results = []
                for sql in sqls:
                    cur.execute(sql)
                    result = cur.fetchall()
                    if 'ITEM' in sql:
                        for item in result:
                            result = []
                            result.append(item[0]) #id
                            result.append(item[1]) #uid
                            result.append(item[2]) #title
                            result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
                            result.append(item[-1]) # colorid
                            results.append(result)
                    if 'PRICE' in sql:
                        for price in result:
                            for item in results:
                                if price[0] in item:
                                    item.append(price[1])
                                    break
                for r in results:
                    print(r)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            # return render_template(category+'.html', results = results)
            return make_response(render_template('itemDetail.html',results = results),200)

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass