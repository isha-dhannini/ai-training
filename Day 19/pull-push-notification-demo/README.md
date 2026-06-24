# Pull vs Push Notification Architecture Demo

## Overview
This project explains and demonstrates two common notification delivery models used in distributed systems:

- **Pull architecture** – the client periodically asks the server for updates.
- **Push architecture** – the server actively sends updates to the client as soon as an event occurs.

The repository includes:
- a **theory section** with architecture explanation
- **advantages and disadvantages** of each model
- **working Python demos** for both pull and push notification systems
- **run instructions** and **sample outputs**

---

# 1) Problem Statement
Applications such as chat systems, order tracking platforms, support desks, and monitoring dashboards often need to notify users when something changes. There are two common approaches:

1. **Pull notifications** – the client checks repeatedly for new updates.
2. **Push notifications** – the server sends updates immediately to connected clients.

This project compares both approaches and demonstrates each with a practical implementation.

---

# 2) Pull Notification Architecture

## Definition
In a **pull model**, the **client initiates communication** and periodically asks the server whether any new notifications are available.

### Typical flow
1. The client sends an HTTP request such as `GET /notifications`.
2. The server returns any new notifications.
3. If there are no new notifications, the server returns an empty list.
4. The client waits for a fixed interval and polls again.

## Pull architecture diagram

```text
+---------+        Poll every few seconds        +---------+
| Client  | ----------------------------------> | Server  |
|         |      GET /notifications             |         |
|         | <---------------------------------- |         |
|         |   notifications / empty response    |         |
+---------+                                     +---------+
```

## Advantages of pull architecture
- Easy to implement using standard HTTP APIs
- No persistent connection is required
- Simple to test and debug
- Works well when real-time updates are not necessary

## Disadvantages of pull architecture
- Generates many unnecessary requests when nothing has changed
- Notification delivery depends on the polling interval
- Can waste network bandwidth and server resources
- Not ideal for highly interactive real-time systems

---

# 3) Push Notification Architecture

## Definition
In a **push model**, the **server initiates communication** and sends notifications to clients as soon as an event occurs.

### Typical flow
1. The client opens a persistent connection to the server.
2. The server keeps the connection open.
3. When an event occurs, the server immediately sends a notification to the connected client.
4. The client receives the update in real time.

## Push architecture diagram

```text
+---------+   Persistent connection (WebSocket)   +---------+
| Client  | <===================================> | Server  |
+---------+                                       +---------+
      ^                                                  |
      |                                                  |
      +------------ instant notification push ----------+
```

## Advantages of push architecture
- Very low latency and real-time delivery
- No repeated polling requests when there are no updates
- Better user experience for live systems
- Efficient for event-driven systems such as chat and alerts

## Disadvantages of push architecture
- More complex to implement and maintain
- Requires persistent connections or a push delivery mechanism
- Reconnection logic and offline handling need to be considered
- Scaling large numbers of concurrent clients can be harder

---

# 4) Pull vs Push Comparison

| Feature | Pull | Push |
|---|---|---|
| Who initiates communication? | Client | Server |
| Transport style | Repeated HTTP polling | Persistent connection / WebSocket |
| Delivery latency | Depends on poll interval | Near real-time |
| Complexity | Low | Medium to high |
| Network efficiency | Lower | Higher |
| Best use cases | Dashboards, periodic status checks | Chat, alerts, live updates |

---

# 5) Practical Demo Included in This Repository

## A. Pull demo
**Files**
- `pull_demo/pull_server.py`
- `pull_demo/pull_client.py`

**What it shows**
- A Flask server exposes:
  - `GET /notifications` → the client polls for updates
  - `POST /add` → manually adds a new notification
- A Python client polls the server every 5 seconds and prints any new notification

---

## B. Push demo
**Files**
- `push_demo/push_server.py`
- `push_demo/push_client.py`

**What it shows**
- A Flask-SocketIO server accepts WebSocket connections
- A Python client stays connected and listens for events
- `POST /trigger` sends a notification immediately to all connected clients

