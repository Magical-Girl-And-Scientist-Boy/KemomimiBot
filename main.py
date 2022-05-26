# 必要モジュールの読み込み
from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 変数appにFlaskを代入。インスタンス化
app = Flask(__name__)

# 環境変数取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 定数
user_name = 'Ken_Cirくん'


# Herokuログイン接続確認のためのメソッド
# Herokuにログインすると「hello world」とブラウザに表示される
@app.route("/")
def hello_world():
    return "Hello World!"


# ユーザーからメッセージが送信された際、LINE Message APIからこちらのメソッドが呼び出される。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text in 'おはよう':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='おはよう！{0}'.format(user_name)))
    elif event.message.text in 'おやすみ':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='おやすみ〜{0}'.format(user_name)))
    elif event.message.text in '好き' or event.message.text in 'すき':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='私も好きだよ！{0}！'.format(user_name)))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録されていない単語だよ！'))


# ポート番号の設定
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
