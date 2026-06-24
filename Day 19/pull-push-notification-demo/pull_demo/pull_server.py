from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Simple in-memory notification store for the demo.
notifications = [
    {
        "id": 1,
        "message": "Welcome! No new updates yet.",
        "time": str(datetime.now())
    }
]


@app.route("/notifications", methods=["GET"])
def get_notifications():
    """
    Pull endpoint:
    The client polls this route periodically to ask for new notifications.

    Query parameter:
    - after_id: return only notifications with id > after_id
    """
    after_id = request.args.get("after_id", default=0, type=int)
    new_items = [n for n in notifications if n["id"] > after_id]
    return jsonify(new_items)


@app.route("/add", methods=["POST"])
def add_notification():
    """
    Adds a new notification manually for testing.

    Example JSON body:
    {
        "message": "Support ticket updated"
    }
    """
    data = request.get_json(silent=True) or {}
    message = data.get("message", "New notification")

    new_id = notifications[-1]["id"] + 1 if notifications else 1
    notification = {
        "id": new_id,
        "message": message,
        "time": str(datetime.now())
    }
    notifications.append(notification)

    return jsonify({
        "status": "added",
        "notification": notification
    })


if __name__ == "__main__":
    print("Pull notification server running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
