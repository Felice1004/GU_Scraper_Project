from flask_restful import Resource 
from config import config
from flask import Flask, render_template, make_response

import psycopg2

class CategoryItems(Resource):
    def get(self, category):
        categories = ['coat', 'jacket','parka','cardigan']
        if category not in categories:
            return make_response('page not found')
        else:
            sql = "SELECT * FROM ITEM WHERE Category = " + "'" + category + "'"
            conn = None
            try:
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(sql)
                result = cur.fetchall()

                results = []

                for item in result:
                    result = []
                    print(item)
                    result.append(item[0]) #id
                    result.append(item[1]) #uid
                    result.append(item[2]) #title
                    result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
                    result.append(item[-1]) # colorid
                    results.append(result)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            # return render_template(category+'.html', results = results)
            return make_response(render_template(category+'.html', results = results))

    def post(self, name):
        pass

    def put(self, name):
        pass

    def delete(self, name):
        pass