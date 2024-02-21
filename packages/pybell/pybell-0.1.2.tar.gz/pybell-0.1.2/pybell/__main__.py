from argparse import ArgumentParser
from pybell.play_ding import play_ding

parser = ArgumentParser()

parser.add_argument('-f', '--file', type=str, default=None,
                    help='The path to the sound file.')

parser.add_argument('-t', '--time', type=float, default=None,
                    help='The time to play the sound for. If None, the sound will be played until it finishes.')

parser.add_argument('-w', '--warning', action='store_true',
                    help='Show a warning dialog after the sound is played. Note that this will block the program until the dialog is closed.')

args = parser.parse_args()

play_ding(args.file, args.time, args.warning)
