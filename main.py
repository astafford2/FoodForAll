
from flask import Flask, render_template, request, redirect, url_for
from bankFood import *
from FoodBankFinder_v1 import *


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


@app.route('/foodBank', methods=['GET', 'POST'])
def findFoodBank():
    if request.method == 'POST':
        address = request.form['addr']
        city = request.form['city']
        state = request.form['stateCode']
        zipcode = request.form['zip']

        origin = address + " " + city + " " + state + " " + zipcode

        bankNames = []
        bankAddrs = []
        bankNums = []
        bankDescs = []
        bankDists = []
        bankTimes = []

        bankNames, bankAddrs, bankNums, bankDescs, bankDists, bankTimes = closestBanks(origin)

        return redirect(url_for('foodBankNeeds', len=len(bankNames), bankNames=bankNames, destinations=bankAddrs, bankNums=bankNums, bankDescs=bankDescs, bankTimes=bankTimes, bankDists=bankDists))

    return render_template('foodbank.html')


@app.route('/companyLogin')
def companyLogin():
    return render_template('companylogin.html')


@app.route('/companyFeatures', methods=['GET', 'POST'])
def companyFeatures():
    if request.method == 'POST':
        formName = request.form['formName']

        if formName == 'INPUT':
            bankName = request.form['bankName']
            foodType = request.form['foodType']
            foodDesc = request.form['foodDesc']
            quantity = request.form['quantity']

            storeFoodItem(bankName, foodType, foodDesc, quantity)
        elif formName == 'REMOVE':
            bankName = request.form['bankName']
            foodDesc = request.form['foodDesc']
            quantity = request.form['quantity']

            removeFoodItem(bankName, foodDesc, quantity)

        return redirect(url_for('companyFeatures'))
    else:
        return render_template('companyFeatures.html')


@app.route('/foodBankNeeds', methods=['GET', 'POST'])
def foodBankNeeds():
    if request.method == 'POST':
        bank = request.form['bankName']
        
        neededItems = fetchFoodNeeded(bank)
        storedItems = fetchFoodByBank(bank)

        return render_template('needsandhaves.html', neededItems=neededItems, storedItems=storedItems)

    else:
        length = int(request.args.get("len"))
        bankNames = request.args.getlist("bankNames")
        destinations = request.args.getlist("destinations")
        bankNums = request.args.getlist("bankNums")
        bankDescs = request.args.getlist("bankDescs")
        bankTimes = request.args.getlist("bankTimes")
        bankDists = request.args.getlist("bankDists")

        return render_template('foodbankneeds.html',  length=length, bankNames=bankNames, destinations=destinations, bankNums=bankNums, bankDescs=bankDescs, bankTimes=bankTimes, bankDists=bankDists)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
