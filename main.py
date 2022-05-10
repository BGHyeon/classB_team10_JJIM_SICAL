from flask import Flask, render_template,request,jsonify
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import uuid
client = MongoClient("mongodb+srv://admin:admin@cluster0.16hc5.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.jjimsical
app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
# login 관련 기능 (종연)
@app.route('/login',methods=['GET'])
def login():
    return render_template('')

@app.route('/login',methods=['POST'])
def login_request():
    print('hello')
    return

# 회원가입 관련 기능 (승현)
@app.route('/join',methods=['GET'])
def join():
    return render_template('')

@app.route('/join',methods=['POST'])
def join_request():
    print('hello')
    return

@app.route('/idcheck',methods=['POST'])
def join_equest():
    print('hello')
    return


# 메인 페이지 관련 기능 개발(규현, 승재)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info',methods=['POST'])
def get_musical_info():
    return

@app.route('/add/comment',methods=['POST'])
def add_comment():
    return

@app.route('/add/favorite',methods=['POST'])
def add_favorite():
    return

@app.route('/remove/comment',methods=['POST'])
def remove_comment():
    return

@app.route('/remove/favorite',methods=['POST'])
def remove_favorite():
    return

def refreshData():
    return

@sched.scheduled_job('cron',hour='0',minute='0',id='initdata')
def crawlingInfo():
    return

sched.start()

if __name__ == '__name__':
    app.run('0.0.0.0',port=5000,debug=True)