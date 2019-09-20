from datetime import datetime

import re
import pprint
from openpyxl import Workbook
import log_constants
import logging
import os, gzip
import sys


# VARIABLE DECLARATION #

#main_path = "C:/MEV/Tokyo2020/Trazas_Transacciones/ParaJesus_o_Carlos/venue_kernel_data"

logging.getLogger().setLevel(logging.DEBUG)

global results
global message_id_keys
global wb
global ws_ovg
global ws_mop
global ws_cidRT
global date_venue_split_number
global date_central_split_number

date_venue_split_number = 10
date_central_split_number = 0

date_mop_venue_split_number = 1
date_mop_central_split_number = 0

date_cid_venue_split_number = 8
date_cid_central_split_number = 0

date_veg_venue_split_number = 10
date_veg_central_split_number = 0

date_cis_unicast_split_bottom = 1
date_cis_unicast_split_top = 3

date_cis_multicast_split_bottom = 1
date_cis_multicast_split_top = 3

results = dict()

uncompose_ovg_first_reference_counter = 0
ovg_first_reference_dict = dict()

uncompose_ovg_second_reference_counter = 0
ovg_second_reference_dict = dict()
ceg_second_reference_dict = dict()


uncompose_ovg_third_reference_counter = 0
ovg_third_reference_dict = dict()
ceg_third_reference_dict = dict()

uncompose_ovg_reference = dict()

trx_id_dict_to_key = dict()
ready_id_join_trx_id_dict = dict()

# PATH VARIABLES #

# VENUE
DKERMOP_FOLDER_PATH =           "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/isyt01_kernel_data/MOP"
DKEROVG_FOLDER_PATH =           "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/isyt01_kernel_data/OVG"
DKERCIDRT_FOLDER_PATH =         "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/isyt01_kernel_data/CIDRT"
DKERVEG_FOLDER_PATH =           "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/isyt01_kernel_data/VEG"
CLIENT_MULTICAST_FOLDER_PATH =  "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/isyt1_cis_logs"

# CENTRAL
DKERCEG_FOLDER_PATH =           "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/central_kernellogs/dkerceg"
DKERCIDRT_CENTRAL_FOLDER_PATH = "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/central_kernellogs/CIDRT"
DKERMOP_CENTRAL_FOLDER_PATH = "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/central_kernellogs/MOP"
DKERVEG_CENTRAL_FOLDER_PATH = "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/central_kernellogs/VEG"
CLIENT_UNICAST_FOLDER_PATH =    "C:/MEV/Tokyo2020/Trazas_Transacciones/08072019/paraCarlos/ikst02_rcis_logs"


def read_lines_from_path(folder_path):
    """Reads the lines from all files in given path.

    For each file in the given path, it will iterate them and will yield each line in.

    :param folder_path: folder path containing files to be read
    :returns: yield for each line in every file
    """
    dirlist = [n for n in os.listdir(folder_path) if os.path.isdir(folder_path + "/" + n)]
    flist = [n for n in os.listdir(folder_path) if os.path.isfile(folder_path + "/" + n)]
    print(*dirlist)
    print(*flist)
    for folder in dirlist:
        filelist = [f for f in os.listdir(folder_path + "/" + folder)]
        for f in filelist:
            print("Reading file: "+f)
            # with gzip.open(folder_path + "/" + folder + "/" + f) as archivo:
            with open(folder_path + "/" + folder + "/" + f) as archivo:
                for line in archivo:
                    try:
                        line = str(line, 'utf-8')
                    except TypeError:
                        pass
                    yield line.rstrip("\n")
    for f in flist:
        print("Reading file: "+f)
        with open(folder_path + "/" + f) as archivo:
            for line in archivo:
                yield line.rstrip("\n")


def dump_all_logs(filename, folder_path, allowed_lines):
    """Dump regex matches to corresponding dict.

    Reading every line in each file found in given folder path, it applies all different regex patterns given in allowed lines parameter.
    Every match will be added into corresponding dict (OVG, MOP...).
    In case of "dkerovg" file, it uses three different dictionaries which must be joined after read all files. This step is done by the 'matching_references()' function.

    :param filename: main name of the filename to be read (dkerovg, dkermop...)
    :param folder_path: folder path containing files to be read
    :param allowed_lines: all allowed regex patterns which be applied to find desired values. (NOTE: This lines are declared into 'log_constants.py' file.)
    """
    logging.debug("STARTING LOG DUMPING FOR: "+filename)

    with open("./filename_"+filename+".log", "w") as todos:
        for line in read_lines_from_path(folder_path):
            found_allowed = [allowed for allowed in allowed_lines if re.search(allowed, line)]
            if len(found_allowed) > 0:
                print(line, file=todos)
                func = switch_uncompose.get(found_allowed[0])
                func(line, found_allowed[0])

    if filename == "dkerovg":
        with open("C:/tmp/resultados_first_reference", "w") as first:
            pprint.pprint(ovg_first_reference_dict, stream=first)
        # pprint.pprint(ovg_first_reference_dict)
        with open("C:/tmp/resultados_second_reference", "w") as second:
            pprint.pprint(ovg_second_reference_dict, stream=second)
        # pprint.pprint(ovg_second_reference_dict)
        with open("C:/tmp/resultados_third_reference", "w") as third:
            pprint.pprint(ovg_third_reference_dict, stream=third)
        # pprint.pprint(ovg_third_reference_dict)
        matching_references(filename)


    if filename == "dkerceg":
