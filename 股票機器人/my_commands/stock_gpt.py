import openai
from replit import db
from my_commands.stock_price import stock_price
from my_commands.stock_news import stock_news
from my_commands.stock_value import stock_fundamental

# 建立 GPT 3.5-16k 模型
def get_reply(messages):
  try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
  except openai.OpenAIError as err:
    reply = f"發生 {err.error.type} 錯誤\n{err.error.message}"
  return reply

# 建立訊息指令(Prompt)
def generate_content_msg(stock_id):

    stock_name = db[stock_id]["stock_name"] if stock_id != "大盤" else stock_id

    price_data = stock_price(stock_id)
    news_data = stock_news(stock_name)

    content_msg = '你現在是一位專業的證券分析師, \
      你會依據以下資料來進行分析並給出一份完整的分析報告:\n'

    content_msg += f'近期價格資訊:\n {price_data}\n'

    if stock_id != "大盤":
        stock_value_data = stock_fundamental(stock_id)
        content_msg += f'每季營收資訊：\n {stock_value_data}\n'

    content_msg += f'近期新聞資訊: \n {news_data}\n'
    content_msg += f'請給我{stock_name}近期的趨勢報告,請以詳細、\
      嚴謹及專業的角度撰寫此報告,並提及重要的數字, reply in 繁體中文'

    return content_msg

# StockGPT
def stock_gpt(stock_id):
    content_msg = generate_content_msg(stock_id)

    msg = [{
        "role": "system",
        "content": "你現在是一位專業的證券分析師, 你會統整近期的股價\
      、基本面、新聞資訊等方面並進行分析, 然後生成一份專業的趨勢分析報告"
    }, {
        "role": "user",
        "content": content_msg
    }]

    reply_data = get_reply(msg)

    return reply_data

