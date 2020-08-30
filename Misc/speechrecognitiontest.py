import os
import shutil

import speech_recognition
import os
from pydub import AudioSegment

os.environ["PATH"] += os.pathsep + '/usr/local/bin' # because my ffmpeg is here, and pydub doesn't look there otherwise



input_file_path = "L7audio.wav" # relative path to input file (includ  extension)
file_name, extension = os.path.splitext(input_file_path)



python_file_directory = os.path.dirname(__file__)
export_directory = os.path.join(python_file_directory, file_name) # up to you

if os.path.exists(export_directory) == True:
    shutil.rmtree(export_directory)
os.mkdir(export_directory)


audio_file = AudioSegment.from_file(input_file_path)

####### Iterate through audio in chunks, export, transcribe, delete #######

a_file = open(os.path.join(export_directory, "transcribed.txt"), "w")
recognizer_object = speech_recognition.Recognizer()

export_duration = 120000 # in milliseconds, choose yourself

current_audio_position = 0 # in milliseconds
current_count = 0 # for export file name
        
max_count = 1000000000
while True:
    try:
        end_audio_position = current_audio_position + export_duration
        
        cropped_audio_file = audio_file[current_audio_position : end_audio_position]

        export_name = str(current_count).zfill(5)
        export_path = os.path.join(export_directory, export_name)
        cropped_audio_file.export(export_path, format = "wav")

        #if current_count % 100 == 0: # print progress
        #    print("exported: {}".format(export_path))

        with speech_recognition.AudioFile(export_path) as source:
            audio = recognizer_object.record(source) # some audio object?
            output_string = recognizer_object.recognize_google(audio)

        a_file.write(output_string + "\n")
        print(output_string) # fun to see progress printed
        
        os.remove(export_path) # delete aduio file permanently 


        if current_count == max_count: # after exported max_count, break
            print("max count reached")
            break

        current_audio_position += export_duration
        current_count += 1
    except Exception as exception: # exceeded sound file length duration
        print(exception)
        break

a_file.close()
print("finished")


########################################
