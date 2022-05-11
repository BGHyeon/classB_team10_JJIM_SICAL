from flask import Flask, render_template,abort,jsonify,session,request,redirect,url_for
from pymongo import MongoClient
import certifi
from selenium import webdriver
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import uuid
import jwt
import hashlib
import traceback
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


SECRET_KEY = 'jjimsical'
ca = certifi.where()
client = MongoClient("mongodb+srv://admin:admin@cluster0.16hc5.mongodb.net/Cluster0?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.jjimsical
app = Flask(__name__)
app.secret_key=SECRET_KEY
sched = BackgroundScheduler(daemon=True)


# login 관련 기능 (종연)
@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')

# login
@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': username_receive, 'pw': pw_hash},{'_id':False})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 관련 기능 (승현)
@app.route('/join')
def register():
    return render_template('join.html')

# 회원가입
@app.route('/join',methods=['POST'])
def join_request():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_give = request.form['nick_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {'id': id_receive,
           'pw': pw_hash,
           'nick': nick_give,
            'favorite':[]
           }


    db.user.insert_one(doc)

    return jsonify({'result': 'success' })

# id 중복체크(회원가입)
@app.route('/idcheck',methods=['POST'])
def show_id():
    id_receive = request.form['id_give']
    all_user = list(db.user.find({},{'_id':False}))
    msg = '생성 가능한 아이디입니다.'
    for user in all_user:
        if user['id'] == id_receive:
            msg = '중복된 아이디입니다.'
    return jsonify({'msg': msg})

# 메인 페이지 관련 기능 개발(규현, 승재)
@app.route('/')
def index():
    token_resive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_resive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({'id': payload['id']});
        if user_info is None:
            return redirect(url_for('login', msg='로그인후 사용해 주세요.'))
        lists = list(db.performance.find({}, {'_id': False}))
        return render_template('index.html', data=lists)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 없습니다.'))

# 사용자 정보 조회
# 사용자가 찜한 정보를 조회하기 위해 사용
@app.route('/userinfo',methods=['GET'])
def get_user_info():
    token_resive = request.cookies.get('mytoken')
    payload = jwt.decode(token_resive, SECRET_KEY, algorithms=['HS256'])
    data= db.user.find_one({'id': payload['id']},{'_id':False})
    if data is None:
        abort(404)
    return jsonify(data)

# 공연 상세 정보
# modal창 내부의 정보를 표시하기 위해 사용
@app.route('/info/<musicalid>',methods=['GET'])
def get_musical_info(musicalid):
    print(musicalid)
    data = db.performance.find_one({'id':musicalid},{'_id':False})
    comments = list(db.comment.find({'musicalid':musicalid},{'_id':False}))
    ret = {
        'data' : data,
        'comment' : comments
    }
    if data is None:
        abort(404)
    return jsonify(ret)

# 코멘트 정보 달기 기능
@app.route('/add/comment/<musicalid>', methods=['POST'])
def add_comment(musicalid):
    token_resive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_resive, SECRET_KEY, algorithms=['HS256'])
        userid = db.user.find_one({'id': payload['id']})
        comment_receive = request.form['comment_give']
        doc = {
            'id': userid['id'],
            'nick' : userid['nick'],
            'comment': comment_receive, #musicalid 값 어떻게 추가하지..
            'musicalid': musicalid,
            'favorite':[]
        }
        db.comment.insert_one(doc)
        return jsonify({'msg': '코멘트 등록 완료'})

    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 없습니다.'))

@app.route('/comment/table',methods=['GET'])
def comment_table():

    return jsonify({'msg'})


# 찜 하기 기능
@app.route('/add/favorite/<musicalid>',methods=['PATCH'])
def add_favorite(musicalid):
    msg = ''
    data={}
    try:
        userid = session.get('id', 'Noinfo')
        user = db.user.find_one({'id':userid},{'_id':False})
        favorites = list(user['favorite'])
        likecount = db.performance.find_one({'id':musicalid})['likecount']
        if musicalid in favorites:
            favorites.remove(musicalid)
            msg = '찜 목록에서 제거되었습니다.'
            db.performance.update_one({'id':musicalid},{'$set':{'likecount':likecount-1}})
        else:
            favorites.append(musicalid)
            msg='찜 등록되었습니다.'
            db.performance.update_one({'id':musicalid},{'$set':{'likecount':likecount+1}})
        db.user.update_one({'id':userid},{'$set':{'favorite':favorites}})
        data =  db.performance.find_one({'id':musicalid},{'_id':False})
    except Exception as e :
        print(e)
        traceback.print_exc()
        msg = '오류발생 나중에 다시 시도해 주세요'
    return jsonify({'msg':msg,'data':data})


@app.route('/remove/comment',methods=['POST'])
def remove_comment():
    return

# 공연 정보 조회하기 위한 사용
# 매일 0시 0분에 공연정보를 크롤링하여 db에 저장
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
            'likecount' : 0
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
                'likecount' : 0
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
    app.run('0.0.0.0',port=5000,debug=True)