from flask import Flask, url_for, render_template, redirect, request
from recherchePDF import recherchePDF

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def menu():
    nameToDb = {}
    with open("nameToDb.txt", "r") as f:
        for line in f:
            (key, val) = line.split(":")
            val = val[:-1] if val[-1] == "\n" else val
            # remove space at the beginning of val
            val = val[1:] if val[0] == " " else val
            nameToDb[key] = val
    tag = request.form['search']
    listeDocu = recherchePDF(tag)
    return render_template("menu.html", listeDocu = listeDocu, listeMatieres = nameToDb)

if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=80,debug=True)