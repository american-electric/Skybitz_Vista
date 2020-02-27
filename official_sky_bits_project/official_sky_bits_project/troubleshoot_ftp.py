
import pyodbc
import sqlite3
import csv
import datetime
from ftplib import FTP, FTP_TLS
import os
import sky_bits_api_parse


def import_to_ftp():
    import pdb; pdb.set_trace()
    with FTP_TLS("ftp.cloud.viewpoint.com") as ftps:
        ftps.login("945", "QnHS6468")
        ftps.prot_p()
        ftps.cwd(r"\imports\EM\SkyBitzMtr")
        local_path = r"C:\Users\jjacinto\OneDrive - HSI\Documents\GitHub\Skybitz_Vista\official_sky_bits_project\official_sky_bits_project\skybitz_2020102.csv"
        with open(local_path, "rb") as csv_file:
            ftps.storlines("Stor skybitz_2020102.csv", csv_file)
        ftps.dir()


import_to_ftp()
n
