import win32com.client
import os
import shutil

"""
This takes all the PSD files in a folder, and makes the edits as described below to them,
and exports them as PNG (without saving changes to the original PSD).

It saves them with the name of the PSD file name and the 'date' (as per below) e.g. "psdnamegoeshere_(SATURDAY-08-08-2020).png"
It saves them in a folder called "<date> exports" e.g. "SATURDAY-08-08-2020 exports"

So this will work on any psd file with the following layer names (note these layers can't be in any layer folders)

If it can't find the layer, it moves on as normal.
"""


# all hail https://martechwithme.com/photoshop-scripting-with-python-on-windows/
#################################################
date = "SATURDY 15/15/2020"
time = "8pm"
mc_name = "MC: Matt Coombe"
mc_description = "Roast Battle Hamilton Winner"
title_description = "Faturing 10 comics"
#################################################

layer_name_and_content_dict = {"date" : date, "time" : time, "mc_name" : mc_name, "mc_description" : mc_description, "title_description" : title_description}
# Feel free to add to the above


def edit_document(a_document, layer_name_and_content_dict):
    for layer_name in layer_name_and_content_dict.keys():
        try:
            a_layer = a_document.ArtLayers[layer_name]
            a_layer.TextItem.contents = layer_name_and_content_dict[layer_name]
        except:
            print("The layer name: {} does not exist. Continuing anyway.".format(layer_name))

def export_document(a_document, export_path):
    #a_document.ResizeImage(Width = 2000, Height = 1049, Resolution = 300) # using default / automatic resample

    options = win32com.client.Dispatch('Photoshop.ExportOptionsSaveForWeb')
    options.Format = 13 # corresponds to PNG
    options.PNG8 = False # I.e. use 24 bits
    options.Quality = 100
    options.Interlaced = False
    #options.Transperancy = False

    a_document.Export(ExportIn = export_path, ExportAs = 2, Options = options) # no idea what '2' is


psd_directory = os.path.dirname(os.path.abspath(__file__)) # assuming psd's are with python file

#setup export directory
export_folder_name = "{} exports".format(date.replace("/", "-"))
export_directory = os.path.join(psd_directory, export_folder_name)
if os.path.exists(export_directory): # if directory exists, delete it
    shutil.rmtree(export_directory)
    print("Folder already exists with that name, deleting that now")
os.mkdir(export_directory)

# get psd files
file_scan = os.listdir(psd_directory)

psd_name_list = list()
for file_name in file_scan:
    if ".psd" in file_name:
        psd_name_list.append(file_name)

# open photoshop
photoshop_application = win32com.client.Dispatch("Photoshop.Application")


for psd_name in psd_name_list:
    psd_path = os.path.join(psd_directory, psd_name)
    photoshop_application.Open(psd_path) # open the document
    a_document = photoshop_application.Application.ActiveDocument # get the document object
    
    edit_document(a_document, layer_name_and_content_dict)

    export_name = "{}_({}).png".format(psd_name[: psd_name.rfind(".")], date.replace("/", "-")) # a bit hacky
    export_path = os.path.join(export_directory, export_name)
    export_document(a_document, export_path)
    
    a_document.Close(2) # the 2 means without saving

photoshop_application.Quit()
# make changes


