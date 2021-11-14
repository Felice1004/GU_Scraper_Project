from flask import Flask
from flask_restful import Api
from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import concurrent.futures
import psycopg2
from config import config
from resources.categoryItems import CategoryItems
from resources.itemDetailView import ItemDetailView
app = Flask(__name__)
api = Api(app)

api.add_resource(CategoryItems, "/category/<string:category>")
api.add_resource(ItemDetailView, "/category/<string:category>/id/<string:id>")


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()