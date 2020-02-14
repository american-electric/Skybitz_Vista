import os
import sys
import csv

from sky_bits_api_parse import get_fleet_array, fleet_list_dict, csv_import
from vista_vehicle_database import all_vista_equipment, all_vista_operators
from ftplib import FTP, FTP_TLS


# csv_import(get_fleet_array(fleet_list_dict())) export works!
# import pdb; pdb.set_trace()
for row in all_vista_equipment():
    print(row)




