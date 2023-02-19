from flask import Flask, url_for, render_template, redirect, request
from recherchePDF import recherchePDF, afficheTout, uploadDB
from os import getenv
from dotenv import load_dotenv
from fetchPeriode import getDictPeriode


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def recherche():
    nameToDb = {}
    with open("nameToDb.txt", "r") as f:
        for line in f:
            (key, val) = line.split(":")
            val = val[:-1] if val[-1] == "\n" else val
            # remove space at the beginning of val
            val = val[1:] if val[0] == " " else val
            val.encode("utf-8")
            nameToDb[key] = val
    f.close()
    tag = request.form['search']
    listeDocu = recherchePDF(tag)
    if tag is None or tag == "":
        listeDocu = afficheTout()
    return render_template("menu.html", listeDocu = listeDocu, listeMatieres = nameToDb)

@app.route("/recherche")
def rechercheMenu():
    nameToDb = {}
    with open("nameToDb.txt", "r") as f:
        for line in f:
            (key, val) = line.split(":")
            val = val[:-1] if val[-1] == "\n" else val
            # remove space at the beginning of val
            val = val[1:] if val[0] == " " else val
            val.encode("utf-8")
            nameToDb[key] = val
    f.close()
    matiere = request.args.get('matiere')
    if matiere:
        # perform search with filter
        listeDocu = recherchePDF(matiere)
    else:
        # perform search without filter
        listeDocu = recherchePDF('')
    return render_template("menu.html", listeDocu=listeDocu, listeMatieres=nameToDb)


@app.route("/search")
def tout():
    nameToDb = {}
    with open("nameToDb.txt", "r") as f:
        for line in f:
            (key, val) = line.split(":")
            val = val[:-1] if val[-1] == "\n" else val
            # remove space at the beginning of val
            val = val[1:] if val[0] == " " else val
            nameToDb[key] = val
    f.close()
    listeDocu = afficheTout()
    return render_template("menu.html", listeDocu = listeDocu, listeMatieres = nameToDb)


@app.route("/upload", methods=['GET'])
def getUpload():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def uploadPost():
    # passw = request.form['password']
    # load_dotenv()
    # if passw != getenv("password_db"):
    #     return redirect(url_for('getUpload'))
    file = request.files['file']
    auteur = request.form['auteur']
    tags = request.form['tags']
    description = request.form['description']
    uploadDB(file, auteur, tags, description)
    return redirect(url_for('index'))

@app.route("/annee", methods=['GET'])
def annee():
    annee = request.args.get('annee')
    # Get the list of dictionaries with subjects for each period
    listeMatieres = getDictPeriode(annee)
    # liste docu = liste des documents retournés par la recherche avec les clés de nameToDb
    liste = []
    # get all the values of the keys for all periods
    for dictMatieres in listeMatieres:
        for key, value in dictMatieres.items():
            listeDocu = recherchePDF(value)
            liste.append(listeDocu)
    # merge all the lists in one
    liste = [item for sublist in liste for item in sublist]
    return render_template("menuannee.html", listeDocu=liste, listeMatieres=listeMatieres)


if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=80,debug=True)