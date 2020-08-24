import os
import math
from skimage.metrics import _structural_similarity as ssim
import cv2
import numpy as np
import img2pdf
import shutil

# use https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# uses https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames/33439833

def mse(imageA, imageB): # copy and pasted from from above link (pretend that I imported it from a module)
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def get_greyscale_image(a_image): # when it says 'a_image' it's really a_image object etc.
    #a_image = cv2.imread(a_path) # open cv image object
    greyscale_image = cv2.cvtColor(a_image, cv2.COLOR_BGR2GRAY)
    return greyscale_image

def get_similarity_value(image_object_1, image_object_2): # pass image object
    greyscale_image_1 = get_greyscale_image(image_object_1) # didn't add 'object' to variable name, but you get the idea
    greyscale_image_2 = get_greyscale_image(image_object_2)
    # i'm not sure why we put it in to greyscale, but I have nothing against it
    # perhaps it's better for the algorithm?

    # using SSIM
    #similarity_value = ssim.structural_similarity(greyscale_image_1, greyscale_image_2) # note, if images are color tyen multichannel = True will do the trick
    # not using color for the sake of unnecessary
    # the range is -1 to 1 (1 indicates perfect similarity)

    # using MSE (0 is perfect match, and increases as less of a match)
    similarity_value = mse(greyscale_image_1, greyscale_image_2)
    
    
    return similarity_value

def export_image_as_png(image_object, export_directory, export_name): # this is specialised
    file_name = "{}.png".format(export_name)
    file_path = os.path.join(export_directory, file_name)
    cv2.imwrite(file_path, image_object)

def get_images_dict(video_path, second_intervals, smallest_similarity_value): # gets images with a similarity value greater than asked
    video_capture_object = cv2.VideoCapture(video_path)
    video_fps = video_capture_object.get(cv2.CAP_PROP_FPS)
    frames_to_wait = round(video_fps * second_intervals) # rounded

    export_count = 1 # starting count at 1
    success_bool = True
    images_dict = dict() # used later
    current_frame = 0
    while True: # each iteration of this is a contending export

        success_bool, image_object = video_capture_object.read() # called it image_object to be clear
        current_frame += 1

        if current_frame % 10 == 0: # stops printing so much (weird requirement). A better thing would be to print every 30 seconds or something.
            print("current_frame: {} (i.e. {:.2f} seconds in to the video)".format(current_frame, current_frame / video_fps))
        
        if success_bool == False: # this seems clearest
            break

        if export_count == 1:
            images_dict[export_count] = image_object
            export_count += 1
        else:
            similarity_value = get_similarity_value(image_object, images_dict[export_count - 1])
            #print("similarity_value to previous export: {:.2f}, if different enough, export count is {}".format(similarity_value, export_count))
            if similarity_value > smallest_similarity_value:
                #print("different enough!")
                images_dict[export_count] = image_object # repeated code, but feels clearer
                export_count += 1
            

        # skip frames
        for i in range(frames_to_wait): # this is slower than a while loop
            video_capture_object.read()
            current_frame += 1

    return images_dict

    #print("\n") # new line each export

    # a smart way would be to brashly go through the video and see when changes happen, and then go to those locations and take the
    # last frame possible before the drastic change (as that is the frame i'm after).
    # get_counts_to_keep_list achieves the same result (just breaks it up in to two steps, which is inefficient)


def get_counts_to_keep_list(images_dict, minimum_similarity_value):
    # a haphazard thing to do (i.e. doing it after the fact) is to go through all the exports and take the last one before a massive
    # similarity value change. This is bad because it is recalculating the similarity value

    # as per algrithm decided on paper (compare two at a time, and if a spike in similarity: take one on left (that'll be the latest version of slide))
    last_count = max(images_dict.keys())
    counts_to_keep_list = list()
    for count in range(1, last_count): # sp gets up to the second to last count
        image_1 = images_dict[count]
        image_2 = images_dict[count + 1]
        
        similarity_value = get_similarity_value(image_1, image_2)

        if count == last_count - 1: # i.e. count is the second to last image (last iteration)
                
            if similarity_value > minimum_similarity_value: # keep both (the second to last is the latest version, and the last is a new slide)
                counts_to_keep_list.append(count) # I haven't seen this case, so assuming it works
                counts_to_keep_list.append(count + 1)
            else: # the last is the latest version of thes lide
                counts_to_keep_list.append(count + 1)
        
        elif similarity_value > minimum_similarity_value:
            counts_to_keep_list.append(count)

    return counts_to_keep_list

housing_directory = os.path.dirname(os.path.abspath(__file__))
smallest_similarity_value = 100 
# tests found (using mse)
# slightly above 1 if the frame is exactly the same (i'm guessing greyscale has rounding errors?)
# slightly under 25 if the mouse is moving around
# the slide adding a new line: gave 173 and 272
second_intervals =  2 # how often should it wait to take the next frame?
# obviously this program does it's job 100% if it checks the video for every frame, but that's too slow, so the seconds
# kind of have to find a balance


video_directory = os.path.dirname(os.path.abspath(__file__)) # choose

scan_list = os.scandir(video_directory)
video_path_list = [file_name.path for file_name in scan_list if ".mp4" in file_name.name]

for video_path in video_path_list:

        video_name = video_path[video_path.rfind("\\") + 1 : video_path.rfind(".")]  # returns the name of the video without extension (crass)
        export_directory = os.path.join(housing_directory, video_name)

        if os.path.exists(export_directory):
                shutil.rmtree(export_directory)
        os.mkdir(export_directory)

        images_dict = get_images_dict(video_path, second_intervals, smallest_similarity_value)
        # perhaps the below is unnecessary (i.e. perhaps a  simple modification to the above can be made) to achieve the latter
        counts_to_keep_list = get_counts_to_keep_list(images_dict, 400) # look through images per above, and get latest version of slide


        slide_count = 1 # more like final-version-of-slide slide count
        for export_count in counts_to_keep_list:
            export_name = "slide {}".format(slide_count) # without extension
            export_image_as_png(images_dict[export_count], export_directory, export_name)

            slide_count += 1

        ########## export to pdf
        export_pdf_path = os.path.join(export_directory, "{}.pdf".format(video_name)) 



        # gross since it recalculates the paths

        with open(export_pdf_path, "wb") as file:
            image_paths_list = [direntry_object.path for direntry_object in os.scandir(export_directory) if ".png" in direntry_object.path]
            print(image_paths_list)
            information = img2pdf.convert(image_paths_list)
            file.write(information)


# I should make a "get slides" function which cleans this all up. This is gross code.
