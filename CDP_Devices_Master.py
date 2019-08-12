import csv
import os

def isolate_cdp_output(filename):
    with open(filename, "r") as f:
        start = 0
        lines = f.readlines()
        cdp_output = str()
        for index, line in enumerate(lines):
            if "#sh cdp neigh det | in ID|IP address:|face:|form:" in line:
                #print("Index:", index, "Line:", line)
                start = index + 1
            if "#" in line and start < index and start > 0:
                #print("Index:", index, "Line:", line)
                end = index
                break
        print("Start and stop: ", start, end)
        for i in range(start, end):
            cdp_output += lines[i] + "\n"
        return cdp_output

def create_device_dict(cdp_output):
    device_dict = dict()
    ip_address_dict = dict()
    platform_dict = dict()
    capabilities_dict = dict()
    localint_dict = dict()
    remoteint_dict = dict()
    remoteint = dict()
    localint = dict()
    lines_list = cdp_output.split("Device ID: ")
    for index, device in enumerate(lines_list):
        device_id_index = device.find(" ")
        device = device.strip("\n")
        device_id = str(index) + ": " + device[:device_id_index].strip("Platform:").strip("\n\n")
        device_info = device[len(device[:device_id_index].strip("Platform:")):].strip("\n").split(":")
        for index2, i in enumerate(device_info):
            print(index, i, device_info)
            if "IP address" in i:
                if "\n\n" in i: i = i.strip("\n\n")
                #print(index, "Should be ip address: ", device_info[index2 + 1].strip("\nPlatform"), "end print")
                ip_address_dict[index] = device_info[index2 + 1].strip("\nPlatform")
            if "Platform" in i:
                platform_dict[index] = device_info[index2 + 1].strip(", Capabilities")
            if "Capabilities" in i:
                capabilities_dict[index] = device_info[index2 + 1].strip("\nInterface")
            if "Interface" in i:
                remoteint_dict[index] = device_info[index2 + 1].strip(",  Port ID (outgoing port)")
            if "Port ID" in i:
                if "Ethernet" in device_info[index2 + 1]:
                    x = device_info[index2 + 1].strip(" ").split("\n")
                    localint_dict[index] = x[0]
                else:
                    localint_dict[index] = device_info[index2 + 1].strip(" ")
        device_dict[device_id] = list()
        try:
            device_dict[device_id].append(ip_address_dict[index])
        except:
            device_dict[device_id].append("None")
        if device_id[0] != 0 and index > 0:
            device_dict[device_id].append(platform_dict[index])
            device_dict[device_id].append(capabilities_dict[index])
            device_dict[device_id].append(remoteint_dict[index])
            device_dict[device_id].append(localint_dict[index])
        else:
            device_dict[device_id].append("Non valid device entry")
    return device_dict

def write_to_csv(filename, dict):
    count = 0
    #fieldnames = ['Device ID', 'IP address', 'Platform', 'Capabilities', 'RemoteInt', 'LocalInt']
    fieldnames = ['Device ID', 'IP address', 'Platform', 'LocalInt', 'RemoteInt', 'Capabilities']
    output_filename = "CDP_Devices" + "_" + (filename.strip(".log")) + ".csv"
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in device_dict.items():
            count += 1
            print(v)
            for i in v:
                if "\n" in i:
                    print("There is a newline in this line: ", v)
            #print("What I'm trying to write", v[11], count, fieldnames[5])
#            if len(v) == 12:
            if k != "0: ":
                    #writer.writerow({fieldnames[0]: k, fieldnames[1]: v[0], fieldnames[2]: v[1], fieldnames[3]: v[2], fieldnames[4]: v[3], fieldnames[5]: v[4]})
                    writer.writerow({fieldnames[0]: k, fieldnames[1]: v[0], fieldnames[2]: v[1], fieldnames[3]: v[3],
                                     fieldnames[4]: v[4], fieldnames[5]: v[2]})
            else:
                print("list index out of range", count, k, v)
            print("Running file writes", count)

# Set this var to false if you want to be prompted for a filename
Testing = False
if Testing:
    filename = "Elk_Court_Core_6500_192.168.227.9_2019-08-09-1453-362182145_s.CDPMasterListFilter.s.log"
else:
    #set base path, assuming a working 'expuxp' folder with Outputs sub folder of files for reading in files
    mainpath = os.getcwd()
    ReadPath = mainpath + "\Outputs"
    CSVOutDir = (mainpath + "\CDP Device CSV Files")

    #change working dir to Readpath, creating if non-existant
    os.chdir(ReadPath)
    if not os.path.abspath(CSVOutDir):
        os.mkdir(CSVOutDir)

    #change working dir to output folder, loop through files and generate csv outputs.
    os.chdir(CSVOutDir)
    #os.chdir(mainpath)
    for file in os.listdir(ReadPath):
        if "s.CDPMasterListFilter.s" in file:
            print(file)
            cdp_output = isolate_cdp_output(file)
            device_dict = create_device_dict(cdp_output)
            write_to_csv(file + ".csv", device_dict)

    #Done