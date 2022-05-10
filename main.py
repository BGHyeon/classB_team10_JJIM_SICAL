from flask import Flask, render_template,abort,jsonify

from pymongo import MongoClient
import certifi

ca = certifi.where()

from selenium import webdriver
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import uuid
client = MongoClient("mongodb+srv://admin:admin@cluster0.16hc5.mongodb.net/Cluster0?retryWrites=true&w=majority", tlsCAFile=ca)
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
def idcheck():
    print('hello')
    return


# 메인 페이지 관련 기능 개발(규현, 승재)
@app.route('/')
def index():
    lists = list(db.performance.find({},{'_id':False}))
    return render_template('index.html',data=lists)

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
    comment_receive = request.form['comment_give']

    doc = {
        'comment': comment_receive,
    }
    db.performance.insert_one(doc)
    
    return jsonify({'msg': '코멘트 등록 완료'})

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
    app.run('0.0.0.0', port=5000, debug=True)