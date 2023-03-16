import mysql.connector
from dotenv import load_dotenv
from os import getenv, path, remove, rename
load_dotenv()

def loadDB():
    db = mysql.connector.connect(
        host = getenv("host_db"),
        user = getenv("user_db"),
        password = getenv("password_db"),
        database = "eureka"
    )
    return db

def rechercheParTag(tag):
    db = loadDB()
    mycursor = db.cursor()
    tag = "%" + tag + "%"
    sql = "SELECT titre, auteur, id_doc, description FROM Documents WHERE id_doc IN (SELECT id_doc FROM Referencement WHERE id_tag IN (SELECT id_tag FROM Tags WHERE nom like %s))"
    val = (tag,)

    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    db.close()

    return myresult

def rechercheParMatiere(matiere):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT titre, auteur, id_doc, description FROM Documents WHERE matiere = %s))"
    val = (matiere,)

    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    db.close()

    return myresult

def rechercheParAnnee(annee):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT titre, auteur, id_doc, description FROM Documents WHERE annee = %s))"
    val = (annee,)

    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    db.close()

    return myresult

def rechercheParMatiereEtAnnee(matiere, annee):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT titre, auteur, id_doc, description FROM Documents WHERE annee = %s AND matiere = %s))"
    val = (annee, matiere,)

    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    db.close()

    return myresult

def rechercheListePDF(listeTags, annee="", matiere=""):
    db = loadDB()
    mycursor = db.cursor()
    listeResult = []
    
    for tag in listeTags:
        sql = "SELECT titre, auteur, id_doc, description FROM Documents WHERE id_doc IN (SELECT id_doc FROM Referencement WHERE id_tag = (SELECT id_tag FROM Tags WHERE nom like %s))"
        val = (tag,)

        if annee != "":
            sql += " AND id_doc IN (SELECT id_doc FROM Referencement WHERE id_tag = (SELECT id_tag FROM Tags WHERE nom like %s))"
            val += (annee,)

        if matiere != "":
            sql += " AND id_doc IN (SELECT id_doc FROM Referencement WHERE id_tag = (SELECT id_tag FROM Tags WHERE nom like %s))"
            val += (matiere,)

        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        listeResult.append(myresult)

    db.close()

    return listeResult

def afficheTout():
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT titre, auteur, id_doc, description FROM Documents" 
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    db.close()

    return myresult

def isPDF(file):
    if not file.filename.endswith(".pdf"):
        return False
    # check if the content of the file is a pdf and not a fake pdf
    # TODO
    return True

def uploadDB(file, auteur, tags, description, annee, type_doc, matiere = ""):
    # if not isPDF(file):
    #     return False
    db = loadDB()
    tags = tags.split(";")
    tags = [tag.strip() for tag in tags]
    titre = file.filename.replace("_", " ")
    titre = titre.replace(".pdf", "")

    tags.append(titre)
    tags.append(annee)
    tags.append(type_doc)
    tags.append(matiere) if matiere != "" else None
    # put the file into the server folder "static/pdf"
    file.save("static/pdf/" + titre + ".pdf")

    tags = [tag.lower() for tag in tags]
    tags = list(dict.fromkeys(tags))
    tags = [tag for tag in tags if tag != ""]

    mycursor = db.cursor()

    sql = "INSERT INTO Documents (titre, auteur, description) VALUES (%s, %s, %s)"
    val = (titre, auteur, description)

    mycursor.execute(sql, val)

    db.commit()

    for tag in tags:
        # check if tag in database else create it
        sql = "SELECT id_tag FROM Tags WHERE nom = %s"
        val = (tag,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            sql = "INSERT INTO Tags (nom) VALUES (%s)"
            val = (tag,)
            mycursor.execute(sql, val)
            db.commit()

        sql = "SELECT id_doc FROM Documents WHERE titre = %s ORDER BY id_doc DESC LIMIT 1"
        val = (titre,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        id_doc = myresult[0][0]

        sql = "INSERT INTO Referencement (id_doc, id_tag) VALUES (%s, (SELECT id_tag FROM Tags WHERE nom = %s))"
        val = (id_doc, tag)

        mycursor.execute(sql, val)

    db.commit()
    db.close()

def supprimePDF(titre, auteur, description):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT id_doc FROM Documents WHERE titre = %s AND auteur = %s AND description = %s"
    val = (titre, auteur, description,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    id_doc = myresult[0][0]

    # delete from Referencement
    sql = "DELETE FROM Referencement WHERE id_doc = %s"
    val = (id_doc,)
    mycursor.execute(sql, val)

    # delete from Documents
    sql = "DELETE FROM Documents WHERE id_doc = %s"
    val = (id_doc,)
    mycursor.execute(sql, val)

    db.commit()

    # Closing the connection
    db.close()

    
    if path.exists("/static/pdf/" + titre + ".pdf"):
        remove(titre + ".pdf")

def getInfos(titre, auteur, description):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT id_doc FROM Documents WHERE titre = %s AND auteur = %s AND description = %s"
    val = (titre, auteur, description,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    id_doc = myresult[0][0]

    sql = "SELECT nom FROM Tags WHERE id_tag IN (SELECT id_tag FROM Referencement WHERE id_doc = %s)"
    val = (id_doc,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    tags = [tag[0] for tag in myresult]

    db.close()

    return tags

def modifiePDF(titre, auteur, description, newTitre, newAuteur, newDescription, newTags, annee, type_doc, matiere):
    db = loadDB()
    mycursor = db.cursor()
    sql = "SELECT id_doc FROM Documents WHERE titre = %s AND auteur = %s AND description = %s"
    val = (titre, auteur, description,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    id_doc = myresult[0][0]

    # modifie Documents
    sql = "UPDATE Documents SET titre = %s, auteur = %s, description = %s WHERE id_doc = %s"
    val = (newTitre, newAuteur, newDescription, id_doc,)

    mycursor.execute(sql, val)

    db.commit()

    newTags = newTags.split(";")
    newTags = [tag.strip() for tag in newTags]
    newTags.append(titre)
    newTags.append(annee)
    newTags.append(type_doc)
    newTags.append(matiere) if matiere != "" else None
    newTags = [tag.lower() for tag in newTags]
    newTags = list(dict.fromkeys(newTags))
    newTags = [tag for tag in newTags if tag != ""]

    # modifie Referencement
    sql = "DELETE FROM Referencement WHERE id_doc = %s"
    val = (id_doc,)

    mycursor.execute(sql, val)

    db.commit()
    
    for tag in newTags:
        # check if tag in database else create it
        sql = "SELECT id_tag FROM Tags WHERE nom = %s"
        val = (tag,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            sql = "INSERT INTO Tags (nom) VALUES (%s)"
            val = (tag,)
            mycursor.execute(sql, val)
            db.commit()

        sql = "INSERT INTO Referencement (id_doc, id_tag) VALUES (%s, (SELECT id_tag FROM Tags WHERE nom = %s))"
        val = (id_doc, tag,)

        mycursor.execute(sql, val)
       

    src = "static/pdf/" + titre + ".pdf"
    dst = "static/pdf/" + newTitre + ".pdf"

    rename(src, dst)
    
    db.commit()
    db.close()