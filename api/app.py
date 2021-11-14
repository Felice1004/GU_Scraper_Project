from flask import Flask
from flask_restful import Api
from flask import Flask, render_template

from resources.user import Coat

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import concurrent.futures
import psycopg2
from config import config


app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/coat')
def coat():
    category = 'coat'
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
            result.append(item[0]) #id
            result.append(item[1]) #uid
            result.append(item[2]) #title
            result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            result.append(item[-1]) # colorid
            # ids.append(item[0])
            # uids.append(item[1])
            # titles.append(item[2])
            # imgs.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            # colors.append(item[-1])
            results.append(result)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return render_template(category+'.html', results = results)

@app.route('/jacket')
def jacket():
    category = 'jacket'
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
            result.append(item[0]) #id
            result.append(item[1]) #uid
            result.append(item[2]) #title
            result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            result.append(item[-1]) # colorid
            # ids.append(item[0])
            # uids.append(item[1])
            # titles.append(item[2])
            # imgs.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            # colors.append(item[-1])
            results.append(result)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return render_template(category+'.html', results = results)

@app.route('/parka')
def parka():
    category = 'parka'
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
            result.append(item[0]) #id
            result.append(item[1]) #uid
            result.append(item[2]) #title
            result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            result.append(item[-1]) # colorid
            # ids.append(item[0])
            # uids.append(item[1])
            # titles.append(item[2])
            # imgs.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            # colors.append(item[-1])
            results.append(result)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return render_template(category+'.html', results = results)

@app.route('/cardigan')
def cardigan():
    category = 'cardigan'
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
            result.append(item[0]) #id
            result.append(item[1]) #uid
            result.append(item[2]) #title
            result.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            result.append(item[-1]) # colorid
            # ids.append(item[0])
            # uids.append(item[1])
            # titles.append(item[2])
            # imgs.append('https://www.gu-global.com/tw/hmall/test/'+ item[1] +'/main/first/561/1.jpg')
            # colors.append(item[-1])
            results.append(result)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return render_template(category+'.html', results = results)

if __name__ == "__main__":
    app.run()