##        with open("C:/tmp/resultados_first_reference_ceg", "w") as first:
##            pprint.pprint(ceg_first_reference_dict, stream=first)
        # pprint.pprint(ovg_first_reference_dict)
        with open("C:/tmp/resultados_second_reference_ceg", "w") as second:
            pprint.pprint(ceg_second_reference_dict, stream=second)
        # pprint.pprint(ovg_second_reference_dict)
        with open("C:/tmp/resultados_third_reference_ceg", "w") as third:
            pprint.pprint(ceg_third_reference_dict, stream=third)
        # pprint.pprint(ovg_third_reference_dict)
        matching_references(filename)

    logging.debug("FINISHED LOG DUMPING FOR: " + filename)



def uncompose_ceg_first_reference(line, _):
    uncompose_ovg_first_reference(line, "CEG")

def uncompose_ceg_second_reference(line, _):
    uncompose_ovg_second_reference(line, "CEG")

def uncompose_ceg_third_reference(line, _):
    uncompose_ovg_third_reference(line, "CEG")



def uncompose_ovg_first_reference(line, component = "OVG"):
    """Uncompose line to extract desired values of OVG log: Start time, disciplines, message type and venue.

    :param line: line of OVG log
    :param _: TODO
    :return: None
    """
    global uncompose_ovg_first_reference_counter
    global ovg_first_reference_dict
    if component == "CEG":
        date_field = date_central_split_number
    else:
        date_field = date_venue_split_number

    new_message = dict()

    new_message["start_time"] = datetime_to_milliseconds(line.split(" ")[date_field])
    new_message["discipline"] = line.split(" ")[-1].split(";")[-5].split("=")[-1]
    new_message["message_type"] = line.split(" ")[-1].split(";")[-1].split("=")[-1].rstrip("\n")
    new_message["venue"] = line.split(" ")[-1].split(";")[-6].split("=")[-1]

    ovg_first_reference_dict[len(ovg_first_reference_dict.keys())] = new_message


def uncompose_ovg_second_reference(line, component = "OVG"):
    """Uncompose line to extract desired values of OVG log: timestamp, message id, discipline and message type.

    :param line: line of OVG log
    :param _: TODO
    :return: None
    """
    global uncompose_ovg_second_reference_counter
    global ovg_second_reference_dict
    global ceg_second_reference_dict
    
    if component == "CEG":
        date_field = date_central_split_number
        dictionary = ceg_second_reference_dict
    else:
        date_field = date_venue_split_number
        dictionary = ovg_second_reference_dict

        
    new_message = dict()

    new_message["timestamp"] = datetime_to_milliseconds(line.split(" ")[date_field])
    new_message["message_id"] = re.search(log_constants.OVG_MESSAGE_HEADERHASH_TAG, line).group(1)
    new_message["discipline"] = re.search(log_constants.OVG_MESSAGE_DISCIPLINE_TAG, line).group(1)
    new_message["message_type"] = re.search(log_constants.OVG_MESSAGE_TYPE_TAG, line).group(1)

    dictionary[len(dictionary.keys())] = new_message


def uncompose_ovg_third_reference(line, component = "OVG"):
    """Uncompose line to extract desired values of OVG log: end time.

    :param line: line of OVG log
    :param _: TODO
    :return: None
    """
    global uncompose_ovg_third_reference_counter
    global ovg_third_reference_dict
    global ceg_second_reference_dict

    
    if component == "CEG":
        date_field = date_central_split_number
        dictionary = ceg_third_reference_dict

    else:
        date_field = date_venue_split_number
        dictionary = ovg_third_reference_dict
        
    message_id = line.split(" ")[-1].rstrip("\n")
    dictionary[message_id] = dict()
    dictionary[message_id]["end_time"] = datetime_to_milliseconds(line.split(" ")[date_field])



