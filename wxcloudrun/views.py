from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread
from flask import Flask


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


app = Flask(__name__)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    f = request.data.decode()[8:-1]
    seg = pkuseg.pkuseg()
    text = seg.cut(f)
    text = str(text)
    bg_pic = imread('E:\竞赛数据集\设计大赛\R-C.jpg')
    wordcloud = WordCloud(mask=bg_pic,background_color='white',font_path='E:\竞赛数据集\设计大赛\华文楷体.ttf',scale=1.5).generate(text)
    '''参数说明：
    mask:设置背景图片   background_color:设置背景颜色
    scale:按照比例进行放大画布，此处指长和宽都是原来画布的1.5倍
    generate(text)：根据文本生成词云 '''

    plt.imshow(wordcloud)
    #显示图片时不显示坐标尺寸
    plt.axis('off')
    #显示词云图片
    # plt.show()
    wordcloud.to_file('E:\微信开发者工具\学习管理辅助系统\static\wordcloud.jpg')
    return "ok"

if __name__ == '__main__':
    app.run(
        host='192.168.1.195',
        port=5000,
        debug=True,
    )
