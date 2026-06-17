from flask import Flask, request, jsonify

app = Flask(__name__)

last_signal = {
    "id": 0,
    "symbol": "",
    "action": ""
}


@app.route("/")
def home():
    return "YesFX Signal Server Running"


@app.route("/webhook", methods=["POST"])
def webhook():

    global last_signal

    data = request.get_json(force=True)

    alert = data.get("alert", "").lower()

    if alert == "buy_now":
        action = "BUY"
    elif alert == "sell_now":
        action = "SELL"
    else:
        return jsonify({"status":"invalid alert"})

    last_signal["id"] += 1
    last_signal["symbol"] = "XAUUSD"
    last_signal["action"] = action

    print(last_signal)

    return jsonify({
        "status":"ok",
        "signal":last_signal
    })


@app.route("/signal")
def signal():
    return jsonify(last_signal)


@app.route("/status")
def status():
    return jsonify({
        "server":"running"
    })


if name == "__main__":
    app.run(host="0.0.0.0", port=5000)
