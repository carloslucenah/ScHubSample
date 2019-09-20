from datetime import datetime

import re
import pprint
from openpyxl import Workbook
import log_constants
import logging
import os, gzip
import sys


logging.getLogger().setLevel(logging.DEBUG)


def defineNewFields():
    """Definition of the fields to be incorporated into the results file, and how to obtain them.

    At this moment, there are five ways to calculate a field:

    1) Define start time from a component, and end time from the same or another one, and calculates the time between them.
    2) Copy a field from one component (such a "PROCESSING TIME" field).
    3) Sum of various fields. They can be a field from a file, or a previously calculated field (with any of the five methods).
	4) Define start time from a component, and end time from the same or another one or, in case it doesn't have end time, it takes the end time from a third component, and calculates the time between them.
	5) Create a new field in date format from a timestamp field of a component
    :returns: none
    """

        "Start-End": calculateStartEndField,
        "Sum": calculateSumField,
        "Copy": copyField,
        "Start-End-Substitute": calculateStartEndSubstituteField,
        "Date": calculateDateField
    
    global newFieldsDefinitions

    newFieldsDefinitions = dict()
    
    #Field Kernel Time: From OVG start time until CID RT end time


    newFieldsDefinitions ["OVG_START_TIME"] = dict()
    newFieldsDefinitions ["OVG_START_TIME"]["fieldType"]="Date"
    newFieldsDefinitions ["OVG_START_TIME"]["componentDate"]="OVG"
    newFieldsDefinitions ["OVG_START_TIME"]["fieldDate"]="START_TIME"

    newFieldsDefinitions ["OVG DISCIPLINE"] = dict()
    newFieldsDefinitions ["OVG DISCIPLINE"]["fieldType"]="Copy"
    newFieldsDefinitions ["OVG DISCIPLINE"]["component"]="OVG"
    newFieldsDefinitions ["OVG DISCIPLINE"]["field"]="DISCIPLINE"

    newFieldsDefinitions ["OVG_MESSAGE_TYPE"] = dict()
    newFieldsDefinitions ["OVG_MESSAGE_TYPE"]["fieldType"]="Copy"
    newFieldsDefinitions ["OVG_MESSAGE_TYPE"]["component"]="OVG"
    newFieldsDefinitions ["OVG_MESSAGE_TYPE"]["field"]="MESSAGE_TYPE"
##
##    newFieldsDefinitions ["VENUE KERNEL TIME"] = dict()
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["fieldType"]="Start-End-Substitute"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["componentStart"]="OVG"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["fieldStart"]="START_TIME"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["componentEnd"]="CID"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["fieldEnd"]="END_TIME"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["componentSubstitute"]="MOP"
##    newFieldsDefinitions ["VENUE KERNEL TIME"]["fieldSubstitute"]="END_TIME"
##
##
##    newFieldsDefinitions ["CIS_MULTICAST"] = dict()
##    newFieldsDefinitions ["CIS_MULTICAST"]["fieldType"]="Copy"
##    newFieldsDefinitions ["CIS_MULTICAST"]["component"]="CIS_MULTICAST"
##    newFieldsDefinitions ["CIS_MULTICAST"]["field"]="PROCESSING_TIME"
##
##    newFieldsDefinitions ["VENUE PUBLISH TIME"] = dict()
##    list_venuePublishTime = ["VENUE KERNEL TIME","CIS_MULTICAST"]
##    newFieldsDefinitions ["VENUE PUBLISH TIME"]["fieldType"]="Sum"
##    newFieldsDefinitions ["VENUE PUBLISH TIME"]["components"] = dict()
##    newFieldsDefinitions ["VENUE PUBLISH TIME"]["newFields"] = list_venuePublishTime
    # newFieldsDefinitions ["VENUE PUBLISH TIME"]["components"]["CIS_MULTICAST"]="PROCESSING_TIME"


