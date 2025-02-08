from copy import deepcopy
import sys, os, zipfile, json, shutil

def audiosettings_main(content_audiosettings: dict, main_partId: str, new_sound: dict[str, str, str], new_volume: int, metronome: bool=False, mute_others: bool=False):
    """
    Produces an audiosettings file for isolating a main part:
    * Replaces the main instrument/voice's sound by another, useful for replacing rythmically inaccurate sounds such as voices.
    * Modifies the volume of the main instrument and lowers the volume of the metronome

    Arguments:
        content_audiosettings: dict          # content of the audiosettings.json file from the original mscz
        main_partId: str          # identifier (in the audiosettings.json) of the main instrument/voice. It's actually an int in str form like "0"
        new_sound:  {"presetBank": str,      # usually "O"
                 "presetName": str,          # instrument name e.g. "Oboe"
                 "presetProgram": str}       # instrument program value e.g. "68"
                Instrument sound we want to replace the original with. You can find the bank and program numbers in the MS Basic database:
                https://docs.google.com/spreadsheets/d/1SwqZb8lq5rfv5regPSA10drWjUAoi65EuMoYtG-4k5s/edit?gid=133112496#gid=133112496
        new_volume: int                      # volume of the main part in Db
        metronome: bool                      # put True AND activate metronome manually in Musescore if you want the metronome
        mute_others: bool                    # put True if you just want the main instrument (e.g. piano file)

    Returns:
        new_audiosettings: dict              # a modified copy of the original audiosettings.json
    """

    new_audiosettings = deepcopy(content_audiosettings)
    main_partId_found = False

    for track in new_audiosettings["tracks"]:
        if track["partId"] == main_partId: # locate the instrument we want to replace
            main_partId_found = True
            track["in"]["resourceMeta"]["attributes"].update(new_sound)
            track["in"]["resourceMeta"].update({"id": "MS Basic\\" + new_sound["presetBank"] + "\\" + new_sound["presetProgram"]})
            track["out"]["volumeDb"] = new_volume
        elif track["partId"] == "999": #"999" is the metronome id
            track["soloMuteState"]["mute"] = not metronome
            # track["out"]["volumeDb"].update(-9) #TODO: put that in the wrapper for tutti
        else:
            track["soloMuteState"]["mute"] = mute_others
            track["out"]["volumeDb"] = 0

    if main_partId_found:
        return new_audiosettings
    else:
        raise Exception("Track partId not found")
        return content_audiosettings

def audiosettings_instrumental(content_audiosettings: dict, metronome: bool=False, voice_list: list=["soprano", "alto", "tenor", "bass", "baritone", "mezzo-soprano", "women", "men", "voice", "kazoo"]):
    """
    Produces an instrumental audiosettings file for pieces with vocals.

    Arguments:
        content_audiosettings: dict   # content of the audiosettings.json file from the original mscz
        metronome: bool               # put True AND activate metronome manually in Musescore if you want the metronome
        voice_list: list              # voices as defined by Musescore by default (yes, kazoo is in there), but you can customise who you want to shut up

    Returns:
        new_audiosettings: dict       # a modified copy of the original audiosettings.json
    """

    new_audiosettings = deepcopy(content_audiosettings)

    for track in new_audiosettings["tracks"]:
        if track["instrumentId"] in voice_list:
            track["soloMuteState"]["mute"] = True

    return new_audiosettings

# def voice_to_partId(voice: Union[tuple|str], audiosettings: dict):
#     """
#     Finds given voice (e.g. ("soprano", 1), ("alto", 2), "piano"...) in audiosettings.json and returns the corresponding partId
#     """

#     if type(voice)==tuple:
    # instrumentId = voice[0]