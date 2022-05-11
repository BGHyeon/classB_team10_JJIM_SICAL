from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from urllib import request
baseUrl = 'http://ticket.yes24.com'
url = 'http://ticket.yes24.com/New/Rank/Ranking.aspx'
driver_options = webdriver.ChromeOptions()
driver_options.add_argument("headless")
driver = webdriver.Chrome(executable_path='./chromedriver_old.exe')
# res = requests.get(url)
# soup = BeautifulSoup(res.content,'html.parser')
driver.get(url)
soup = BeautifulSoup(driver.page_source,'html.parser')
herfs = []
best_div = soup.find('div',{'class':'rank-best'}).find_all('div')

for a in best_div:
    data = {
        'url' :a.find('a')['href'],
        'poster' : a.select_one('span.rank-best-img').select_one('img')['src'] ,
        'name' : a.select_one('p.rlb-tit').text,
        'date' : a.select_one('p.rlb-sub-tit').text[0:21],
        'location' :a.select_one('p.rlb-sub-tit').text[21:]
    }
    herfs.append(data)

list_div = soup.find('div',{'class':'rank-list'}).find_all('div')
#
# for b in list_div:
#
#     urls = b.select_one('p.rank-list-tit').select_one('a')['href']
#     res = requests.get(baseUrl + urls)
#     asoup = BeautifulSoup(res.content, 'html.parser')
#     contents = []
#     posters = asoup.select_one('#divPerfContent').find_all('img')
#     for i in posters:
#         contents.append(i['src'])
#     data = {
#         'url' : urls,
#         'poster' : b.select_one('img')['src'],
#         'name' : b.select_one('p.rank-list-tit').text,
#         'date' : b.select('div')[3].text[0:21],
#         'location' :  b.select('div')[3].text[21:],
#         'contentUrl' : contents
#     }
#     herfs.append(data)

tmp = dict.fromkeys(herfs)
herfs2 = list(tmp)
print(herfs2)
driver.quit()