## CENTRAL

    newFieldsDefinitions ["CENTRAL PUBLISH TIME"] = dict()
    newFieldsDefinitions ["CENTRAL PUBLISH TIME"]["fieldType"]="Start-End"
    newFieldsDefinitions ["CENTRAL PUBLISH TIME"]["componentStart"]="OVG"
    newFieldsDefinitions ["CENTRAL PUBLISH TIME"]["fieldStart"]="START_TIME"
    newFieldsDefinitions ["CENTRAL PUBLISH TIME"]["componentEnd"]="VEG"
    newFieldsDefinitions ["CENTRAL PUBLISH TIME"]["fieldEnd"]="END_TIME"

    newFieldsDefinitions ["CENTRAL TIME"] = dict()
    newFieldsDefinitions ["CENTRAL TIME"]["fieldType"]="Start-End-Substitute"
    newFieldsDefinitions ["CENTRAL TIME"]["componentStart"]="CEG"
    newFieldsDefinitions ["CENTRAL TIME"]["fieldStart"]="START_TIME"
    newFieldsDefinitions ["CENTRAL TIME"]["componentEnd"]="CID_CENTRAL"
    newFieldsDefinitions ["CENTRAL TIME"]["fieldEnd"]="END_TIME"
    newFieldsDefinitions ["CENTRAL TIME"]["componentSubstitute"]="MOP_CENTRAL"
    newFieldsDefinitions ["CENTRAL TIME"]["fieldSubstitute"]="END_TIME"
    
##
####### Este ya no es necesario     
##    newFieldsDefinitions ["CENTRAL CIDRT"] = dict()
##    newFieldsDefinitions ["CENTRAL CIDRT"]["fieldType"]="Copy"
##    newFieldsDefinitions ["CENTRAL CIDRT"]["component"]="CID_CENTRAL"
##    newFieldsDefinitions ["CENTRAL CIDRT"]["field"]="PROCESSING_TIME"
######
    
##    newFieldsDefinitions ["CIS UNICAST"] = dict()
##    newFieldsDefinitions ["CIS UNICAST"]["fieldType"]="Copy"
##    newFieldsDefinitions ["CIS UNICAST"]["component"]="CIS_UNICAST"
##    newFieldsDefinitions ["CIS UNICAST"]["field"]="PROCESSING_TIME"

    
    ##list_totalCentralTime = ["CENTRAL PUBLISH TIME", "CENTRAL TIME", "CENTRAL CIDRT", "CIS UNICAST"]
##    list_totalCentralTime = ["CENTRAL PUBLISH TIME", "CENTRAL TIME", "CIS UNICAST"]

    newFieldsDefinitions ["TOTAL CENTRAL TIME"] = dict()
    list_totalCentralTime = ["CENTRAL PUBLISH TIME", "CENTRAL TIME"]
    newFieldsDefinitions ["TOTAL CENTRAL TIME"]["fieldType"]="Sum"
    newFieldsDefinitions ["TOTAL CENTRAL TIME"]["components"] = dict()
    newFieldsDefinitions ["TOTAL CENTRAL TIME"]["newFields"] = list_totalCentralTime
    newFieldsDefinitions ["TOTAL CENTRAL TIME"]["components"]["CIS_MULTICAST"]="PROCESSING_TIME"
    
##
##
##    newFieldsDefinitions ["CENTRAL TIME"] = dict()
##    newFieldsDefinitions ["CENTRAL TIME"]["fieldType"]="Sum"
##    newFieldsDefinitions ["CENTRAL TIME"]["componentOne"]="CIS"
##    newFieldsDefinitions ["CENTRAL TIME"]["fieldOne"]="PROCESSING_TIME"
##    newFieldsDefinitions ["CENTRAL TIME"]["componentTwo"]=""
##    newFieldsDefinitions ["CENTRAL TIME"]["fieldTwo"]="VENUE KERNEL TIME" 


def read_lines_from_path(path):
    """Reads the lines from all files in given path.

    For each file in the given path, it will iterate them and will yield each line in.

    :param folder_path: folder path containing files to be read
    :returns: yield for each line in every file
    """
    print("Reading file: "+path)
    with open(path) as archivo:
        for line in archivo:
            yield line.rstrip("\n")


def initialize ():
    """Uncompose line to extract desired values of OVG log: Start time, disciplines, message type and venue.

    :param line: line of OVG log
    :param _: TODO
    :return: None
    """
    global mainDictionary
    global newFieldsDictionary

    mainDictionary = dict()
    newFieldsDictionary = dict()
    defineNewFields()

def readCsv (component, path):
    """Uncompose line to extract desired values of OVG log: Start time, disciplines, message type and venue.

    :param line: line of OVG log
    :param _: TODO
    :return: None
    """
    for line in read_lines_from_path(path):
        if "MESSAGE_ID" in line:
            fields = line.split("##")
        else:
            values = line.split("##")
            key = values[0]
            if key not in mainDictionary.keys():
                mainDictionary[key] = dict()
            mainDictionary[key][component] = dict()
            for position,field in enumerate(fields):
                if position > 0:
                    mainDictionary[key][component][field] = values[position]
                 

