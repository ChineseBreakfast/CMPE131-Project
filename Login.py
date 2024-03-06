from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def test():
    return "<html> <body> <h1> you made it  </h1> </body> </html>"