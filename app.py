
import crawler

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import time

#line token
channel_access_token = '{channel_access_token}'
channel_secret = '{channel_secret}'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

user_id = '{user_id}'

app = Flask(__name__)
line_bot_api.push_message(user_id, TextSendMessage(text="股票價格警示機器人啟動中..."))

alert_list = []

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature")
        abort(400)
    except Exception as e:
        app.logger.error("An error occurred while handling webhook body:")
        app.logger.error(str(e))
        return 'Error'

    app.logger.info("Webhook handled successfully")
    return 'OK'
    # line_bot_api.reply_message(event.reply_token,message)


def push_message(message):
    text_message = TextSendMessage(text=message)

    line_bot_api.push_message(user_id, text_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message = str(event.message.text)

    alert_list.append(message)

    for alert in alert_list:
        try:
            message = crawler.price_alert(alert)
            if message != "":
                alert_list.remove(alert)
                push_message(message)

            time.sleep(5)

        except:
            push_message("[" + alert + "] 不正確")
            alert_list.remove(alert)
        

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
