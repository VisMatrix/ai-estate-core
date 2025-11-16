from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# 之后会用环境变量配置号码，在 Render 上设置
TWILIO_CA = os.environ.get("TWILIO_CA_NUMBER", "+16479059805")
TWILIO_US = os.environ.get("TWILIO_US_NUMBER", "+13322622322")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK", "https://example.com")

@app.route("/voice", methods=["POST"])
def voice():
# 🔔 Twilio 来电入口：欢迎语 + 采集语言（暂时不用 MiniMax）

resp = VoiceResponse()

# 欢迎语
resp.say(
"您好，这里是 VisMatrix AI 房产助手。 "
"我会记录您想看的区域和预算，稍后通过微信或短信给您推荐房源。",
language="zh-CN"
)

# 收集用户语音
gather = Gather(
input="speech",
action="/handle-speech",
method="POST",
speech_timeout="auto",
language="zh-CN",
)
resp.append(gather)

return str(resp)
