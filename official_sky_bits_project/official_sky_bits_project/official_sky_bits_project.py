import os
import sys
import csv

from sky_bits_api_parse import get_fleet_array, fleet_list_dict, csv_import
# from vista_vehicle_database import all_vista_equipment, all_vista_operatorsdetail
from ftplib import FTP, FTP_TLS


csv_import(get_fleet_array(fleet_list_dict()))
# import pdb; pdb.set_trace()



#for row in all_vista_equipment():
    #print(row)


# print(fleet_list_dict())

# (1, 'AE059', '02', '10-02', '01.100', 'Ford', 'F250', '2006  ', '1FTNF20556EB68921', 'AE059 - John Gerard', 'A', Decimal('127992.00'), datetime.datetime(2019, 1, 16, 0, 0), ' T20044', 'HI', None, 1, None, None)