---

# 6) Project Structure

```text
pull-push-notification-demo/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── pull_demo/
│   ├── pull_server.py
│   └── pull_client.py
│
└── push_demo/
    ├── push_server.py
    └── push_client.py
```

---

# 7) Setup Instructions

## Step 1: Clone the repository
```bash
git clone <your-repo-url>
cd pull-push-notification-demo
```

## Step 2: Create a virtual environment

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

---

# 8) How to Run the Pull Demo

## Terminal 1 — Start the pull server
```bash
python pull_demo/pull_server.py
```

The server starts on:
```text
http://127.0.0.1:5000
```

## Terminal 2 — Start the pull client
```bash
python pull_demo/pull_client.py
```

The client polls every 5 seconds.

## Terminal 3 — Add a notification
### Option A: curl
```bash
curl -X POST http://127.0.0.1:5000/add -H "Content-Type: application/json" -d "{\"message\":\"Support ticket updated\"}"
```

### Option B: Python one-liner
```bash
python -c "import requests; print(requests.post('http://127.0.0.1:5000/add', json={'message':'Support ticket updated'}).json())"
```

## Expected pull output
```text
Polling for notifications every 5 seconds...

[NEW] 1 - Welcome! No new updates yet. (...)
No new notifications.
[NEW] 2 - Support ticket updated (...)
```

---

# 9) How to Run the Push Demo

## Terminal 1 — Start the push server
```bash
python push_demo/push_server.py
```

The server starts on:
```text
http://127.0.0.1:5001
```

## Terminal 2 — Start the push client
```bash
python push_demo/push_client.py
```

## Terminal 3 — Trigger a push notification
### Option A: curl
```bash
curl -X POST http://127.0.0.1:5001/trigger -H "Content-Type: application/json" -d "{\"message\":\"Your support ticket has been resolved\"}"
```

### Option B: Python one-liner
```bash
python -c "import requests; print(requests.post('http://127.0.0.1:5001/trigger', json={'message':'Your support ticket has been resolved'}).json())"
```

## Expected push output
```text
Connected to push server
[PUSH RECEIVED] Connected to push server (...)
[PUSH RECEIVED] Your support ticket has been resolved (...)
```

---

# 10) Internal Working of the Demos

## Pull demo internals
- The server stores notifications in a Python list.
- The client remembers the latest notification ID it has already seen.
- On every poll, the client sends `after_id=<last_seen_id>`.
- The server returns only notifications with a larger ID.

## Push demo internals
- The client opens a persistent WebSocket connection to the server.
- The server keeps the connection active.
- When `/trigger` is called, the server emits a `notification` event to all connected clients.
- The client receives the event instantly and prints it.

---

# 11) Notes on Polling vs Push
This project demonstrates **basic polling** and **WebSocket push**. In real systems, there are more variants:

## Polling
The client asks the server for updates every fixed interval.

## Long polling
The client sends a request, and the server holds the request open until new data is available or a timeout occurs.

## Server-Sent Events (SSE)
The server streams updates over a single HTTP connection from server to client.

## WebSockets
A full-duplex persistent connection that allows real-time two-way communication.

---

# 12) Suggested Screenshots for Submission
To make the GitHub submission stronger, capture screenshots of:

## Pull
1. pull server terminal running
2. pull client terminal polling
3. POST request to `/add`
4. pull client receiving the new notification

## Push
1. push server terminal running
2. push client connected
3. POST request to `/trigger`
4. push client receiving the notification instantly

You can add them in a `screenshots/` folder and reference them in this README.

---

# 13) Conclusion
Both pull and push architectures are useful for notification delivery, but they serve different needs.

- **Pull** is simpler and easier to implement, but it introduces delay and can waste resources due to repeated polling.
- **Push** is better for real-time systems because the server sends updates immediately, but it requires more sophisticated infrastructure and connection handling.

Therefore, the correct choice depends on the application's requirements for **latency**, **complexity**, **scale**, and **user experience**.