def matching_references(component):
    """Join into the first dictionary the second and third dictionaries (of the OVG log) using the message_id reference.

    After read all files, elements are stored into three different dictionaries. This function dumps the second and
    third dictionaries into the first one using message_id reference among others.
    Then, when all information is stored into the first dictionary, it will execute 'dump_ovg_references()' to re-order
    information.

    In case of use 'dkerceg' instead of 'dkerovg', it will execute 'dump_ceg_references()' directly.
    """
    if component == "dkerceg":
        dump_ceg_references()
    else:
        for i in range(0, len(ovg_first_reference_dict.keys())):
            for j in ovg_second_reference_dict.keys():
                if (ovg_first_reference_dict[i]["discipline"] == ovg_second_reference_dict[j]["discipline"] and
                        ovg_first_reference_dict[i]["message_type"] == ovg_second_reference_dict[j]["message_type"] and
                        ovg_first_reference_dict[i]["start_time"] < ovg_second_reference_dict[j]["timestamp"]):
                                ovg_first_reference_dict[i]["message_id"] = ovg_second_reference_dict[j]["message_id"]
                                if ovg_second_reference_dict[j]["message_id"] in ovg_third_reference_dict.keys():
                                    ovg_first_reference_dict[i]["end_time"] = ovg_third_reference_dict[ovg_second_reference_dict[j]["message_id"]]["end_time"]
                                    # ADDING PROCESSING TIME
                                    ovg_first_reference_dict[i]["processing_time"] = ovg_first_reference_dict[i]["end_time"] - ovg_first_reference_dict[i]["start_time"]
                                    del ovg_third_reference_dict[ovg_second_reference_dict[j]["message_id"]]
                                del ovg_second_reference_dict[j]
                                break

        dump_ovg_references()


def dump_ovg_references():
    """Reorders the first dictionary of OVG log.

    Method to reorder the first dictionary, which stores information about OVG log, after dumping on it the second and third dictionaries.

    :return: None
    """
    for i in ovg_first_reference_dict.keys():
        uncompose_ovg_reference[ovg_first_reference_dict[i]["message_id"]] = dict()
        uncompose_ovg_reference[ovg_first_reference_dict[i]["message_id"]]["OVG"] = dict()

        uncompose_ovg_reference[ovg_first_reference_dict[i]["message_id"]]["OVG"] = ovg_first_reference_dict[i]
        del uncompose_ovg_reference[ovg_first_reference_dict[i]["message_id"]]["OVG"]["message_id"]

    # pprint.pprint(uncompose_ovg_reference)


def dump_ceg_references():
    """Reorders the first dictionary of CEG log.

    Method to reorder the first, second and third dictionary dumping it to only one.
    Is similar to the 'dump_ovg_references()' but this case is only applied to the DKERCEG version.

    :return: None
    """
    for i in ceg_second_reference_dict.keys():
        message_id = ceg_second_reference_dict[i]["message_id"]
        
        if message_id not in uncompose_ovg_reference.keys():
            uncompose_ovg_reference[message_id] = dict()
        # {0: {'discipline': 'TEN',
        #      'message_id': 'a5a836cc008131c28459d79e8a3516ce93fbac1b',
        #      'message_type': 'DT_CONFIG',
        #      'timestamp': 1552405959108},
        uncompose_ovg_reference[message_id]["CEG"] = dict()

        uncompose_ovg_reference[message_id]["CEG"]["discipline"] = ceg_second_reference_dict[i]["discipline"]
        uncompose_ovg_reference[message_id]["CEG"]["message_type"] = ceg_second_reference_dict[i]["message_type"]
        uncompose_ovg_reference[message_id]["CEG"]["start_time"] = ceg_second_reference_dict[i]["timestamp"]

        try:
            uncompose_ovg_reference[message_id]["CEG"]["end_time"] = ceg_third_reference_dict[message_id]["end_time"]
            uncompose_ovg_reference[message_id]["CEG"]["processing_time"] = ceg_third_reference_dict[message_id]["end_time"] - uncompose_ovg_reference[message_id]["CEG"]["start_time"]
        except KeyError:
            pass

    # pprint.pprint(uncompose_ovg_reference)


switch_mop_start_end = {
    log_constants.MOP_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST: "start_time",
    log_constants.MOP_MESSAGE_RECEIVED_CONST: "start_time",
    log_constants.MOP_MESSAGE_PROCESSED_CONST_3: "end_time",
    log_constants.MOP_MESSAGE_SKIPPED_CONST: "end_time",
    log_constants.MOP_MESSAGE_ERROR_CONST: "end_time",
    log_constants.MOP_TRANSACTION_ID: "transaction_id"
}

switch_mop_central_start_end = {
    log_constants.MOP_CENTRAL_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST: "start_time",
    log_constants.MOP_CENTRAL_MESSAGE_RECEIVED_CONST: "start_time",
    log_constants.MOP_CENTRAL_MESSAGE_PROCESSED_CONST_3: "end_time",
    log_constants.MOP_CENTRAL_MESSAGE_SKIPPED_CONST: "end_time",
    log_constants.MOP_CENTRAL_MESSAGE_ERROR_CONST: "end_time",
    log_constants.MOP_CENTRAL_TRANSACTION_ID: "transaction_id"
}

