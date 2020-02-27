
import pyodbc
import sqlite3
import csv
import datetime
from ftplib import FTP, FTP_TLS
import os
import sky_bits_api_parse


def all_vista_equipment():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.16.2.30;DATABASE=ViewpointTest;UID=powerbi;PWD=p0W3rB!D4t4')
    cursor = conn.cursor()
    data = cursor.execute("aec.spEMEquipment")
    vista_vehicle_data = data.fetchall()
    return vista_vehicle_data


def all_vista_operators():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.16.2.30;DATABASE=ViewpointTest;UID=powerbi;PWD=p0W3rB!D4t4')
    cursor = conn.cursor()
    data = cursor.execute("aec.spEMOperator")
    vista_operator_data = data.fetchall()
    return vista_operator_data


def import_to_ftp(file_name):
    with FTP_TLS("ftp.cloud.viewpoint.com") as ftps:
        ftps.login("945", "QnHS6468")
        ftps.prot_p()
        ftps.cwd(r"\imports\EM\SkyBitzMtr")
        local_path = r"C:\Users\jjacinto\OneDrive - HSI\Documents\GitHub\Skybitz_Vista"
        local_file = os.path.join(local_path, file_name)
        with open(local_file, "rb") as csv_file:
            ftps.storlines("Stor " + file_name, csv_file)
        ftps.dir()



