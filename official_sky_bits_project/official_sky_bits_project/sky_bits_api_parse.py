import requests
import xml.etree.ElementTree as ET
import csv
import datetime
import os
from os import system, name

from vista_vehicle_database import import_to_ftp


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def loading_bar(fleet_dict, fleet, counter):
    loading_bar = ""
    progress_at = counter
    for i in range(len(fleet_dict)):
        if progress_at > 0:
            loading_bar += "*"
            progress_at -= 1
        else:
            loading_bar += "_"
            progress_at -= 1
    clear()
    print("Loading Fleet: {}\n{}".format(fleet, loading_bar))
        


def fleet_list_dict():
    # ready for import
    parameters = {"user": "jjacinto@americanelectric.com", "password": "Blehbleh808"}
    response = requests.get("https://www.perigeegps.com/api/v1/DataFleetStatus2.asmx/GetFleetList?", params=parameters)
    with open('fleet_list.xml', 'wb') as f:
        f.write(response.content)
    tree = ET.parse("fleet_list.xml")
    root = tree.getroot()
    fleet_list_dict = {}
    for child in root:
        if child.tag == "{http://www.reltima.com/}ResultData":
            for fleet_status in child:
                fleet_name = ''
                fleet_id = ''
                for fleet_details in fleet_status:
                    if fleet_details.tag == '{http://www.reltima.com/}FleetID':
                        fleet_id += fleet_details.text
                    elif fleet_details.tag == '{http://www.reltima.com/}FleetName':
                        fleet_name += fleet_details.text
                fleet_list_dict[fleet_name] = fleet_id
    return fleet_list_dict


def get_odometer_data(vehicle_id):
    # ready for import
    now = datetime.datetime.now()
    past = now + datetime.timedelta(-30)
    end_date_string = now.strftime("%m/%d/%Y")
    start_date_string = past.strftime("%m/%d/%Y")
    parameters = {"vehicleID": vehicle_id, "start": start_date_string, "end": end_date_string, "user": "jjacinto@americanelectric.com", "password": "Blehbleh808"}
    response = requests.get("https://www.perigeegps.com/api/v1/DataFleetStatus2.asmx/GetVehicleTracksWithOdometer?", params=parameters)
    with open('odometer_data.xml', 'wb') as f:
        f.write(response.content)
    tree = ET.parse("odometer_data.xml")
    root = tree.getroot()
    odometer_data = []
    for child in root:
        if child.tag == "{http://www.reltima.com/}ResultData":
            for status in child:
                for details in status:
                    if details.tag == "{http://www.reltima.com/}Odometer":
                        odometer_data.append(details.text)
    if odometer_data:
        return odometer_data[len(odometer_data) - 1]
    else:
        return None

def csv_report_writer(fleet_file, csv_filename):
    # ready for import
    with open(csv_filename, mode='w', newline='') as fleet_file:
        report_writer = csv.writer(fleet_file)
        report_writer.writerow(['Vehicle Name','Odometer Reading','Fleet Name'])
        for data_row in vehicle_string_list:
            report_writer.writerow(data_row.split(','))

def get_fleet_sublists_dict(entire_fleet):
    fleet_dict = {}
    fleet_list = []
    for item in entire_fleet:
        if item[2] not in entire_fleet:
            fleet_list.append(item[2])
    for item in fleet_list:
        fleet_dict[item] = []
    for item in entire_fleet:
        fleet_dict[item[2]].append(item)
    return fleet_dict


def get_company(fleet):
    # import pdb; pdb.set_trace()
    # ready for import
    fleet_to_company_list = []
    fleet_to_company = {'CraneTech': 2, 'ElectroTest': 5, 'G&PS': 4}
    for item in fleet_to_company:
        fleet_to_company_list.append(item)
    if fleet in fleet_to_company_list:
        return fleet_to_company[fleet]
    else:
        return 1


def company_rectifier(vehicle_export_list, entire_fleet):
    company_checker = []
    final_export = []
    for vehicle in entire_fleet:
        if get_company(vehicle[2]) > 1:
            company_checker.append(vehicle)
    for vehicle in vehicle_export_list:
        if vehicle[0] in [i[0] for i in company_checker] and vehicle[3] == 1:
            for item in company_checker:
                if vehicle[0] == item[0]:
                    final_export.append([vehicle[0], vehicle[1], vehicle[2], item[3]])
        else:
            final_export.append(vehicle)
    return final_export

def duplicate_fix(export_list):
    final_export_fixed = []
    for vehicle in export_list:
        equipment_name = vehicle[0].strip().split("-")[0]
        duplicate_counter = 0
        for item in final_export_fixed:
            if item[0].strip().split("-")[0] == equipment_name:
                duplicate_counter += 1
        if duplicate_counter == 0:
            final_export_fixed.append(vehicle)
    return final_export_fixed
        


