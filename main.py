
from flask import Flask, render_template, request
from bankFood import *

app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutus.html')


@app.route('/contactUs')
def contactUs():
    return render_template('contactus.html')


@app.route('/foodBank')
def findFoodBank():
    return render_template('foodbank.html')


@app.route('/foodBankNeeds', methods=['GET', 'POST'])
def foodBankNeeds():
    if request.method == 'POST':
        bank = request.form['bankName']
        
        neededItems = fetchFoodNeeded(bank)
        storedItems = fetchFoodByBank(bank)

        return render_template('needsandhaves.html', neededItems=neededItems, storedItems=storedItems)

    else:
        return render_template('foodbankneeds.html')


@app.route('/needsAndHaves')
def needsAndHaves():
    # bank = input("Enter bank name: ")
    # neededItems = fetchFoodNeeded(bank)
    # storedItems = fetchFoodByBank(bank)

    return render_template('needsandhaves.html') # , neededItems=neededItems, storedItems=storedItems


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