def calculateStartEndField (key, header):
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :return: None
    """
    # print("He llegado al calculateStartEndField de la key: " + key)
    if key not in newFieldsDictionary.keys():
        newFieldsDictionary[key] = dict()

    componentStart = newFieldsDefinitions[header]["componentStart"]
    componentEnd = newFieldsDefinitions[header]["componentEnd"]
    fieldStart = newFieldsDefinitions[header]["fieldStart"]
    fieldEnd = newFieldsDefinitions[header]["fieldEnd"]
    if (componentStart not in mainDictionary[key].keys()) or (componentEnd not in mainDictionary[key].keys()):
        newFieldsDictionary[key][header] = 0
    else:
        newFieldsDictionary[key][header] = int(mainDictionary[key][componentEnd][fieldEnd]) - int(mainDictionary[key][componentStart][fieldStart])
        #print(int(mainDictionary[key][componentEnd][fieldEnd]) - int(mainDictionary[key][componentStart][fieldStart]))
           
    # print ("Hora de fin: " + mainDictionary[key][componentEnd][fieldEnd])
    # print ("Hora de inicio: " + mainDictionary[key0][componentStart][fieldStart])


def calculateDateField (key, header):
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :return: None
    """
    # print("He llegado al calculateStartEndField de la key: " + key)
    if key not in newFieldsDictionary.keys():
        newFieldsDictionary[key] = dict()

    componentDate = newFieldsDefinitions[header]["componentDate"]
    fieldDate = newFieldsDefinitions[header]["fieldDate"]
    # dateFormat = newFieldsDefinitions[header]["dateFormat"]

    if componentDate not in mainDictionary[key].keys():
        newFieldsDictionary[key][header] = 0
    else:
        # print (datetime.fromtimestamp(int(mainDictionary[key][componentDate][fieldDate])/1000))
        newFieldsDictionary[key][header] = datetime.fromtimestamp(int(mainDictionary[key][componentDate][fieldDate])/1000)


def calculateStartEndSubstituteField (key, header):
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :return: None
    """
    # print("He llegado al calculateStartEndField de la key: " + key)
    if key not in newFieldsDictionary.keys():
        newFieldsDictionary[key] = dict()

    componentStart = newFieldsDefinitions[header]["componentStart"]
    componentEnd = newFieldsDefinitions[header]["componentEnd"]
    componentSubstitute = newFieldsDefinitions[header]["componentSubstitute"]

    fieldStart = newFieldsDefinitions[header]["fieldStart"]
    fieldEnd = newFieldsDefinitions[header]["fieldEnd"]
    fieldSubstitute = newFieldsDefinitions[header]["fieldSubstitute"]
    
    if componentStart not in mainDictionary[key].keys():
        startTime = 0
    else:
        startTime = int(mainDictionary[key][componentStart][fieldStart])
    
    if componentEnd not in mainDictionary[key].keys():
        if componentSubstitute not in mainDictionary[key].keys():
            endTime = 0
        else:
            endTime = int(mainDictionary[key][componentSubstitute][fieldSubstitute])
    else:
        endTime = int(mainDictionary[key][componentEnd][fieldEnd])

    if startTime == 0 or endTime == 0:
        newFieldsDictionary[key][header] = 0
    else:
        newFieldsDictionary[key][header] =  endTime - startTime
        #print(int(mainDictionary[key][componentEnd][fieldEnd]) - int(mainDictionary[key][componentStart][fieldStart]))
           
    # print ("Hora de fin: " + mainDictionary[key][componentEnd][fieldEnd])
    # print ("Hora de inicio: " + mainDictionary[key][componentStart][fieldStart])


def copyField (key, header):
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :return: None
    """
    if key not in newFieldsDictionary.keys():
        newFieldsDictionary[key] = dict()

    component = newFieldsDefinitions[header]["component"]
    field = newFieldsDefinitions[header]["field"]

    if (component not in mainDictionary[key].keys()):
        newFieldsDictionary[key][header] = 0
    else:
        newFieldsDictionary[key][header] = mainDictionary[key][component][field]
        #print(int(mainDictionary[key][componentEnd][fieldEnd]) - int(mainDictionary[key][componentStart][fieldStart]))
           
    # print ("Hora de fin: " + mainDictionary[key][componentEnd][fieldEnd])
    # print ("Hora de inicio: " + mainDictionary[key][componentStart][fieldStart])