switch_cidrt_start_end = {
    log_constants.CID_RT_INFO_RECEIVED_MODELTRANSACTION_CONST: "start_time",
    log_constants.CID_RT_INFO_PROCESSED_MODELTRANSACTION_CONST: "end_time",
    log_constants.CID_RT_INFO_SENDING_PROJECT_GET_ID: "trx_id"
}

switch_cidrt_central_start_end = {
    log_constants.CID_RT_CENTRAL_INFO_RECEIVED_MODELTRANSACTION_CONST: "start_time",
    log_constants.CID_RT_CENTRAL_INFO_PROCESSED_MODELTRANSACTION_CONST: "end_time",
    log_constants.CID_RT_CENTRAL_INFO_SENDING_PROJECT_GET_ID: "trx_id"
}


def mop_central_add_start_end_time(line, regex):
    mop_add_start_end_time(line, regex, "MOP_CENTRAL")

def mop_add_start_end_time(line, regex, component = "MOP"):
    """TOOL FUNCTION: 

    :param line:
    :param regex:
    :return:
    """
    key = re.search(regex, line).group(1)

    # only when is dumping MOP #
    if uncompose_ovg_reference.get(key) is None:
        uncompose_ovg_reference[key] = dict()

    if component not in uncompose_ovg_reference[key].keys():
        uncompose_ovg_reference[key][component] = dict()

    if (component == "MOP_CENTRAL"):
        switch = switch_mop_central_start_end
        date_field = date_mop_central_split_number
    else:
        switch = switch_mop_start_end
        date_field = date_mop_venue_split_number
        
    # print(regex)
    if (component == "MOP_CENTRAL"):
        uncompose_ovg_reference[key][component][switch[regex]] = datetime_to_milliseconds(line.split(" ")[date_field])
    else:
        uncompose_ovg_reference[key][component][switch_mop_start_end[regex]] = datetime_to_milliseconds(line.split("0m")[-1].split(" ")[date_field])


    # ADDING PROCESSING TIME
    # print (regex)
    if switch[regex] == "end_time":
        if "start_time" in uncompose_ovg_reference[key][component].keys():
            uncompose_ovg_reference[key][component]["processing_time"] = uncompose_ovg_reference[key][component]["end_time"] - uncompose_ovg_reference[key][component]["start_time"]
        else:
            uncompose_ovg_reference[key][component]["processing_time"] = "Not valid"



def mop_central_add_transaction_id(line, regex, component = "MOP"):
    mop_add_transaction_id(line, regex, "MOP_CENTRAL")

def mop_add_transaction_id(line, regex, component = "MOP"):

    transaction_id = re.search(regex, line).group(1)
    key = transaction_id.split("#")[-1]

    ##only when is dumping MOP ##
    if uncompose_ovg_reference.get(key) is None:
        uncompose_ovg_reference[key] = dict()

    if "MOP" not in uncompose_ovg_reference[key].keys():
        uncompose_ovg_reference[key][component] = dict()

    uncompose_ovg_reference[key][component][switch_mop_start_end[regex]] = transaction_id


def cidrt_central_add_start_end_time(line, regex):
   cidrt_add_start_end_time(line, regex, "CIDRT_CENTRAL")

def cidrt_add_start_end_time(line, regex, component = "CID_RT"):

    if (component == "CIDRT_CENTRAL"):
        switch = switch_cidrt_central_start_end
        date_field = date_cid_central_split_number
    else:
        switch = switch_cidrt_start_end
        date_field = date_cid_venue_split_number

    key = line.split("#")[-1].rstrip("\n")
    #print ("La key vale: " + key)

    ##ONLY CIDRT WITHOUT OVG##
    if uncompose_ovg_reference.get(key) is None:
        uncompose_ovg_reference[key] = dict()

    try:
        if component not in uncompose_ovg_reference[key].keys():
            uncompose_ovg_reference[key][component] = dict()

        uncompose_ovg_reference[key][component][switch[regex]] = datetime_to_milliseconds(line.split(" ")[date_field])

        ## ADDING PROCESSING TIME

        if switch[regex] == "end_time":
            uncompose_ovg_reference[key][component]["processing_time"] = uncompose_ovg_reference[key][component]["end_time"] - uncompose_ovg_reference[key][component]["start_time"]
    except KeyError:
        pass

def cidrt_central_add_id(line, regex):
    cidrt_add_id(line, regex, "CIDRT_CENTRAL")


