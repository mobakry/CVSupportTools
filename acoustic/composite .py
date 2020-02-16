'''
This code composes two files as a foreground and background audios
to use this write this command on your cmd:
python composite.py path\to\FGfiles path\to\BGfiles path\to\outputs FilesNumber

p.s: you can use sample files in background and foreground folders

'''

import scaper
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='')

parser.add_argument("FilesPath", type=str, help="A directory of foreground folders")
parser.add_argument("BackGround", type=str, help="A deirectory of background folders")
parser.add_argument("OutPath", type=str, help="A directory to store output files")
parser.add_argument("Nfiles",type=int, help="Numer of out files")

args = parser.parse_args()


Num_files = args.Nfiles
# OUTPUT FOLDER
outfolder = args.OutPath

# SCAPER SETTINGS
fg_folder = args.FilesPath
bg_folder = args.BackGround

ref_db = -40
duration = 20.0

source_time_dist = 'const'
source_time = 0.0

event_time_dist = 'truncnorm'
event_time_mean = 5.0
event_time_std = 2.0
event_time_min = 0.0
event_time_max = 10.0


event_duration_dist = 'const'
event_duration_value = 0.2

snr_dist = 'const'
snr_min = 20



for i in range(Num_files):

    # create a scaper
    sc = scaper.Scaper(duration, fg_folder, bg_folder)
    sc.protected_labels = []
    sc.ref_db = ref_db


    # add background
    sc.add_background(label=('choose', []),
                        source_file=('choose', []),
                        source_time=('const', 0))

    # add random number of foreground events

    sc.add_event(label=('choose', []),
                source_file=('choose', []),
                 source_time=(source_time_dist, source_time),
                 event_time=(event_time_dist, event_time_mean, event_time_std, event_time_min, event_time_max),
                 event_duration=(event_duration_dist, event_duration_value),
                 snr=(snr_dist, snr_min),
                 pitch_shift=None,
                 time_stretch=None)
    #(time_stretch_dist, time_stretch_min, time_stretch_max)
    # generate
    audiofile = os.path.join(outfolder, "sound{:d}.wav".format(i+1))
    jamsfile = os.path.join(outfolder, "sound{:d}.jams".format(i+1))
    txtfile = os.path.join(outfolder, "sound{:d}.txt".format(i+1))

    sc.generate(audiofile, jamsfile,
                allow_repeated_label=True,
                allow_repeated_source=False,
                reverb=0.1,
                disable_sox_warnings=True,
                no_audio=False,
                txt_path=txtfile)
