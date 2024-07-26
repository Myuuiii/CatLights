import os
import sys
from typing import Dict
from wand.image import Image
import midiutil.MidiFile as MidiFile
import re

#
#
#
# SETTINGS
#
#
#
skipSpeedPrompt = False;

# --------------------------------------------------
#
# Classes
#
class AnimationSource:
    name = "";
    BPM = 0;
    FrameCount = 0;
    Frames = [];

class PixelColor:
    Hex = "";
    
class ResultFrame:
    FrameNumber = 0;
    PixelVelocities = [[0 for x in range(10)] for y in range(10)];

class SourceFrame:
    FrameNumber = 0;
    PixelColors = [[PixelColor() for x in range(10)] for y in range(10)];

#
# Button Mapper
#
MappingArray = [
    [ 0, 28, 29, 30, 31, 32, 33, 34, 35, 27 ],
    [ 108, 64, 65, 66, 67, 96, 97, 98, 99, 100],
    [ 109, 60, 61, 62, 63, 92, 93, 94, 95, 101 ],
    [ 110, 56, 57, 58, 59, 88, 89, 90, 91, 102 ],
    [ 111, 52, 53, 54, 55, 84, 85, 86, 87, 103 ],
    [ 112, 48, 49, 50, 51, 80, 81, 82, 83, 104 ],
    [ 113, 44, 45, 46, 47, 76, 77, 78, 79, 105 ],
    [ 114, 40, 41, 42, 43, 72, 73, 74, 75, 106 ],
    [ 115, 36, 37, 38, 39, 68, 69, 70, 71, 107 ],
    [ 0, 116, 117, 118, 119, 120, 121, 122, 123, 0 ]
]

#
# Color Map Reader
#
def read_color_map(path: str) -> Dict[str, int]:
    color_map = {}
    current_velocity = 1

    with Image(filename=path) as image:
        # Start at the bottom left of the image
        for column in range(4):  # 1 Column 1 4 pixels
            for y in range(7, -1, -1):  # 8 rows
                for x in range(0 + column * 4, 4 + column * 4):  # 4 pixels

                    pixels = list(image.export_pixels(
                        x=x, y=y, width=1, height=1, channel_map="RGB"))

                    hexCode = "#%02x%02x%02x" % (pixels[0], pixels[1], pixels[2])

                    if current_velocity == 128:  # Off value
                        current_velocity = 0

                    color_map[hexCode] = current_velocity
                    current_velocity += 1

    return color_map

#
#
# MAIN FUNCTIONS
#
#

# Function to generate a natural sort key for each filename
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def ImagesToAnimationSource(dirName: str, bpm: int):
    source = AnimationSource()
    source.name = dirName
    source.Frames = []
    source.BPM = bpm

    # Get all the images in the directory, check if the file is not .aseprite
    images = [f for f in os.listdir(dirName) if os.path.isfile(
        os.path.join(dirName, f)) and not f.endswith(".aseprite")]
    images = sorted(images, key=natural_sort_key)
    
    print(images)

    source.FrameCount = len(images)

    for index, image in enumerate(images):
        frame = ImageToSourceFrame(os.path.join(dirName, image), index)
        convertedFrame = ConvertFrame(frame)
        resultFrame = ResultFrame()
        resultFrame.FrameNumber = convertedFrame.FrameNumber
        resultFrame.PixelVelocities = [row[:] for row in convertedFrame.PixelVelocities]
        source.Frames.append(resultFrame)

    return source


def ImageToSourceFrame(fileName: str, index: int):
    frame = SourceFrame()
    frame.FrameNumber = index + 1

    with Image(filename=fileName) as image:

        for x in range(0, 10):
            for y in range(0, 10):
                pixels = list(image.export_pixels(
                    x=y, y=x, width=1, height=1, channel_map="RGB"))
                hex = "#%02x%02x%02x" % (pixels[0], pixels[1], pixels[2])
                frame.PixelColors[x][y].Hex = hex
    return frame


def ConvertFrame(frame: SourceFrame):
    result = ResultFrame()
    result.FrameNumber = frame.FrameNumber
    for i in range(0, len(frame.PixelColors)):
        for j in range(0, len(frame.PixelColors[i])):
            result.PixelVelocities[i][j] = ConvertPixel(
                frame.PixelColors[i][j])
    return result


def ConvertPixel(pixel: PixelColor):
    if pixel.Hex in velocityMap:
        return velocityMap[pixel.Hex]
    else:
        return 0


def WriteMidiFile(animationSource: AnimationSource, noteSpeed: int = 0.1):
    midi = MidiFile.MIDIFile(1)
    track = 0
    time = 0
    midi.addTrackName(track, time, animationSource.name)
    midi.addTempo(track, time, animationSource.BPM)
    channel = 0

    note_times = {}  # Dictionary to keep track of note start and end times

    for frame in animationSource.Frames:
        for i in range(0, len(frame.PixelVelocities)):
            for j in range(0, len(frame.PixelVelocities[i])):
                velocity = frame.PixelVelocities[i][j]
                if velocity > 0 and velocity < 128:
                    noteNumber = MappingArray[i][j]
                    if noteNumber in note_times and note_times[noteNumber][1] == time:
                        # Extend note duration if velocity is the same as previous frame
                        if note_times[noteNumber][2] == velocity:
                            note_times[noteNumber] = (note_times[noteNumber][0], time + noteSpeed, velocity)
                        # Otherwise, add a new note
                        else:
                            midi.addNote(
                                track, channel, noteNumber, note_times[noteNumber][0], note_times[noteNumber][1]-note_times[noteNumber][0], note_times[noteNumber][2])
                            note_times[noteNumber] = (time, time + noteSpeed, velocity)
                    else:
                        note_times[noteNumber] = (time, time + noteSpeed, velocity)
        time += noteSpeed

    # Add the remaining notes
    for noteNumber, note_time in note_times.items():
        midi.addNote(
            track, channel, noteNumber, note_time[0], note_time[1]-note_time[0], note_time[2])

    with open(animationSource.name + ".mid", "wb") as output_file:
        midi.writeFile(output_file)


#
#
#
# EXECUTION
#
#
#
velocityMap = read_color_map("VelocityMap.png")

if len(sys.argv) < 2:
    directoryToProcess = input("Enter directory to process: ")
else:
    directoryToProcess = sys.argv[1]
    
if skipSpeedPrompt == False:
    noteSpeedInput = input("Enter note speed (default 10): ");
    if noteSpeedInput == "":
        noteSpeedInput = 10
else:
    noteSpeedInput = 10

noteSpeed = float(noteSpeedInput) / 100;

WriteMidiFile(ImagesToAnimationSource(directoryToProcess, 250), noteSpeed)