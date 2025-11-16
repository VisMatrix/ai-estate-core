from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# 之后会用环境变量来配置号码，n8n 等
TWILIO_CA = os.environ.get("TWILIO_CA_NUMBER", "+16479059805") # 先写死，稍后可在环境变量里覆盖
TWILIO_US = os.environ.get("TWILIO_US_NUMBER", "+13322622322")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK", "https://example.com")


@app.route("/voice", methods=["POST"])
def voice():
"""
Twilio 来电入口：
先播放一段欢迎语，让客户开头说一句（暂时不用 MiniMax）
"""
resp = VoiceResponse()

# 欢迎语
resp.say(
"您好，这里是 VisMatrix AI 房产助手。",
voice="woman",
language="zh-CN"
)

# 收集一句语音，后面可以接 MiniMax
gather = Gather(
input="speech",
action="/handle-speech",
method="POST",
speech_timeout="auto",
language="zh-CN"
)
gather.say(
"请简单说一下您想看的区域和预算，比如：北约克，一百六十万。",
voice="woman",
language="zh-CN"
)
resp.append(gather)

# 如果用户不说话，就再回到 /voice
resp.redirect("/voice")

return str(resp)


@app.route("/handle-speech", methods=["POST"])
def handle_speech():
"""
暂时不接 AI，只是把用户说的话打印出来，然后挂断。
以后在这里接 MiniMax。
"""
speech = request.form.get("SpeechResult", "").strip()
from_number = request.form.get("From", "")

print(f"[来电号码] {from_number}")
print(f"[用户说] {speech}")

resp = VoiceResponse()

if not speech:
resp.say(
"不好意思，我没有听清楚，我们下次再联系。",
voice="woman",
language="zh-CN"
)
resp.hangup()
return str(resp)

# 暂时简单回复一句，证明链路打通
resp.say(
f"好的，我听到了：{speech}。 "
"稍后我会把房源发给您，有需要可以再联系我。",
voice="woman",
language="zh-CN"
)
resp.hangup()
return str(resp)


@app.route("/", methods=["GET"])
def health_check():
"""
用来检查服务是否正常运行：
将来 Render / Replit 部署后，可以在浏览器里开根路径看。
"""
return "VisMatrix AI Estate Core is running."


if __name__ == "__main__":
# 本地跑的时候用这个，部署到 Render 会用 gunicorn 启动
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
