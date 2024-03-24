from pathlib import Path
from database import loadDB

def getDictPeriode(annee):
    # liste avec les matieres de chaque periode
    liste = []
    for i in range(1, 5):
        nameToDb = {}
        nom = "static/listeMatieres/"+ str(annee) + "/" + str(i)+".txt"
        nom_path = Path(nom)
        if not nom_path.exists():
            continue
        with open(nom, "r") as f:
            for line in f:
                (key, val) = line.split(":")
                val = val[:-1] if val[-1] == "\n" else val
                # remove space at the beginning of val
                val = val[1:] if val[0] == " " else val
                nameToDb[key] = val
        f.close()
        liste.append(nameToDb)
    return liste

def getDictAll():
    liste = []
    for i in range (3, 6):
        liste.append(getDictPeriode(i))
    return liste

def getReverseDictMat():
    nameToDb = {}
    for i in range(3, 6):
        for j in range(1, 5):
            nom = "static/listeMatieres/"+ str(i) + "/" + str(j)+".txt"
            nom_path = Path(nom)
            if not nom_path.exists():
                continue
            with open(nom, "r") as f:
                for line in f:
                    (val, key) = line.split(":")
                    key = key[:-1] if key[-1] == "\n" else key
                    # remove space at the beginning of val
                    key = key[1:] if key[0] == " " else key
                    nameToDb[key] = val
            f.close()
    return nameToDb

def listeMatAnnees():
    matieres = []
    # créé une liste pour chaque période de chaque année dans static
    for i in range(3, 6):
        mat = getDictPeriode(i)
        matieres.append(mat)
    return matieres

def listeAnnPerMatActives():
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT MIN(annee), MIN(periode), matiere FROM Documents GROUP BY matiere"
    mycursor.execute(sql)
    matieresActives = mycursor.fetchall()
    db.close()
    return matieresActives

def listeAnneesActives(matieresActives):
    anneesActives = []
    for matiere in matieresActives:
        if matiere[0] not in anneesActives and matiere[0] != 6:
            anneesActives.append(matiere[0])
    anneesActives.sort()
    return anneesActives

def listePeriodesActives(annee, listeMatActives):
    periodesActives = []
    for matiere in listeMatActives:
        if matiere[0] == annee and matiere[1] not in periodesActives:
            periodesActives.append(matiere[1])
    periodesActives.sort()
    return periodesActives

def listeMatActives(annee, periode, listeMatActives):
    matieresActives = []
    for matiere in listeMatActives:
        if matiere[0] == annee and matiere[1] == periode:
            matieresActives.append(matiere[2])
    matieresActives.sort()
    return matieresActives

def getDictMatieresActives():
    dictMatieres = {}
    annPerMat = listeAnnPerMatActives()
    anneesActives = listeAnneesActives(annPerMat)

    for annee in anneesActives:
        periodesActives = listePeriodesActives(annee, annPerMat)
        dictMatieres[annee] = {}
        for periode in periodesActives:
            matieresActives = listeMatActives(annee, periode, annPerMat)
            dictMatieres[annee][periode] = matieresActives
    return dictMatieres