from flask import Flask, request, jsonify

app = Flask(__name__)

last_signal = {
    "id": 0,
    "symbol": "",
    "action": "",
    "price": "",
    "time": ""
}


@app.route("/")
def home():
    return "YesFX Signal Server Running"


@app.route("/status")
def status():
    return jsonify({
        "server": "running"
    })


@app.route("/webhook", methods=["POST"])
def webhook():

    global last_signal

    data = request.get_json(force=True)

    print("Incoming Signal:")
    print(data)

    alert = str(data.get("alert", "")).lower()

    if alert == "buy_now":
        action = "BUY"
    elif alert == "sell_now":
        action = "SELL"
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid Alert"
        }), 400

    signal_id = data.get("id")

    if signal_id is None or signal_id == "":
        last_signal["id"] += 1
    else:
        last_signal["id"] = int(signal_id)

    last_signal["symbol"] = data.get("symbol", "XAUUSD")
    last_signal["action"] = action
    last_signal["price"] = data.get("price", "")
    last_signal["time"] = data.get("time", "")

    print("Stored Signal:")
    print(last_signal)

    return jsonify({
        "status": "ok",
        "signal": last_signal
    })


@app.route("/signal")
def signal():
    return jsonify(last_signal)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
