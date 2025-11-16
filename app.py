from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# 之后会用环境变量来配置号码、n8n 等
TWILIO_CA = os.environ.get("TWILIO_CA_NUMBER", "+16479059805") # 先写死，你之后在环境变量里改
TWILIO_US = os.environ.get("TWILIO_US_NUMBER", "+13322622322")


@app.route("/voice", methods=["POST"])
def voice():
"""
Twilio 来电的入口：
暂时只做一个简单欢迎语 + 让客户说一句话（不调用 MiniMax）
"""
resp = VoiceResponse()

# 欢迎语
resp.say(
"您好，这里是 VisMatrix AI 房地产助手。"
"现在是测试版本，如果您听到这句话，说明系统已经接通。",
language="zh-CN"
)

# 收集一段语音，后面可以接 MiniMax
gather = Gather(
input="speech",
action="/handle-speech",
method="POST",
speech_timeout="auto",
language="zh-CN"
)
gather.say(
"请简单说一下，您是想了解学区房、投资房，还是其他需求？",
language="zh-CN"
)
resp.append(gather)

# 如果用户不说话，重新回到 /voice
resp.redirect("/voice")

return str(resp)


@app.route("/handle-speech", methods=["POST"])
def handle_speech():
"""
暂时不接 AI，只是重复用户说的话，然后挂断。
以后会在这里接 MiniMax。
"""
speech = request.form.get("SpeechResult", "").strip()
from_number = request.form.get("From", "")

print(f"[来电号码] {from_number}")
print(f"[用户说] {speech}")

resp = VoiceResponse()

if not speech:
resp.say("不好意思，我没有听清楚。我们下次再联系。", language="zh-CN")
resp.hangup()
return str(resp)

# 暂时简单复述，证明链路打通
resp.say(
f"好的，我听到您说：{speech}。"
"后续我会为您整理几套房源，再联系您。",
language="zh-CN"
)
resp.hangup()
return str(resp)


@app.route("/", methods=["GET"])
def health_check():
"""
用来检查服务是否正常运行。
将来 Render / Replit 部署后，可以在浏览器打开根路径看。
"""
return "VisMatrix AI Estate Core is running."


if __name__ == "__main__":
# 本地跑的时候用，部署到 Render 会用别的启动方式
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
