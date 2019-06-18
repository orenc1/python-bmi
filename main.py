from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result_dict = request.form
        height = result_dict['height']
        weight = result_dict['weight']
        try:
            height = float(height)/100
            weight = float(weight)
        except Exception as ex:
            return render_template('error.html')                           
        bmi = weight / height**2
        return render_template('result.html', bmi=round(bmi, 2))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8088)
