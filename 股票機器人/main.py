from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, 
    TextMessage, 
    TextSendMessage)
import os
import my_commands.database 
from my_commands.stock_gpt import stock_gpt, get_reply


api = LineBotApi(os.getenv('LINE_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_SECRET'))

app = Flask(__name__)

@app.post("/")
def callback():
    # 取得 X-Line-Signature 表頭電子簽章內容
    signature = request.headers['X-Line-Signature']

    # 以文字形式取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 比對電子簽章並處理請求內容
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("電子簽章錯誤, 請檢查密鑰是否正確？")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 檢測是否為4位數的股票代碼或「大盤」訊息
    if (len(user_message) == 4 and user_message.isdigit()) or user_message == '大盤':
        reply_text = stock_gpt(user_message)
    # 一般訊息
    else:
        msg = [  {"role": "system",
                  "content":"reply in 繁體中文"
              }, {"role": "user",
                  "content":user_message}]
        reply_text = get_reply(msg)
      
    api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))
      
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

