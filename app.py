from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# 之后会用环境变量更灵活，这里先不强制依赖它们
TWILIO_CA = os.environ.get("TWILIO_CA_NUMBER")
TWILIO_US = os.environ.get("TWILIO_US_NUMBER")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK", "")


@app.route("/voice", methods=["POST"])
def voice():
"""Twilio 来电入口：欢迎语 + 录音（只做最简单的通了再说）"""
resp = VoiceResponse()

# 欢迎语
resp.say(
"您好，这里是 VisMatrix AI 房产助手。",
voice="woman",
language="zh-CN",
)

# 让用户说一句话
gather = Gather(
input="speech",
action="/handle-speech",
method="POST",
speech_timeout="auto",
language="zh-CN",
)
gather.say(
"请说您想看的区域和预算，比如：北约克，一百六十万。",
voice="woman",
language="zh-CN",
)
resp.append(gather)

# 如果没说话，就再问一次
resp.redirect("/voice")

return str(resp)


@app.route("/handle-speech", methods=["POST"])
def handle_speech():
"""接住用户说的话，先打印出来，再简单复述一遍"""
speech = request.form.get("SpeechResult", "").strip()
from_number = request.form.get("From", "")

# 打日志（以后可以接 n8n / Notion）
print(f"来电号码: {from_number}")
print(f"用户说: {speech}")

resp = VoiceResponse()

if not speech:
resp.say(
"不好意思，我没有听清楚，我们下次再联系。",
voice="woman",
language="zh-CN",
)
resp.hangup()
return str(resp)

# 简单复述一遍，证明线路打通
resp.say("好的，我听到您说：", voice="woman", language="zh-CN")
resp.say(speech, voice="woman", language="zh-CN")
resp.say(
"稍后我会为您匹配合适的房源，再联系您。",
voice="woman",
language="zh-CN",
)
resp.hangup()
return str(resp)


@app.route("/", methods=["GET"])
def health_check():
"""Render / 浏览器 打开根路径用"""
return "VisMatrix AI Estate Core is running."


if __name__ == "__main__":
# 本地跑的时候用，Render 会用 gunicorn 启动这行不会走到
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
