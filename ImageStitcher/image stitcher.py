from PIL import Image
import shutil # inefficient because i'm only using one thing
import os

def merge_images(image_locations_list):
    # iterate through images open them, get size, close them
    # create new image of that size
    # iterate through images, paste them
    resultant_width = 0
    resultant_height = 0
    for image_location in image_locations_list:
        current_image = Image.open(image_location)
        width, height = current_image.size
        current_image.close()
        if height > resultant_height: # could've used max instead
            resultant_height = height
        resultant_width += width

    resultant_image = Image.new('RGBA', (resultant_width, resultant_height))
    current_width = 0
    for image_location in image_locations_list:
        current_image = Image.open(image_location)
        width, height = current_image.size
        resultant_image.paste(im = current_image, box=(current_width, 0))
        current_width += width
    return resultant_image, resultant_width, resultant_height # getting them from here is more efficient

def get_scan(pack_location):
    dir_scan_list = list()
    scan_list = os.listdir(pack_location)
    for material_name in scan_list:
        a_path = pack_location + "\\" + material_name
        if os.path.isdir(a_path) == False and ".png" in material_name: # i.e. files only. first part redundant
            dir_scan_list.append(a_path)
    return dir_scan_list

#a_location = r"C:\Users\Nathan Longhurst\Desktop\Python_Image_Fun\All Modules\Module1"
dir_name, file_name = os.path.split(os.path.abspath(__file__)) # from internet
a_location = dir_name

image_locations_list = get_scan(a_location)
image_locations_list = sorted(image_locations_list, key=os.path.getmtime) # lol got this off the internet

print("This is going to take all the .png files open in this folder, and merge them into one file, relative to the items you want per row")
row_size = int(input("How many per row? "))
    

end_height = 0
end_width = 0
temp_dir_loc = a_location + "\\" + "temp_dir"
try:
    temp_dir = os.mkdir(a_location + "\\" + "temp_dir")
except:
    print("temp folder already exists, please delete it")
    exit()


row_count = 0
while len(image_locations_list) != 0:
    row_count += 1
    current_locations = image_locations_list[:row_size]
    image_locations_list = image_locations_list[row_size:] # memory intensive, better option to pop?
    resultant_image, resultant_width, resultant_height = merge_images(current_locations)
    end_width = max(end_width, resultant_width)
    end_height += resultant_height
    result_file_path = temp_dir_loc + "\\" + "merged_row" + str(row_count) + ".png"
    resultant_image.save(result_file_path)
    resultant_image.close()

#image_locations_list = get_scan(temp_dir_loc)
#end_image = Image.new('RGBA', (end_width, end_height))
#current_height = 0
#for image_location in image_locations_list:
#    current_image = Image.open(image_location)
#    width, height = current_image.size
#    end_image.paste(im = current_image, box=(0, current_height))
#    current_height += height
#    current_image.close()
#end_file_path = a_location + "\\" + "merged_in_rows_" + str(row_size) + ".png"
#end_image.save(end_file_path)
#end_image.close()

#shutil.rmtree(temp_dir_loc) # deletes temp directory and its contents
    
