import subprocess
import sys

args = sys.argv[1:]

for arg in args:
    subprocess.call(['python', 'CatLights - MIDI Converter.py', arg])
    