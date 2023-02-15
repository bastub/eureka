import mysql.connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def recherchePDF(tag):
    db = mysql.connector.connect(
        host = getenv("host_db"),
        user = getenv("user_db"),
        password = getenv("password_db"),
        database = "eureka"
    )

    mycursor = db.cursor()

    sql = "SELECT titre, auteur, id_doc FROM Documents WHERE id_doc IN (SELECT id_doc FROM Referencement WHERE id_tag = (SELECT id_tag FROM Tags WHERE nom like %s))"

    val = (tag,)

    mycursor.execute(sql, val)

    # Fetching all pdf
    myresult = mycursor.fetchall()

    # Closing the connection
    db.close()

    return myresult

def afficheTout():
    db = mysql.connector.connect(
        host = getenv("host_db"),
        user = getenv("user_db"),
        password = getenv("password_db"),
        database = "eureka"
    )

    mycursor = db.cursor()

    sql = "SELECT titre, auteur, id_doc FROM Documents"

    mycursor.execute(sql)

    # Fetching all pdf
    myresult = mycursor.fetchall()

    # Closing the connection
    db.close()

    return myresult

def uploadDB(file, auteur, tags, description):
    db = mysql.connector.connect(
        host = getenv("host_db"),
        user = getenv("user_db"),
        password = getenv("password_db"),
        database = "eureka"
    )
    tags = tags.split(";")
    tags = [tag.strip() for tag in tags]

    titre = file.filename.replace("_", " ")
    titre = titre.replace(".pdf", "")

    tags.append(titre)

    # put the file into the server folder "static/pdf"
    file.save("static/pdf/" + titre + ".pdf")

    cpt = getenv("cpt")

    mycursor = db.cursor()

    # use cpt as id value
    sql = "INSERT INTO Documents (titre, auteur, description) VALUES (%s, %s, %s)"
    val = (titre, auteur, description)

    mycursor.execute(sql, val)

    db.commit()

    id_doc = cpt

    for tag in tags:
        # check if tag in database else create it
        sql = "SELECT * FROM Tags WHERE nom = %s"
        val = (tag,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            sql = "INSERT INTO Tags (nom) VALUES (%s)"
            val = (tag,)
            mycursor.execute(sql, val)
            db.commit()

        sql = "SELECT id_doc FROM Documents WHERE titre = %s"
        val = (titre,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        id_doc = myresult[0][0]

        sql = "INSERT INTO Referencement (id_doc, id_tag) VALUES (%s, (SELECT id_tag FROM Tags WHERE nom = %s))"
        val = (id_doc, tag)

        mycursor.execute(sql, val)

    db.commit()

    # Closing the connection
    db.close()