import threading

from flask import Flask, render_template, request, redirect, url_for, jsonify
from backend.monitoring import EndpointMonitor

app = Flask(__name__)
monitor = EndpointMonitor()

def start_background_monitor():
    monitor.run()

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

    #print('updating interval')
    monitor.update_check_interval(endpoint_id, new_interval)

    return jsonify({"success": True, "new_interval": new_interval})


if __name__ == '__main__':
    monitor_thread = threading.Thread(target=start_background_monitor, daemon=True)
    monitor_thread.start()

    app.run(debug=True, use_reloader=False)
