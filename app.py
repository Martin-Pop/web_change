from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
import os
from backend.monitoring import EndpointMonitor
from backend.websocket_client import WebsocketClient

load_dotenv()

WS_CONNECT_ENDPOINT = "wss://localhost:7076/ws/connect"

app = Flask(__name__)
ws_client = WebsocketClient(WS_CONNECT_ENDPOINT, os.getenv("WS_TOKEN"))
ws_client.start()
monitor = EndpointMonitor(ws_client)

@app.route('/')
def dashboard():
    all_endpoints = monitor.get_all_endpoints()
    return render_template('index.html', endpoints=all_endpoints)


@app.route('/add_endpoint', methods=['POST'])
def add_endpoint():
    url_to_add = request.form.get('url_input')

    if url_to_add:
        monitor.add_to_monitor(url_to_add)
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


if __name__ == '__main__':
    monitor.start()

    app.run(debug=True, use_reloader=False)