def cidrt_add_id(line, regex, component = "CID_RT"):

    key = line.split("#")[-1].rstrip("\n")
    discipline = re.search(regex, line).group(1)
    trx_id = re.search(regex, line).group(2)

    if (component == "CIDRT_CENTRAL"):
        switch = switch_cidrt_central_start_end
    else:
        switch = switch_cidrt_start_end

    try:
        if component not in uncompose_ovg_reference[key].keys():
            uncompose_ovg_reference[key][component] = dict()

        uncompose_ovg_reference[key][component][switch[regex]] = trx_id
        uncompose_ovg_reference[key][component]["discipline"] = discipline
        discipline = discipline.replace("/"," ")
        trx_id_dict_to_key[discipline+ "#" + trx_id] = key

    except KeyError:
        print("The key: " + key + " does not exist in the list.")
        pass


def cisclient_add_time(line, regex):

    trx_id = re.search(regex, line).group(1)

    key = get_key_from_trx_id(trx_id)

    if key is not None:
        if "CIS_CLIENT" not in uncompose_ovg_reference[key].keys():
            uncompose_ovg_reference[key]["CIS_CLIENT"] = dict()

        uncomposed_hour = line.split(" ")
        uncompose_ovg_reference[key]["CIS_CLIENT"][switch_cis_client_start_end[regex]] = datetime_to_milliseconds_CIS_CLIENT(uncomposed_hour[1]+" "+uncomposed_hour[2])

        ## ADDING PROCESSING TIME

        if switch_cis_client_start_end[regex] == "end_time":
            uncompose_ovg_reference[key]["CIS_CLIENT"]["processing_time"] = uncompose_ovg_reference[key]["CIS_CLIENT"]["end_time"] - uncompose_ovg_reference[key]["CIS_CLIENT"]["start_time"]


switch_cis_client_start_end = {
    log_constants.CIS_CLIENT_RECEIVED_TRANSACTION: "start_time",
    log_constants.CIS_CLIENT_PROCESSED_TRANSACTION: "end_time"
}


def get_key_from_trx_id(trx_id):

    for k in uncompose_ovg_reference.keys():
        if "CID_RT" in uncompose_ovg_reference[k].keys():
            if uncompose_ovg_reference[k]["CID_RT"]["trx_id"] == str(trx_id):
                return k

    return None


switch_veg_start_end = {
    log_constants.VEG_RECEIVED_TRANSACTION: "start_time",
    log_constants.VEG_SENT_TRANSACTION: "end_time"
}

switch_veg_central_start_end = {
    log_constants.VEG_CENTRAL_RECEIVED_TRANSACTION: "start_time",
    log_constants.VEG_CENTRAL_SENT_TRANSACTION: "end_time"
}


def veg_central_add_time(line, regex):
    veg_add_time(line, regex, "VEG_CENTRAL")


def veg_add_time(line, regex, component = "VEG"):

    key = re.search(regex, line).group(1)

    if (component == "VEG_CENTRAL"):
        switch = switch_veg_central_start_end
        date_field = date_veg_central_split_number
    else:
        switch = switch_veg_start_end
        date_field = date_veg_venue_split_number

    if component not in uncompose_ovg_reference[key].keys():
        uncompose_ovg_reference[key][component] = dict()

    uncompose_ovg_reference[key][component][switch[regex]] = datetime_to_milliseconds(line.split(" ")[date_field])

    ## ADDING PROCESSING TIME

    if switch[regex] == "end_time":
        uncompose_ovg_reference[key][component]["processing_time"] = uncompose_ovg_reference[key][component]["end_time"] - \
                                                                 uncompose_ovg_reference[key][component]["start_time"]


switch_client_multicast_start_end = {
    log_constants.CLIENT_MULTICAST_RECEIVED_TRANSACTION: "start_time",
    log_constants.CLIENT_MULTICAST_TIMES_TRANSACTION: "end_time"
}

switch_client_unicast_start_end = {
    log_constants.CLIENT_UNICAST_RECEIVED_TRANSACTION: "start_time",
    log_constants.CLIENT_UNICAST_TIMES_TRANSACTION: "end_time"
}


def client_unicast_add_time(line, regex):
    client_multicast_add_time(line, regex, "CLIENT_UNICAST")

