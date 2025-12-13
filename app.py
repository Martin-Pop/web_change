from flask import Flask, render_template, request, redirect, url_for
from backend.db_access import DatabaseAccess, get_db_structure

app = Flask(__name__)
db = DatabaseAccess("monitor.db")
db.execute(get_db_structure())


@app.route('/')
def dashboard():
    all_endpoints = db.fetch_all("SELECT * FROM endpoints ORDER BY id DESC")
    return render_template('index.html', endpoints=all_endpoints)


@app.route('/add_endpoint', methods=['POST'])
def add_endpoint():
    url_to_add = request.form.get('url_input')

    if url_to_add:
        db.execute("INSERT INTO endpoints (url) VALUES (?)", (url_to_add,))
    return redirect(url_for('dashboard'))


@app.route('/delete_endpoint/<int:endpoint_id>', methods=['POST'])
def delete_endpoint(endpoint_id):
    db.execute("DELETE FROM endpoints WHERE id = ?", (endpoint_id,))

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)