from flask import Flask, render_template, request
import json


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8088)
