import json
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from getstock import scrape
#一直沒辦法從heroku放到line develop 一直沒辦法verify
app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('s90CJRc8v3/yE9n21sa7s7n8lX+oR+wEHsQavhLtAsqqP48urI25HSN6GJn0H+AevjX6X6fMnl7nWeX1I3hmTFYEU0FpqGtGkLab1cp8YaCMegX9tnNrsjJnL4w9+TuEmbwg1jQ6q0MLHhq0WDbJkgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e67c72abd96e846c3a4ebbdd3a2725d0')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
# Message event
@handler.add(MessageEvent)
def handle_message(event):
    """message_type = event.message.type
    user_id = event.source.user_id"""
    reply_token = event.reply_token
    message = event.message.text
    line_bot_api.reply_message(reply_token,TextSendMessage(text=message))
    """
    if message_type == "text":
        message = event.message.text
        if ((message[0] == ".") & message[1:6].isdigit()):
                target = message[1:6]
                targetjson = scrape(target)
                line_bot_api.reply_message(reply_token, FlexSendMessage('請輸入股票代號: ', targetjson))
        #if(message == "test"):
        #    Buttom = json.load(open('json/detail/selecttarget.json', 'r', encoding='utf-8'))
        #    line_bot_api.reply_message(reply_token, FlexSendMessage('請輸入股票代號: ', Buttom))
        
# Postback event
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    reply_token = event.reply_token
    if(data == 'target'): 
        target = event.postback.text
        targetjson = scrape(target)
        line_bot_api.reply_message(reply_token, FlexSendMessage('result', targetjson))

    """
import os
if __name__ == "__main__":
    app.run()