def client_multicast_add_time(line, regex, component="CLIENT_MULTICAST"):

    constants = {"CLIENT_UNICAST": {"RECEIVED":log_constants.CLIENT_UNICAST_RECEIVED_TRANSACTION, "TIMES": log_constants.CLIENT_UNICAST_TIMES_TRANSACTION },
                 "CLIENT_MULTICAST": {"RECEIVED":log_constants.CLIENT_MULTICAST_RECEIVED_TRANSACTION, "TIMES": log_constants.CLIENT_MULTICAST_TIMES_TRANSACTION }
        }


    if (component == "CLIENT_UNICAST"):
        date_field_bottom = date_cis_unicast_split_bottom
        date_field_top = date_cis_unicast_split_top
    else:
        date_field_bottom = date_cis_multicast_split_bottom
        date_field_top = date_cis_multicast_split_top
    
    date_cis_unicast_split_bottom

    if regex == constants[component]["RECEIVED"]:
        # START TIME# [76333] 2019-05-22 16:11:28,285 [6] INFO DCISCCM.DCISSubscriptionManager --> [OG GLFMSTROKE--]--Received Tx:17125 Content: 2861 bytes 
        discipline = re.search(regex, line).group(1)
        trx_id = re.search(regex, line).group(2)
        #print("added trx_id: "+ discipline + "#" + trx_id + " to list.")
        if uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]].get(component) is None:
            uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component] = dict()
            #print(uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]])
        uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component]["start_time"] = datetime_to_milliseconds_dcisccm(" ".join(line.split(" ")[date_field_bottom:date_field_top]))
    elif regex == constants[component]["TIMES"]:
        # END TIME# [395] 2019-03-13 01:54:47.442 {DEC} Times for 34 Decode 0ms Total 30 ms (Source:ZMQ)

        try:
            discipline = re.search(regex, line).group(1)
            trx_id = re.search(regex, line).group(2)
            if uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]].get(component) is not None:
                uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component]["end_time"] = datetime_to_milliseconds_CIS_CLIENT(" ".join(line.split(" ")[date_field_bottom:date_field_top]))
                uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component]["processing_time"] = uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component]["end_time"] - uncompose_ovg_reference[trx_id_dict_to_key[discipline+ "#" + trx_id]][component]["start_time"]
        except KeyError:
            print("error ocurred:")
            #print("searched ready_trx_id: "+ready_trx_id)
            print("value from ready_trx_id: "+ discipline+ "#" + trx_id)
            print("available keys: ")
            pprint.pprint(ready_id_join_trx_id_dict)
            print("available trx to key:")
            pprint.pprint(trx_id_dict_to_key)
            sys.exit(1)


def client_multicast_join_trx_and_ready_id(line,regex):
    # [161] 2019-03-13 01:54:10.174 {ZMQ}  ZMQ Message with ID:8 processed. [*READY* 9 (12932 bytes)][No next]
    # Group 1 = the transaction ID, Group 2 = The ready transaction ID
    # CLIENT_MULTICAST_PROCESSED_TRANSACTION = "ZMQ Message with ID:(\d+?) processed\. \[\*READY\* ([a-zA-Z0-9]+?) \(\d+? bytes\)\]"
    trx_id = re.search(regex, line).group(1)
    ready_trx_id = re.search(regex, line).group(2)
    ready_id_join_trx_id_dict[ready_trx_id] = trx_id


switch_uncompose = {
    log_constants.OVG_INFO_RECEIVED_OVTP_CONST : uncompose_ovg_first_reference,
    log_constants.OVG_INFO_HEADER_PARSED_VALUES_CONST_3 : uncompose_ovg_second_reference,
    log_constants.OVG_MESSAGE_PROCESSED_OK : uncompose_ovg_third_reference,
    log_constants.CEG_INFO_RECEIVED_OVTP_CONST : uncompose_ceg_first_reference,
    log_constants.CEG_INFO_HEADER_PARSED_VALUES_CONST_3 : uncompose_ceg_second_reference,
    log_constants.CEG_MESSAGE_PROCESSED_OK : uncompose_ceg_third_reference,
    log_constants.MOP_MESSAGE_RECEIVED_CONST: mop_add_start_end_time,
    log_constants.MOP_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST : mop_add_start_end_time,
    log_constants.MOP_MESSAGE_PROCESSED_CONST_3 : mop_add_start_end_time,
    log_constants.MOP_MESSAGE_SKIPPED_CONST: mop_add_start_end_time,
    log_constants.MOP_MESSAGE_ERROR_CONST: mop_add_start_end_time,
    log_constants.MOP_TRANSACTION_ID: mop_add_transaction_id,
    log_constants.MOP_CENTRAL_MESSAGE_RECEIVED_CONST: mop_central_add_start_end_time,
    log_constants.MOP_CENTRAL_TOPIC_PROCESSOR_HEADER_PARSED_VALUE_CONST : mop_central_add_start_end_time,
    log_constants.MOP_CENTRAL_MESSAGE_PROCESSED_CONST_3 : mop_central_add_start_end_time,
    log_constants.MOP_CENTRAL_MESSAGE_SKIPPED_CONST: mop_central_add_start_end_time,
    log_constants.MOP_CENTRAL_MESSAGE_ERROR_CONST: mop_central_add_start_end_time,
    log_constants.MOP_CENTRAL_TRANSACTION_ID: mop_central_add_transaction_id,
    log_constants.CID_RT_INFO_RECEIVED_MODELTRANSACTION_CONST: cidrt_add_start_end_time,
    log_constants.CID_RT_INFO_PROCESSED_MODELTRANSACTION_CONST: cidrt_add_start_end_time,
    log_constants.CID_RT_INFO_SENDING_PROJECT_GET_ID: cidrt_add_id,
    log_constants.CID_RT_CENTRAL_INFO_RECEIVED_MODELTRANSACTION_CONST: cidrt_central_add_start_end_time,
    log_constants.CID_RT_CENTRAL_INFO_PROCESSED_MODELTRANSACTION_CONST: cidrt_central_add_start_end_time,
    log_constants.CID_RT_CENTRAL_INFO_SENDING_PROJECT_GET_ID: cidrt_central_add_id,
    log_constants.CIS_CLIENT_RECEIVED_TRANSACTION: cisclient_add_time,
    log_constants.CIS_CLIENT_PROCESSED_TRANSACTION: cisclient_add_time,
    log_constants.VEG_RECEIVED_TRANSACTION: veg_add_time,
    log_constants.VEG_SENT_TRANSACTION: veg_add_time,
    log_constants.VEG_CENTRAL_RECEIVED_TRANSACTION: veg_central_add_time,
    log_constants.VEG_CENTRAL_SENT_TRANSACTION: veg_central_add_time,
    log_constants.CLIENT_MULTICAST_RECEIVED_TRANSACTION: client_multicast_add_time,
    log_constants.CLIENT_MULTICAST_TIMES_TRANSACTION: client_multicast_add_time,
    log_constants.CLIENT_UNICAST_RECEIVED_TRANSACTION: client_unicast_add_time,
    log_constants.CLIENT_UNICAST_TIMES_TRANSACTION: client_unicast_add_time
    #log_constants.CLIENT_MULTICAST_PROCESSED_TRANSACTION: client_multicast_join_trx_and_ready_id
}


