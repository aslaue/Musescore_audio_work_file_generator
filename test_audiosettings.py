from fonctions import *
import json

audiosettings = json.load(open("/home/delphine/Musique/choir_audio_export_tool/example_folder/Super_Mario_Sunshine_Secret_Course_tutti/audiosettings.json"))

# audiosettings_alto = audiosettings_main(audiosettings, "2", {"presetBank": "0", "presetName": "Oboe", "presetProgram": "68"}, 9) #ok
# json.dump(audiosettings_alto, open("audiosettings_sunshine_A.json", 'w+'), indent=4)

audiosettings_instru = audiosettings_instrumental(audiosettings)
json.dump(audiosettings_instru, open("audiosettings_sunshine_instru.json", 'w+'), indent=4)