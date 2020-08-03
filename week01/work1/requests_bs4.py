'''
基于 Requests 和 bs4 爬取猫眼电影 Top10
@auth Li Yongbin
@time 2020-08-03
'''
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
cookie = '__mta=55530900.1595498244881.1595498716397.1595499735520.5; uuid_n_v=v1; uuid=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; _csrf=d2e2e8539904705cff1d576dffa39ccb370e3b66b82266d7951a059eb02e1a84; mojo-uuid=0f1c6e86365e634f56d43d091689d2f2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595498245; _lxsdk_cuid=1737b1b2adec8-07f24758072927-31627402-384000-1737b1b2adec8; _lxsdk=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; mojo-session-id={"id":"eed67e805d452bc7b7018f2cd1274600","time":1595592699591}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595592902; __mta=55530900.1595498244881.1595499735520.1595592902317.6; _lxsdk_s=17380bc6ee9-696-422-59f%7C%7C3'
request_header = {'user-agent': user_agent, 'Cookie': cookie}

maoyan_url = 'https://maoyan.com/films?showType=3'

response = requests.get(maoyan_url, headers=request_header)

document = bs(response.text, 'html.parser')
movie_hover_info_nodes = document.find_all('div', attrs={'class': 'movie-hover-info'})[0:10]

movie_list_top10 = []

for movie_hover_info_node in movie_hover_info_nodes:
    movie_hover_title_nodes = movie_hover_info_node.find_all('div', attrs={'class': 'movie-hover-title'})

    movie_name = movie_hover_title_nodes[0].find('span', attrs={'class': 'name'}).text
    movie_type = movie_hover_title_nodes[1].text.replace("\n", "").split(":")[1].strip()
    movie_release_time = movie_hover_title_nodes[3].text.replace("\n",     "").split(":")[1].strip()

    movie_list_top10.append({
        "name": movie_name,
        "type": movie_type,
        "time": movie_release_time,
    })

movie = pd.DataFrame(data=movie_list_top10)
movie.to_csv('./work1/movie_top10.csv', encoding='utf8', index=False, header=False)