def datetime_to_milliseconds(date_time):
    """Converts datetime with pattern: %d/%m/%y-%H:%M:%S,%f to milliseconds.

    Used to every timestamp in logs except CIS CLIENT.

    :param date_time: datetime to be converted
    :return: datetime converted to milliseconds
    """
    return int(datetime.strptime(date_time, "%d/%m/%y-%H:%M:%S,%f").timestamp()*1000)


def datetime_to_milliseconds_dcisccm(date_time):
    """Converts datetime with pattern: %d/%m/%y-%H:%M:%S,%f to milliseconds.

    Used to every timestamp in logs except CIS CLIENT.

    :param date_time: datetime to be converted
    :return: datetime converted to milliseconds
    """
    return int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S,%f").timestamp()*1000)



def datetime_to_milliseconds_CIS_CLIENT(date_time):
    """Converts datetime with pattern: %Y-%m-%d %H:%M:%S.%f to milliseconds.

    Used to CIS CLIENT.

    :param date_time: datetime to be converted
    :return: datetime converted to milliseconds
    """
    #  2019-03-05 18:33:41.650
    return int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f").timestamp()*1000)


## PROCESSING FUNCTIONS ##


def print_results():
    pprint.pprint(results)


switch_headers = {
    
    "OVG": ["DISCIPLINE", "MESSAGE_TYPE", "START_TIME", "END_TIME", "PROCESSING_TIME"],
    "CEG": ["DISCIPLINE", "MESSAGE_TYPE", "START_TIME", "END_TIME", "PROCESSING_TIME"],
    "MOP": ["START_TIME", "END_TIME", "PROCESSING_TIME"],
    "MOP_CENTRAL": ["START_TIME", "END_TIME", "PROCESSING_TIME"],
    "CID_RT": ["DISCIPLINE", "TRX_ID", "START_TIME", "END_TIME", "PROCESSING_TIME"],
    "CIDRT_CENTRAL": ["DISCIPLINE", "TRX_ID", "START_TIME", "END_TIME", "PROCESSING_TIME"],
    "VEG": ["START_TIME", "END_TIME", "PROCESSING_TIME"],
    "VEG_CENTRAL": ["START_TIME", "END_TIME", "PROCESSING_TIME"],
    "CLIENT_MULTICAST": ["START_TIME", "END_TIME", "PROCESSING_TIME"],
    "CLIENT_UNICAST": ["START_TIME", "END_TIME", "PROCESSING_TIME"]
    
}