def get_fleet_array(fleet_list_dict):
    # ready for import
    entire_fleet = []
    vehicle_export_list = []
    csv_filename = 'Report_Folder\hsi_fleet.csv'
    counter = 0
    loading_bar(fleet_list_dict, "", counter)
    for fleet in fleet_list_dict:
        xml_filename = fleet
        parameters = {"fleetID": fleet_list_dict[fleet], "user": "jjacinto@americanelectric.com", "password": "Blehbleh808"}
        response = requests.get("https://www.perigeegps.com/api/v1/DataFleetStatus2.asmx/GetFleetStatus?", params=parameters)
        with open(xml_filename, 'wb') as f:
            f.write(response.content)
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        child_counter = 0
        for child in root:
            if child.tag == "{http://www.reltima.com/}ResultData":
                for vehicle_status in child:
                    details_list = []
                    vehicle_odometer_data = 0
                    for vehicle_description in vehicle_status:
                        if vehicle_description.tag == "{http://www.reltima.com/}VehicleID":
                            odometer_data_variable = get_odometer_data(vehicle_description.text)
                            if odometer_data_variable:
                                vehicle_odometer_data += float(odometer_data_variable)
                            else:
                                vehicle_odometer_data = None
                        if vehicle_description.tag == "{http://www.reltima.com/}VehicleName":
                            details_list.append(vehicle_description.text)
                        if vehicle_description.tag == "{http://www.reltima.com/}Odometer":
                            details_list.append(vehicle_odometer_data)
                    details_list.append(fleet)
                    details_list.append(get_company(fleet))
                    entire_fleet.append(details_list)
                child_counter += 1
        counter += 1
        loading_bar(fleet_list_dict, fleet, counter)
    fleet_list_dict = get_fleet_sublists_dict(entire_fleet)
    duplicate_checker = []
    special_fleet = []
    for fleet in fleet_list_dict:
        for vehicle in fleet_list_dict[fleet]:
            if vehicle[2] == 'Maui':
                vehicle_export_list.append(vehicle)
                duplicate_checker.append(vehicle[0])
            elif vehicle[2] == 'Kaui':
                vehicle_export_list.append(vehicle)
                duplicate_checker.append(vehicle[0])
            elif vehicle[2] == 'Big Island':
                vehicle_export_list.append(vehicle)
                duplicate_checker.append(vehicle[0])
            elif vehicle[2] == 'Oahu All':
                vehicle_export_list.append(vehicle)
                duplicate_checker.append(vehicle[0])
            else:
                special_fleet.append(vehicle)
    for vehicle in special_fleet:
        if vehicle[0] not in duplicate_checker:
            vehicle_export_list.append(vehicle)
    for vehicle in vehicle_export_list:
        if vehicle[2] == 'Maui':
            vehicle.append("Maui County")
        elif vehicle[2] == 'Kaui':
            vehicle.append("Kauai County")
        elif vehicle[2] == 'Big Island':
            vehicle.append("Hawaii County")
        else:
            vehicle.append("Oahu County")
    company_fixed_vehicle_export_list = company_rectifier(vehicle_export_list, entire_fleet)
    final_final_list = duplicate_fix(company_fixed_vehicle_export_list)
    return final_final_list


def get_formatted_date():
    now = datetime.datetime.now()
    current_month = now.strftime("%m")
    current_year = now.strftime("%Y")
    formatted_date = "{}/1/{}".format(current_month, current_year) # use this date for mth
    return formatted_date

def csv_import(get_fleet_array):
    formatted_date = get_formatted_date()
    file_formatted_date = "skybitz_{}{}{}.csv".format(formatted_date.split('/')[2], formatted_date.split('/')[1], formatted_date.split('/')[0])
    with open(file_formatted_date, mode='w', newline='') as csv_file:
        report_writer = csv.writer(csv_file)
        report_writer.writerow(['Co','Mth','BatchSeq','Equipment','CurrentOdometer']) # for csv
        report_list = []
        batch_counter = 1
        for vehicle in get_fleet_array:
            if vehicle[1]:
                co = vehicle[3]
                mth = formatted_date
                batch_seq = batch_counter
                equipment = vehicle[0].strip().split("-")[0]
                current_odometer = vehicle[1]
                report_writer.writerow([co,mth,batch_seq,equipment,current_odometer])
                batch_counter += 1
    import_to_ftp(file_formatted_date)
    os.remove(file_formatted_date)
            
