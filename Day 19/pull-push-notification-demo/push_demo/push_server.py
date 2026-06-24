from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"

# WebSocket server for push notifications.
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return "Push notification server is running"


@app.route("/trigger", methods=["POST"])
def trigger_notification():
    """
    Sends a push notification to all connected clients.

    Example JSON body:
    {
        "message": "Your support ticket has been resolved"
    }
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "New push notification")

    payload = {
        "message": message,
        "time": str(datetime.now())
    }

    socketio.emit("notification", payload)

    return jsonify({
        "status": "sent",
        "payload": payload
    })


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("notification", {
        "message": "Connected to push server",
        "time": str(datetime.now())
    })


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    print("Push notification server running at http://127.0.0.1:5001")
    socketio.run(app, debug=True, port=5001)
