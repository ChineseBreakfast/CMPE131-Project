from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/help')
def test():
    return "render_template('test.html')"

@app.route('/', methods=['get','post'])
def test():
    return "render_template('test.html')"