import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to push server")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.on("notification")
def receive_notification(data):
    print(f"[PUSH RECEIVED] {data['message']} ({data['time']})")


if __name__ == "__main__":
    sio.connect("http://127.0.0.1:5001")
    sio.wait()
