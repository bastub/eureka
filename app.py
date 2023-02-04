from flask import Flask, url_for, render_template, redirect, request
from recherchePDF import recherchePDF

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def menu():
    tag = request.form['search']
    listeDocu = recherchePDF(tag)
    return render_template("menu.html", listeDocu = listeDocu)

if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=80,debug=True)