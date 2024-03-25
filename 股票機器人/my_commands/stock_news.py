import requests
from bs4 import BeautifulSoup
import datetime as dt

# 新聞資料
def stock_news(stock_name ="大盤"):
  if stock_name == "大盤":
    stock_name="台股 -盤中速報"

  data=[]
  # 取得 Json 格式資料
  json_data = requests.get(f'https://ess.api.cnyes.com/ess/api/v1/news/keyword?q={stock_name}&limit=5&page=1').json()

  # 依照格式擷取資料
  items=json_data['data']['items']
  for item in items:
      # 網址、標題和日期
      news_id = item["newsId"]
      title = item["title"]
      publish_at = item["publishAt"]
      # 使用 UTC 時間格式
      utc_time = dt.datetime.utcfromtimestamp(publish_at)
      formatted_date = utc_time.strftime('%Y-%m-%d')
      # 前往網址擷取內容
      url = requests.get(f'https://news.cnyes.com/'
                        f'news/id/{news_id}').content
      soup = BeautifulSoup(url, 'html.parser')
      p_elements=soup .find_all('p')
      # 提取段落内容
      p=''
      for paragraph in p_elements[4:]:
          p+=paragraph.get_text()
      data.append([stock_name, formatted_date ,title,p])
  return data