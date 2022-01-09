import json
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

from getstock import detail
app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('M/YXQ7eb1gQBh6LnTKg4l22aQh136wH8/UXxs77GFV57aZoJ6/j7CCd5UGP/hfpu6qVAAdR/Ot3dJBpKvf0IMA1HX30WlljA8B1YkMoi7ocBifkwJ10r09tY3v6MI4P3M4j84et5+Q0x9sU4PuaY7QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('21597241e1485661e1572270a5016e88')

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
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    if message_type == "text":
        message = event.message.text
        if ((message[0] == ".") & message[1:6].isdigit()):
                target = message[1:6]
                targetjson = detail(target)
                line_bot_api.reply_message(reply_token, FlexSendMessage('請輸入股票代號: ', targetjson))
        #if(message == "test"):
        #   Buttom = json.load(open('json/detail/selecttarget.json', 'r', encoding='utf-8'))
        #    line_bot_api.reply_message(reply_token, FlexSendMessage('請輸入股票代號: ', Buttom))
        


# Postback event
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    reply_token = event.reply_token
    if(data == 'target'): 
        target = event.postback.text
        targetjson = detail(target)
        line_bot_api.reply_message(reply_token, FlexSendMessage('result', targetjson))



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)