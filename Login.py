from flask import Flask, render_template

app = Flask(__name__)


@app.post('/')
def index():
    return render_template('test.html')