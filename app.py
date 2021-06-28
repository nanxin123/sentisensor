from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator

# from textblob import TextBlob

app = Flask(__name__)

person = {
    'title': '简历',
    'first_name': '南',
    'last_name': '新',
    'address': '9 rue Léon Giraud · PARIS · FRANCE',
    'job': 'Web developer',
    'call': '13986540189',
    'email': '2531540573@qq.com',
    'city': '武汉',
    'description': '一名普通程序员.',
    'social_media': [
        {
            'link': 'https://www.facebook.com/nono',
            'icon': 'fa-facebook-f'
        },
        {
            'link': 'https://github.com/nono',
            'icon': 'fa-github'
        },
        {
            'link': 'linkedin.com/in/nono',
            'icon': 'fa-linkedin-in'
        },
        {
            'link': 'https://twitter.com/nono',
            'icon': 'fa-twitter'
        }
    ],
    'img': 'img/img_nono.jpg',
    'experiences': [
        {
            'time': '参与时间',
            'name': '项目名称',
            'project_name': '谷粒商城',
            'project_time': '2021.03.01 - 2021.06.18',
            'description': '项目描述',
            'project_description': '谷粒商城是一套B2C模式电商系统，包括前台商城和后台管理系统,销售自营给客户。后台管理系统和前台商城都是基于基于SpringBoot实现。后台管理系统包含商品管理、库存管理、订单管理、营销管理，用户管理，内容管理。前台商城包含首页门户，商品推荐，商品搜索，商品展示，购物车，订单流程，商品秒杀,用户认证。',
            'skill':'涉及技术',
            'project_skill':'Spirng、SpringMVC、SpringBoot、MyBatisPuls、Redis、MySQL、SpringCloud、RabbitMq、Elasticsearch、Thymleaf、Vue等',
            'design':'设计技术',
            'project_design':['1、采用分布式的项目开发模式整个项目分为：认证服务、会员服务、订单服务、商品服务、检索服务、购物车服务、秒杀服务等。',
                              '2、基于RabbitMq支持消息事务这一特点，采用最大努力通知的分布式事务解决方案去处理分布式事务场景。',
                              '3、基于延时队列这一特点实现定时关单功能，以及实现	秒杀	活动高并发访问场景的流量削峰。',
                              '4、基于Redis消息中间件，实现了购物车，接口幂等，秒杀活动等高并发访问场景的开发。',
                              '5、采用Redisson框架解决Redis在分布式情况下锁的问题。',
                              '6、采用线程池异步执行任务，提高整个商品详细页面的访问速度。'
                              ],
            'duty':'责任描述',
            'duty_description':['1.负责后台管理系统后端开发','2.负责前台商城后端开发','3.负责部分前端代码编写','4.负责项目的部署']
        }
    ],
    'education': [
        {
            'university': '高中',
            'degree': 'Projets informatiques et Startégies d\'entreprise (PISE)',
            'description': 'Gestion de projets IT, Audit, Programmation',
            'mention': 'Bien',
            'timeframe': '2015 - 2016'
        },
        {
            'university': 'Paris Dauphine',
            'degree': 'Master en Management global',
            'description': 'Fonctions supports (Marketing, Finance, Ressources Humaines, Comptabilité)',
            'mention': 'Bien',
            'timeframe': '2015'
        },
        {
            'university': 'Lycée Turgot - Paris Sorbonne',
            'degree': 'CPGE Economie & Gestion',
            'description': 'Préparation au concours de l\'ENS Cachan, section Economie',
            'mention': 'N/A',
            'timeframe': '2010 - 2012'
        }
    ],
    'programming_languages': {
        'HMTL': ['fa-html5', '100'],
        'CSS': ['fa-css3-alt', '100'],
        'SASS': ['fa-sass', '90'],
        'JS': ['fa-js-square', '90'],
        'Wordpress': ['fa-wordpress', '80'],
        'Python': ['fa-python', '70'],
        'Mongo DB': ['fa-database', '60'],
        'MySQL': ['fa-database', '60'],
        'NodeJS': ['fa-node-js', '50']
    },
    'languages': {'French': 'Native', 'English': 'Professional', 'Spanish': 'Professional',
                  'Italian': 'Limited Working Proficiency'},
    'interests': ['Dance', 'Travel', 'Languages']
}


@app.route('/')
def cv(person=person):
    return render_template('index.html', person=person)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route('/chart')
def index():
    return render_template('chartsajax.html', graphJSON=gm())


def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country'] == country], x="year", y="gdpPercap")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@app.route('/senti')
def main():
    text = ""
    values = {"positive": 0, "negative": 0, "neutral": 0}

    with open('ask_politics.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 2000 == 0:
                break
            if 'text' in row:
                nolinkstext = re.sub(
                    r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                    '', row['text'], flags=re.MULTILINE)
                text = nolinkstext

            blob = TextBlob(text)
            for sentence in blob.sentences:
                sentiment_value = sentence.sentiment.polarity
                if sentiment_value >= -0.1 and sentiment_value <= 0.1:
                    values['neutral'] += 1
                elif sentiment_value < 0:
                    values['negative'] += 1
                elif sentiment_value > 0:
                    values['positive'] += 1

    values = sorted(values.items(), key=operator.itemgetter(1))
    top_ten = list(reversed(values))
    if len(top_ten) >= 11:
        top_ten = top_ten[1:11]
    else:
        top_ten = top_ten[0:len(top_ten)]

    top_ten_list_vals = []
    top_ten_list_labels = []
    for language in top_ten:
        top_ten_list_vals.append(language[1])
        top_ten_list_labels.append(language[0])

    graph_values = [{
        'labels': top_ten_list_labels,
        'values': top_ten_list_vals,
        'type': 'pie',
        'insidetextfont': {'color': '#FFFFFF',
                           'size': '14',
                           },
        'textfont': {'color': '#FFFFFF',
                     'size': '14',
                     },
    }]

    layout = {'title': '<b>意见挖掘</b>'}

    return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0", threaded=True)













