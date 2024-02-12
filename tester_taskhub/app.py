# tester home page
from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route("/")
def index():
    '''
    this is what happens in the home page
    '''
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)