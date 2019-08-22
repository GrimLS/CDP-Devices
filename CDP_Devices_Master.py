import csv
import os

device_dict = dict()
ip_address_dict = dict()
platform_dict = dict()
capabilities_dict = dict()
localint_dict = dict()
remoteint_dict = dict()
remoteint = dict()
localint = dict()

def isolate_cdp_output(filename):
    #try:
    os.chdir(ReadPath)
    with open(filename, "r") as f:
        #open(f, "q")
        start = 0

        lines = f.readlines()
        #print(lines)
        cdp_output = str()
        for index, line in enumerate(lines):
            #print(index+" "+line)
            if "#sh cdp neigh det | in ID|IP address:|face:|form:" in line:
                #print("Index:", index, "Line:", line)
                start = index + 1
            if "#" in line and start < index and start > 0:
                #print("Index:", index, "Line:", line)
                end = index
                break
        #print("Start and stop: ", start, end)
        for i in range(start, end):
            cdp_output += lines[i] + "\n"
        return cdp_output

    #except:
        #return "Nothing"

def update_device_dict(cdp_output):

    lines_list = cdp_output.split("Device ID: ")
    for index, device in enumerate(lines_list):
        device_id_index = device.find(" ")
        device = device.strip("\n")
        device_id = device[:device_id_index].strip("Platform:").strip("\n\n")
        device_info = device[len(device[:device_id_index].strip("Platform:")):].strip("\n").split(":")
        for index2, i in enumerate(device_info):
            #print(index, i, device_info)
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
        print("index is: ",index," Print the devid ",device_id)
        if index > 0:
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
    #Adjusted ordering
    fieldnames = ['Device ID', 'IP address', 'Platform', 'LocalInt', 'RemoteInt', 'Capabilities']
    output_filename = "CDP_Devices" + "_" + (filename.strip(".log")) + ".csv"
    if os._exists(output_filename):
        try:
            os.open(output_filename)
            for osr in os.read(count):
                count += 1
        except:
            pass

    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if count is 0:
            writer.writeheader()
        count = 0
        for k, v in device_dict.items():
            #print("device dict items count is "+str(count))

            for i in v:
                if "\n" in i:
                    print("There is a newline in this line: ", v)
            if count != 0:
                    writer.writerow({fieldnames[0]: k, fieldnames[1]: v[0], fieldnames[2]: v[1], fieldnames[3]: v[3],
                                     fieldnames[4]: v[4], fieldnames[5]: v[2]})
            count += 1
        return str(os.path)

if __name__ == '__main__':
    # Set this var to false if you want to be prompted for a filename
    Testing = False
    if Testing:
        filename = "Elk_Court_Core_6500_192.168.227.9_2019-08-09-1453-362182145_s.CDPMasterListFilter.s.log"
    else:
        #set base path, assuming a working 'expuxp' folder with Outputs sub folder of files for reading in files
        mainpath = os.getcwd()

        ReadPath = mainpath + "\Outputs"

        for file in os.listdir(ReadPath):
            if "s.CDPMasterListFilter.s" in file:
                #print(file)
                cdp_output = isolate_cdp_output(file)
                #print(cdp_output)
                if cdp_output != "Nothing":
                    device_dict = update_device_dict(cdp_output)
                    outfile = write_to_csv("CDPMasterList", device_dict)
                    print("CSV written to: " + outfile)
    #Done
