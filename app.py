from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# 环境变量（之后在 Render 上配置）
TWILIO_CA = os.environ.get("TWILIO_CA_NUMBER", "+16479059805")
TWILIO_US = os.environ.get("TWILIO_US_NUMBER", "+13322622322")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK", "https://example.com")


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()

    # 欢迎语
    resp.say(
        "您好，这里是 VisMatrix AI 房产助手。",
        language="zh-CN",
    )
    resp.say(
        "我会记录您感兴趣的区域和预算，稍后通过微信或短信给您推荐房源。",
        language="zh-CN",
    )

    # 收集用户语音
    gather = Gather(
        input="speech",
        action="/handle-speech",
        method="POST",
        speech_timeout="auto",
        language="zh-CN",
    )
    gather.say(
    "现在请您用一句话说出您想要的城市和预算，比如，多伦多一百万预算。",
    language="zh-CN",
    )
    resp.append(gather)

    return str(resp)


@app.route("/handle-speech", methods=["POST"])
def handle_speech():
# 暂时不接 AI，只把用户说的内容拿到，然后挂断
speech = request.form.get("SpeechResult", "").strip()
from_number = request.form.get("From", "")

print(f"来电号码: {from_number}")
print(f"用户语音: {speech}")

resp = VoiceResponse()

if not speech:
resp.say(
"不好意思，我没有听清楚，我们下次再联系。",
language="zh-CN",
)
resp.hangup()
return str(resp)

# TODO: 之后可以把 speech 和 from_number 发到 n8n / MiniMax 等外部服务
resp.say(
"好的，我已经记录下来，稍后会通过微信或短信联系您。",
language="zh-CN",
)
resp.hangup()
return str(resp)


@app.route("/", methods=["GET"])
def health_check():
return "OK"
