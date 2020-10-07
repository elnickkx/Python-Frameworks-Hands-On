import os

def fileHandling(strData, filepath):
    readdata = ""
    if type(strData) == list:
        for i in strData:
            readdata = "".join(i.replace("\n", ""))
            with open(filepath, 'a+') as fl:
                fl.write(readdata)
    
    return filepath
    
def fileFormatter(filePath, newPath):
    fileOpen = open(filePath, 'r+')
    filedata = fileOpen.readlines()
    
    return fileHandling(filedata, newPath)
    
    
    
# def spaceHandling(filepath):
#     fl_open = open(filepath)
#     filedata = (fl_open.readlines()[0]).split(".")
#     str_data = ""
#     for data in filedata:
#         str_data = "".join(data.strip())
#         with open("new1.txt", 'a+') as fl:
#             fl.write(str_data)