def calculateSumField (key, header):
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :return: None
    """
    # print("He llegado al calculateSumField de la key: " + key)
    if key not in newFieldsDictionary.keys():
        newFieldsDictionary[key] = dict()

    sumNewFields = 0
    sumComponents = 0

    #print ("Para el header " + header + " tengo: ")
    #print (newFieldsDefinitions[header].keys())
    
    for field in newFieldsDefinitions[header]["newFields"]:
        if field in newFieldsDictionary[key].keys():
            sumNewFields += int(newFieldsDictionary[key][field])


    for component in newFieldsDefinitions[header]["components"].keys():
        if component in mainDictionary[key].keys():
            field = newFieldsDefinitions[header]["components"][component]
            sumComponents += int(mainDictionary[key][component][field])

    #print("Se agrega a la key: " + key + " la header: " + header + " con valor: " + str(int(sumOne) + int(sumTwo)))
    #newFieldsDictionary[key][header] = str(int(sumOne) + int(sumTwo))
    newFieldsDictionary[key][header] = int(sumNewFields) + int(sumComponents)
    # print ("Hora de fin: " + mainDictionary[key][componentEnd][fieldEnd])
    # print ("Hora de inicio: " + mainDictionary[key][componentStart][fieldStart])                    



def addNewFields ():
    """Calculate the value of a new field from start time and end time from the same or different components, and adds it to the newFieldsDictionary.

    :param key: Message id
    :param header: Name of the new field
    :param componentStart: Name of the component with the start time to be read
    :param fieldStart: Name of the field with the start time to be read
    :param componentEnd: Name of the component with the end time to be read
    :param fieldEnd: Name of the field with the end time to be read
    :return: None
    """
    switchFieldType = {
        "Start-End": calculateStartEndField,
        "Sum": calculateSumField,
        "Copy": copyField,
        "Start-End-Substitute": calculateStartEndSubstituteField,
        "Date": calculateDateField
        }
    
    #print(newFieldsDefinitions.keys())
    for key in mainDictionary:
        #if key not in 
        for field in newFieldsDefinitions:
            func = switchFieldType[newFieldsDefinitions[field]["fieldType"]]
            # print("func vale: " +func)
            func(key, field)

    
def print_results():
    pprint.pprint(results)



def save_results():

    # available_keys = ['OVG', 'MOP', 'CID_RT', 'CIS_CLIENT', 'VEG', 'CLIENT_MULTICAST']

    file = open("./results.csv", "w")
    tempKey = list(newFieldsDictionary.keys())[0]
    headers = list(newFieldsDictionary[tempKey].keys())
    stringHeader = "MESSAGE_ID##"
    for header in headers:
        if headers.index(header) < len(headers)-1:
            stringHeader = stringHeader + header + "##"
        else:
            stringHeader = stringHeader + header + "\n"

    file.write(stringHeader)
    #print (headers)
    for key in newFieldsDictionary:
        stringLine = key + "##"
        fieldsList = list(newFieldsDictionary[key].keys())
        #print (fieldsList)
        for field in fieldsList:
            if fieldsList.index(field) < len(fieldsList)-1:
                stringLineAux = str(newFieldsDictionary[key][field]) + "##"
                stringLine = stringLine + stringLineAux
                #print(stringLine)
            else:
                #print(newFieldsDictionary[key][field])
                #print(field)
                stringLineAux = str(newFieldsDictionary[key][field]) + "\n"
                stringLine = stringLine + stringLineAux
        # print(stringLine)
        file.write(stringLine)


if __name__ == "__main__":

    ## Se crean los diccionarios y se inicializa el proceso
    initialize()

    ## Se espefican los ficheros csv a leer
    readCsv("OVG","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results_OVG_venue.csv")
    #readCsv("CID","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/Resultados_Venue/results_CID_RT.csv")
    #readCsv("CIS_MULTICAST","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/Resultados_Venue/results_CLIENT_MULTICAST.csv")
    #readCsv("MOP","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/Resultados_Venue/results_MOP.csv")
    readCsv("VEG","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results_VEG_venue.csv")
    readCsv("CEG","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results_CEG.csv")
    readCsv("CID_CENTRAL","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results_CID_RT.csv")
    #readCsv("CIS_UNICAST","C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/enviar_05072019/resultados_CENTRAL_08072019/results_CLIENT_MULTICAST.csv")
    readCsv("MOP_CENTRAL","C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results_MOP.csv")


    ## Se agregan los campos generados
    addNewFields()

    ## Se genera el fichero de resultados
    save_results()
