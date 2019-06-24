from flask import Flask, render_template, request
from datetime import datetime
import json, sqlite3


class DBWrapper:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute(self, sql_cmd, values):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        if values:
            cur.execute(sql_cmd, values)
        else:
            cur.execute(sql_cmd)
        conn.commit()
        conn.close()

    def init(self):
        self.execute("CREATE TABLE IF NOT EXISTS users_info (timestamp DATETIME, client_ip TEXT, Height TEXT, Weight TEXT)",None)

    def insert(self, current_time, client_ip, height, weight):
        self.execute("INSERT INTO users_info VALUES(?,?,?,?)",(current_time, client_ip, height, weight))

    def view(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users_info')
        rows = cur.fetchall()
        conn.close()
        return rows


app = Flask(__name__)


def is_number(num):
    try:
        float(num)
    except ValueError:
        return False
    else:
        return True


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result_dict = request.form
        height = result_dict['height']
        weight = result_dict['weight']

        db = app.config.get('db_wrapper')
        db.insert(datetime.now(), request.remote_addr, height, weight)

        illegal_values_list = []
        if not is_number(height) or float(height) > 220 or float(height) < 40:
            illegal_values_list.append('height')
        if not is_number(weight) or float(weight) > 200 or float(weight) < 3:
            illegal_values_list.append('weight')
        if len(illegal_values_list) > 0:
            return render_template('error.html', errors=json.dumps(illegal_values_list))
        try:
            height = float(height)/100
            weight = float(weight)
        except Exception as ex:
            return render_template('error.html')                           
        bmi = weight / height**2
        return render_template('result.html', bmi=round(bmi, 2))

    return


@app.route('/stats')
def stats():
    db = app.config.get('db_wrapper')
    rows = db.view()
    return str(rows)


if __name__ == "__main__":
    db_wrapper = DBWrapper('bmi_db.db')
    db_wrapper.init()
    app.config['db_wrapper'] = db_wrapper
    app.run(debug=True, host='0.0.0.0', port=8088)
