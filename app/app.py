# 用flask写一个接口，根据入参路径的不同，如getData/5, getData/15, getData/30, getData/60, 
# 分别以5min、15min、30min、60min为时间分割点，把data.txt中的数据分隔成一个一个点，每个点的数值是该段时间内的统计事件数
# data.txt中每一行如下：
# {"docId":"9973483e98d7d8ca0484709ff5e14c9854d_0","newsCpId":"100","language":"zh","source":"新浪","FirstCategory":"时政: 0.99, ","title":"“台湾是中国的一部分”，摇滚歌手沃特斯仗义执言","level3MainTopic":"1165","picUrl":"https://tysearch-imagepub-drcn.obs.cn-south-1.myhuaweicloud.com/866bd37c416eb41000cbf4963a537e4e_m500","level3Topic":"1165: 0.21974025666713715, ","picUrlList":[],"wordNer":"[{\"entity\":\"台湾\",\"type\":\"LOC\"},{\"entity\":\"中国\",\"type\":\"LOC\"}]","level2MainTopic":"224","publishName":"新浪","summary":"“台湾是中国的一部分”，摇滚歌手沃特斯仗义执言","publishTime":"1659977076","keywordForFeed":"沃特斯: 6.421843528747559, 一部分: 3.1342108249664307, 仗义执言: 6.656825542449951, ","isVideo":"false","level1Topic":"14: 0.35514017939567566, 25: 0.1355140209197998, 26: 0.11214952915906906, ","url":"https://finance.sina.com.cn/tech/roll/2022-08-09/doc-imizmscv5407432.shtml","SecondCategory":"","tags":"[{\"from_type\":[\"title_keyword\"],\"entity_type\":\"\",\"weight\":8006.421843528748,\"word\":\"沃特斯\",\"normalized_word\":\"\"},{\"from_type\":[\"title_keyword\"],\"entity_type\":\"\",\"weight\":3003.1342108249664,\"word\":\"一部分\",\"normalized_word\":\"\"},{\"from_type\":[\"entity\"],\"entity_type\":\"LOC\",\"weight\":1.6970704793930054,\"word\":\"台湾\",\"normalized_word\":\"\"},{\"from_type\":[\"entity\"],\"entity_type\":\"LOC\",\"weight\":1.2150416374206543,\"word\":\"中国\",\"normalized_word\":\"\"}]","realTitle":"“台湾是中国的一部分”，摇滚歌手沃特斯仗义执言","contentKeywordForFeed":"中国: 16003.535964488983, 台湾: 9004.64979314804, 沃特斯: 8017.3058795928955, 西方: 8009.126523971558, 国家: 7004.691147327423, 一个中国原则: 5014.0998430252075, 西方国家: 5012.407744407654, 美国: 5003.847471237183, 公报: 4010.9069232940674, 中美: 4008.538659095764, ","region":"my","level1MainTopic":"14","level2Topic":"74: 0.13161993026733398, 160: 0.1129283457994461, 224: 0.1456386297941208, "}
from flask import Flask, render_template
from flask_cors import CORS
import json, time

app = Flask(__name__) #
CORS(app, supports_credentials=True)
# 配置static为静态文件目录
app.config['STATIC_FOLDER'] = 'static'

with open('data.txt', encoding='utf-8') as f:
    lines = f.readlines()
    
@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

# getData/:splitKey接口
@app.route('/getData/<split_len>', methods=['GET'])
def get_data(split_len):
    data = [json.loads(line) for line in lines]
    # 按照splitKey分割data, 统计每个分割段的事件数
    time_len = int(split_len) * 60 # 分钟转换成秒
    result = []
    start_time = int(data[0]['publishTime'])
    split_time = start_time + time_len # 第一个分割点
    the_time = time.strftime("%H:%M:%S", time.localtime(start_time))
    result.append({'time': the_time, 'count': 1})
    for item in data:
      publish_time = int(item['publishTime'])
      if publish_time > split_time:
        split_time = publish_time + time_len # 更新分割点为下一个分割段的开始时间
        # 转换时间戳为时间
        the_time = time.strftime("%H:%M:%S", time.localtime(publish_time))
        result.append({'time': the_time, 'count': 1})
        result[-1]['count'] = 1 # 该段时间内的事件数
      else:
        result[-1]['count'] += 1
      
    return json.dumps(result) # 返回json格式的数据, 
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)