def save_results():

    available_keys = ['OVG', 'MOP', 'CID_RT', 'VEG', 'CLIENT_MULTICAST', 'CEG', 'MOP_CENTRAL', 'CIDRT_CENTRAL', 'VEG_CENTRAL', 'CLIENT_UNICAST']

    ovg_file = open("./results_OVG.csv", "w")
    ceg_file = open("./results_CEG.csv", "w")
    mop_central_file = open("./results_MOP_CENTRAL.csv", "w")
    mop_file = open("./results_MOP.csv", "w")
    cidrt_file = open("./results_CID_RT.csv", "w")
    cidrt_central_file = open("./results_CIDRT_CENTRAL.csv", "w")
    cis_unicast_file = open("./results_CIS_UNICAST.csv", "w")
    veg_file = open("./results_VEG.csv", "w")
    veg_central_file = open("./results_VEG_CENTRAL.csv", "w")
    cis_multicast_file = open("./results_CIS_MULTICAST.csv", "w")

    switch_file = {
        "OVG":ovg_file,
        "MOP":mop_file,
        "CID_RT":cidrt_file,
        "VEG":veg_file,
        "CLIENT_MULTICAST":cis_multicast_file,
        "CEG":ceg_file,
        "MOP_CENTRAL":mop_central_file,
        "CIDRT_CENTRAL":cidrt_central_file,
        "VEG_CENTRAL":veg_central_file,
        "CLIENT_UNICAST":cis_unicast_file
    }

    ovg_file.write("MESSAGE_ID##"+"##".join(switch_headers["OVG"]) + "\n")
    ceg_file.write("MESSAGE_ID##"+"##".join(switch_headers["CEG"]) + "\n")
    mop_file.write("MESSAGE_ID##"+"##".join(switch_headers["MOP"]) + "\n")
    mop_central_file.write("MESSAGE_ID##"+"##".join(switch_headers["MOP_CENTRAL"]) + "\n")
    cidrt_file.write("MESSAGE_ID##"+"##".join(switch_headers["CID_RT"]) + "\n")
    cidrt_central_file.write("MESSAGE_ID##"+"##".join(switch_headers["CIDRT_CENTRAL"]) + "\n")
    cis_unicast_file.write("MESSAGE_ID##"+"##".join(switch_headers["CLIENT_UNICAST"]) + "\n")
    cis_multicast_file.write("MESSAGE_ID##"+"##".join(switch_headers["CLIENT_MULTICAST"]) + "\n")
    veg_file.write("MESSAGE_ID##"+"##".join(switch_headers["VEG"]) + "\n")
    veg_central_file.write("MESSAGE_ID##"+"##".join(switch_headers["VEG_CENTRAL"]) + "\n")
    #client_multicast_file.write("MESSAGE_ID##"+"##".join(switch_headers["CLIENT_MULTICAST"]) + "\n")

    for id in uncompose_ovg_reference.keys():
        for k in available_keys:
            try:
                file = switch_file[k]
                save_ovg(file, id, uncompose_ovg_reference[id][k], k)
            except Exception as err:
                pass


def save_ovg(file, message_id, elements, application):
    lower_headers = [x.lower() for x in switch_headers[application]]
##    if application == "CLIENT_UNICAST":
##        print(file)
##        print("headers: ")
##        print (lower_headers)
##        print("elements: ")
##        print(elements)
    line = message_id+"##"+"##".join([str(elements[header]) for header in lower_headers])
##    if application == "CEG":
##        print(line)
##        print(file)
    file.write(line+"\n")


def get_value(elements, key):
    try:
        return str(elements[key])
    except KeyError:
        return ""


if __name__ == "__main__":


## Venue
    
    dump_all_logs("dkerovg", DKEROVG_FOLDER_PATH, log_constants.OVG_allowed_lines)
    dump_all_logs("dkermop", DKERMOP_FOLDER_PATH, log_constants.MOP_allowed_lines)
    dump_all_logs("dkercid", DKERCIDRT_FOLDER_PATH, log_constants.CID_RT_allowed_lines)
    dump_all_logs("dkerveg", DKERVEG_FOLDER_PATH, log_constants.VEG_allowed_lines)
    dump_all_logs("client_multicast", CLIENT_MULTICAST_FOLDER_PATH, log_constants.CLIENT_MULTICAST_allowed_lines)


## Central
    dump_all_logs("dkerceg", DKERCEG_FOLDER_PATH, log_constants.CEG_allowed_lines)
    dump_all_logs("dkermop_central", DKERMOP_CENTRAL_FOLDER_PATH, log_constants.MOP_CENTRAL_allowed_lines)
    dump_all_logs("dkercid_central", DKERCIDRT_CENTRAL_FOLDER_PATH, log_constants.CID_RT_CENTRAL_allowed_lines)
    dump_all_logs("dkerveg_central", DKERVEG_CENTRAL_FOLDER_PATH, log_constants.VEG_CENTRAL_allowed_lines)
    dump_all_logs("client_unicast", CLIENT_UNICAST_FOLDER_PATH, log_constants.CLIENT_UNICAST_allowed_lines)
    

    # dump_all_logs("dkercis", DKERCISCLIENT_FOLDER_PATH, log_constants.CIS_CLIENT_allowed_lines)

    # pprint.pprint(uncompose_ovg_reference)
    save_results()
    # logging.info("STARTING PROCESS")
    # # init_configuration()
    # # prepare_xl()
    # print("OVG extraction started")
    # start_ovg()
    # print("OVG extraction finished")
    # print("MOP extraction started")
    # start_mop()
    # print("MOP extraction finished")
    # #start_cidRT()
    # #print_results()
    # save_results_ovg()
    # save_results_mop()
