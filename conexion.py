import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # Si tu MySQL tiene clave, cámbiala aquí
        database="servicios_db"
    )
