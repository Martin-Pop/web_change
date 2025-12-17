from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room
from dotenv import load_dotenv
import os, datetime
from backend.monitoring import EndpointMonitor
from backend.websocket_client import WebsocketClient

load_dotenv()

WS_CONNECT_ENDPOINT = "wss://localhost:7076/ws/connect"

app = Flask(__name__)
socketio = SocketIO(app)
ws_client = WebsocketClient(WS_CONNECT_ENDPOINT, os.getenv("WS_TOKEN"))
ws_client.start()

def notify_stat_update(endpoint_id, new_data):
    socketio.emit('new_stat', new_data, room=f"stats_{endpoint_id}")

monitor = EndpointMonitor(ws_client, notify_stat_update)

@socketio.on('join')
def on_join(data):
    room = f"stats_{data['endpoint_id']}"
    join_room(room)

#routes
@app.route('/')
def dashboard():
    all_endpoints = monitor.get_all_endpoints()
    return render_template('index.html', endpoints=all_endpoints)

@app.route('/add_endpoint', methods=['POST'])
def add_endpoint():
    url_to_add = request.form.get('url_input')
    interval = request.form.get("time_interval", type=int)

    if url_to_add:
        monitor.add_to_monitor(url_to_add, interval)
    return redirect(url_for('dashboard'))


@app.route('/delete_endpoint/<int:endpoint_id>', methods=['POST'])
def delete_endpoint(endpoint_id):
    monitor.remove_from_monitor(endpoint_id)

    return redirect(url_for('dashboard'))


@app.route('/update_interval/<int:endpoint_id>', methods=['POST'])
def update_interval(endpoint_id):
    data = request.get_json()
    new_interval = data.get('time_interval')

    if not new_interval:
        return jsonify({"error": "No interval provided"}), 400

    monitor.update_check_interval(endpoint_id, new_interval)

    return jsonify({"success": True, "new_interval": new_interval})

@app.route('/stats/<int:endpoint_id>', methods=['GET'])
def stats(endpoint_id):

    statistics = monitor.get_statistics(endpoint_id)
    return render_template('stats.html', statistics=statistics, endpoint_id=endpoint_id)

#filter
@app.template_filter('format_datetime')
def format_datetime(value):
    return datetime.datetime.fromtimestamp(value).strftime('%d.%m.%Y %H:%M')

if __name__ == '__main__':
    monitor.start()

    #app.run(debug=True, use_reloader=False)
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
