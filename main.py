from flask import Flask, render_template, abort, jsonify, request, redirect, url_for,session
from pymongo import MongoClient
from selenium import webdriver
import requests
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import uuid
client = MongoClient("mongodb+srv://admin:admin@cluster0.16hc5.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.jjimsical
app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
SECRET_KEY = 'jjimsical'

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})




# 회원가입 관련 기능 (승현)

@app.route('/join')
def join():
   return render_template('join.html')

@app.route('/join',methods=['GET'])
def join_get():
    return render_template('join.html')

@app.route('/join',methods=['POST'])
def join_request():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_give = request.form['name_give']
    gender_give = request.form['gender_give']
    nick_give = request.form['nick_give']
    phone_give = request.form['phone_give']

    doc = {'id': id_receive,
           'pw': pw_receive,
           'name': name_give,
           'gender': gender_give,
           'nick': nick_give,
           'phone': phone_give,
           'favorite':[]}
    db.user.insert_one(doc)

    return jsonify({'msg': '가입 완료'})

@app.route('/idcheck',methods=['POST'])
def show_id():
    id_receive = request.form['id_give']
    all_user = list(db.user.find({},{'_id':False}))
    # print(all_user)
    msg ='아이디를 입력해주세요'
    for user in all_user:
        if user['id'] == id_receive:
            msg = '중복된 아이디입니다.'
        else:
            msg = '생성 가능한 아이디입니다.'
    # print(all_movies[0]['title'])
    return jsonify({'msg': msg})


# 메인 페이지 관련 기능 개발(규현, 승재)
@app.route('/')
def index():
    token_resive = request.cookies.get('jwt_token')
    try:
        payload = jwt.decode(token_resive,SECRET_KEY,algorithms=['HS256'])
        user_info = db.user.find_one({'id':payload['id']});
        session['id'] = user_info['id'];
        lists = list(db.performance.find({},{'_id':False}))
        return render_template('index.html',data=lists)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login',msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 없습니다.'))

@app.route('/userinfo',methods=['GET'])
def get_user_info():
    userid = session.get('id','NoInfo')
    if userid == 'NoInfo':
        abort(404)
    data = db.user.find_one({'id': userid}, {'_id': False})
    if data is None:
        abort(404)
    return jsonify(data)

@app.route('/info/<musicalid>',methods=['GET'])
def get_musical_info(musicalid):
    print(musicalid)
    data = db.performance.find_one({'id':musicalid},{'_id':False})
    if data is None:
        abort(404)
    print(data)
    return jsonify(data)

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
    baseUrl = 'http://ticket.yes24.com'
    url = 'http://ticket.yes24.com/New/Rank/Ranking.aspx'
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("headless")
    driver = webdriver.Chrome(executable_path='./chromedriver')
    res = driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    herfs = []
    best_div = soup.find('div', {'class': 'rank-best'}).find_all('div')

    for a in best_div:
        urls = a.find('a')['href']
        res = requests.get(baseUrl + urls)
        asoup = BeautifulSoup(res.content, 'html.parser')
        data = {
            'id': str(uuid.uuid1()),
            'url': urls,
            'poster': a.select_one('span.rank-best-img').select_one('img')['src'],
            'name': a.select_one('p.rlb-tit').text,
            'date': a.select_one('p.rlb-sub-tit').text[0:21],
            'location': a.select_one('p.rlb-sub-tit').text[21:],
        }

        herfs.append(data)

    list_div = soup.find('div', {'class': 'rank-list'}).find_all('div')

    for b in list_div:
        urlss = b.select_one('p.rank-list-tit')
        if urlss is not None:

            urls = b.select_one('p.rank-list-tit').select_one('a')
            res = requests.get(baseUrl + urls['href'])
            asoup = BeautifulSoup(res.content, 'html.parser')
            poster = asoup.select_one('div.rn-product-imgbox').select_one('img')['src']
            date = asoup.select_one('span.ps-date').text
            location = asoup.find('span', {'class': 'ps-location'})
            locationText = ''
            if location is None:
                locationText = 'No Info'
            else:
                locationText = location.text
            data = {
                'id': str(uuid.uuid1()),
                'url': urls['href'],
                'poster': poster,
                'name': b.select_one('p.rank-list-tit').text,
                'date': date,
                'location': locationText,
            }
            herfs.append(data)

    for item in herfs:
        data = db.performance.find_one({'url': item['url']})
        if data is None:
            db.performance.insert_one(item)
    driver.quit()
    return

sched.start()

if __name__ == '__main__':
    app.run('0.0.0.0',port=8000,debug=True)