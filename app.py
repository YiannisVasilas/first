from flask import Flask, render_template, request
import json
import sqlite3
import requests

connection = sqlite3.connect('customers.sqlite3', check_same_thread=False)

c = connection.cursor()

app = Flask(__name__)

@app.route('/')
def hello_world():
    joke_json = requests.get('https://api.chucknorris.io/jokes/random')
    joke = json.loads(joke_json.text)
    city = request.args.get('city')
    if city == None:
        city = 'Athens'
    weather_json = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=8a4801f9135796e49e0d10f6fc9d955e&units=metric&lang=el')
    weather = json.loads(weather_json.text)
    return render_template('index.html', joke=joke, weather=weather)

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)


@app.route('/api/nomoi')
def nomoi_api():
    with open('nomoi.json', encoding='utf-8') as f:
        nomoi = sorted(json.load(f), key=lambda x : x['population'], reverse=True)
    return json.dumps(nomoi, ensure_ascii=False)

@app.route('/api/nomos/<id>')
def nomos_api(id):
    with open('nomoi.json', encoding='utf-8') as f:
        nomoi = json.load(f)
    nomos = [n for n in nomoi if n['id'] == int(id)][0]
    return json.dumps(nomos, ensure_ascii=False)
    

@app.route('/nomoi')
def nomoi():
    with open('nomoi.json', encoding='utf-8') as f:
        # nomoi = sorted(json.load(f), key=lambda x : x['population'], reverse=True)
        nomoi = json.load(f)
    query = request.args.get('query')
    if query:
        nomoi = [nomos for nomos in nomoi if query in nomos['capital'] or query in nomos['name']]
    return render_template("nomoi.html", nomoi=nomoi)


@app.route('/pelates')
def pelates():
    sql = "SELECT * FROM customers"
    c.execute(sql)
    pelates = c.fetchall()
    return render_template("pelates.html", pelates=pelates)

@app.route('/pelates/<page>')
def pelates_paged(page):
    sql = f"SELECT * FROM customers LIMIT 50 OFFSET {(int(page)-1) * 50}"
    c.execute(sql)
    pelates = c.fetchall()
    return render_template("pelates.html", pelates=pelates)

@app.route('/formexample',methods = ['POST', 'GET'])
def formexample():
    # query = request.args.get('query')
    query = request.form['query'] if request.method == 'POST' else request.args.get('query')
    return render_template("formexample.html", pelates=pelates, query=query)
    


if __name__ == '__main__':
    app.run(debug=True)