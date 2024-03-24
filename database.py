from os import getenv
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def loadDB():
    db = mysql.connector.connect(
        host = getenv("host_db"),
        user = getenv("user_db"),
        password = getenv("password_db"),
        database = "eureka"
    )
    return db